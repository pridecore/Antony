import queue
import sounddevice as sd
import vosk
import json
import os
import threading

# Шлях до моделі (розпакованої)
MODEL_PATH = "models/vosk-model-small-ua-0.22"

# Перевірка наявності моделі
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"[Vosk ❌] Модель не знайдено у '{MODEL_PATH}' — спочатку завантаж її!")

model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time_, status):
    if status:
        print(f"[Mic ⚠️]: {status}")
    q.put(bytes(indata))

def get_voice_input(timeout: int = 10) -> str:
    """
    Слухає мікрофон, розпізнає мову та повертає текст.
    timeout — максимальний час очікування голосу у секундах.
    """
    print("[🎧 Antony слухає тебе...]")

    result_text = ""
    done_event = threading.Event()

    def recognition_thread():
        nonlocal result_text
        rec = vosk.KaldiRecognizer(model, 16000)
        try:
            while not done_event.is_set():
                data = q.get()
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    text = res.get("text", "").strip()
                    if text:
                        result_text = text
                        done_event.set()
                        break
        except Exception as e:
            print(f"[Vosk Error]: {e}")
            done_event.set()

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            thread = threading.Thread(target=recognition_thread)
            thread.start()

            # Очікуємо або тайм-аут
            thread.join(timeout=timeout)
            done_event.set()  # Якщо тайм-аут, сигналізуємо вихід

            thread.join()  # Гарантуємо завершення потоку

    except KeyboardInterrupt:
        print("\n[Antony]: Голосовий ввід перервано вручну.")
    except Exception as e:
        print(f"[Antony]: Помилка аудіо: {e}")

    if result_text:
        print(f"[Antony 🗣️]: Розпізнано: {result_text}")
    else:
        print("[Antony]: Не почуто жодного голосу або тайм-аут.")

    return result_text