import json
import os
import queue
import threading
import time
import urllib.request
import zipfile

from config import DATA_DIR

MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = os.path.join(DATA_DIR, MODEL_NAME)
MODEL_ZIP = os.path.join(DATA_DIR, f"{MODEL_NAME}.zip")


def _download_model():
    os.makedirs(DATA_DIR, exist_ok=True)
    for attempt in range(2):
        if os.path.exists(MODEL_ZIP):
            os.remove(MODEL_ZIP)
        urllib.request.urlretrieve(MODEL_URL, MODEL_ZIP)
        if not zipfile.is_zipfile(MODEL_ZIP):
            if attempt == 0:
                continue
            raise RuntimeError("Downloaded voice model archive is invalid.")
        with zipfile.ZipFile(MODEL_ZIP, "r") as archive:
            archive.extractall(DATA_DIR)
        if os.path.exists(MODEL_ZIP):
            os.remove(MODEL_ZIP)
        return


class VoiceOutput:
    def __init__(self, volume):
        self.available = False
        self.engine = None
        self._lock = threading.Lock()
        try:
            import pyttsx3
        except ImportError:
            return
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", volume)
            self.available = True
        except Exception:
            self.engine = None
            self.available = False

    def set_volume(self, volume):
        if not self.available:
            return
        try:
            self.engine.setProperty("volume", volume)
        except Exception:
            return

    def speak(self, text, interrupt=True):
        if not self.available or not text:
            return False
        if interrupt:
            self.stop()

        def run():
            with self._lock:
                self.engine.say(text)
                self.engine.runAndWait()

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return True

    def stop(self):
        if not self.available:
            return
        try:
            self.engine.stop()
        except Exception:
            return


class VoiceInput:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.available = False
        self.model_ready = False
        self.model = None
        self.listening = False
        self.status = ""
        self._preparing = False
        self._stop_event = threading.Event()
        try:
            import sounddevice as sd
            import vosk
        except ImportError:
            self.status = "Voice input not installed."
            return
        self.sd = sd
        self.vosk = vosk
        self.available = True

    def _set_status(self, text):
        self.status = text

    def prepare_async(self):
        if not self.available or self.model_ready or self._preparing:
            return
        self._preparing = True
        threading.Thread(target=self._prepare, daemon=True).start()

    def _prepare(self):
        self._set_status("Preparing voice model...")
        try:
            if not os.path.isdir(self.model_dir):
                _download_model()
            self.model = self.vosk.Model(self.model_dir)
            self.model_ready = True
            self._set_status("")
        except Exception as exc:
            self._set_status(f"Voice input unavailable: {exc}")
        finally:
            self._preparing = False

    def start_listening(self, on_text, on_error, timeout=5):
        if not self.available:
            on_error("Voice input is unavailable.")
            return False
        if not self.model_ready:
            self.prepare_async()
            on_error("Voice model is preparing. Try again in a moment.")
            return False
        if self.listening:
            return False

        self.listening = True
        self._stop_event.clear()
        threading.Thread(
            target=self._listen_worker,
            args=(on_text, on_error, timeout),
            daemon=True,
        ).start()
        return True

    def _listen_worker(self, on_text, on_error, timeout):
        self._set_status("Listening...")
        audio_queue = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status:
                return
            audio_queue.put(bytes(indata))

        try:
            with self.sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                recognizer = self.vosk.KaldiRecognizer(self.model, 16000)
                start_time = time.time()
                result_text = ""
                partial_text = ""
                while not self._stop_event.is_set():
                    try:
                        data = audio_queue.get(timeout=0.1)
                    except queue.Empty:
                        if time.time() - start_time > timeout:
                            break
                        continue
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        result_text = result.get("text", "").strip()
                        if result_text:
                            break
                    else:
                        partial = json.loads(recognizer.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                if not self._stop_event.is_set():
                    if not result_text:
                        final = json.loads(recognizer.FinalResult())
                        result_text = final.get("text", "").strip()
                    if len(result_text) < 2:
                        if len(partial_text) >= 2:
                            on_text(partial_text)
                            return
                        on_error("No speech detected.")
                    else:
                        on_text(result_text)
        except Exception:
            if not self._stop_event.is_set():
                on_error("Microphone unavailable.")
        finally:
            self.listening = False
            self._set_status("")

    def stop_listening(self):
        if not self.listening:
            return
        self._stop_event.set()
        self.listening = False
        self._set_status("")


class VoiceManager:
    def __init__(self, settings):
        self.settings = settings
        self.input_enabled = settings.get("voice_input", True)
        self.output_enabled = settings.get("voice_output", True)
        self.voice_volume = settings.get("voice_volume", 0.8)
        self.output = VoiceOutput(self.voice_volume)
        self.input = VoiceInput(MODEL_DIR)
        if self.input_enabled:
            self.input.prepare_async()

    def set_input_enabled(self, enabled):
        self.input_enabled = enabled
        self.settings["voice_input"] = enabled
        if enabled:
            self.input.prepare_async()
        else:
            self.input.stop_listening()

    def set_output_enabled(self, enabled):
        self.output_enabled = enabled
        self.settings["voice_output"] = enabled
        if not enabled:
            self.output.stop()

    def set_volume(self, volume):
        self.voice_volume = volume
        self.settings["voice_volume"] = volume
        self.output.set_volume(volume)

    def speak(self, text, interrupt=True):
        if not self.output_enabled:
            return False
        return self.output.speak(text, interrupt=interrupt)

    def stop_speaking(self):
        self.output.stop()

    def start_listening(self, on_text, on_error, timeout=5):
        if not self.input_enabled:
            on_error("Voice input is off.")
            return False
        self.output.stop()
        return self.input.start_listening(on_text, on_error, timeout)

    def stop_listening(self):
        self.input.stop_listening()

    @property
    def listening(self):
        return self.input.listening

    @property
    def status(self):
        return self.input.status
