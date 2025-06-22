import os
import numpy as np
from TTS.api import TTS
import simpleaudio as sa
from scipy.io.wavfile import write as write_wav
import threading

# Назва української моделі VITS з Hugging Face
MODEL_NAME = "svito-zar/ukrainian_vits"

print("[Antony] Ініціалізація голосового синтезу...")
tts = TTS(MODEL_NAME)

def _play_audio(filepath: str):
    try:
        wave_obj = sa.WaveObject.from_wave_file(filepath)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"[Antony ⚠️] Помилка відтворення аудіо: {e}")
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"[Antony ⚠️] Не вдалося видалити тимчасовий файл: {e}")

def speak(text: str):
    print(f"[Antony 🎙️]: {text}")
    try:
        # Отримуємо аудіо-масив (numpy) із синтезатора
        wav = tts.tts(text)
        sample_rate = 22050  # Для цієї моделі зазвичай 22050 Гц

        temp_wav_path = "temp_output.wav"
        # Приводимо float32 масив до int16 для WAV формату
        wav_int16 = np.int16(wav * 32767)
        write_wav(temp_wav_path, sample_rate, wav_int16)

        # Відтворення в окремому потоці, щоб не блокувати
        threading.Thread(target=_play_audio, args=(temp_wav_path,), daemon=True).start()

    except Exception as e:
        print(f"[Antony ⚠️] Помилка в speak(): {e}")