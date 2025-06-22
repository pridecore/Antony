import random
import datetime
import json
import os

class EmotionEngine:
    def __init__(self, path="data/mood.json"):
        self.path = path
        self.mood = self._load_mood()

    def _load_mood(self):
        if not os.path.exists(self.path):
            mood = {
                "state": "neutral",
                "intensity": 0.5,
                "history": []
            }
            self._save_mood(mood)
            return mood
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise json.JSONDecodeError("Empty file", "", 0)
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            # Якщо файл порожній або пошкоджений — створюємо дефолтний
            mood = {
                "state": "neutral",
                "intensity": 0.5,
                "history": []
            }
            self._save_mood(mood)
            return mood

    def _save_mood(self, mood):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(mood, f, indent=4, ensure_ascii=False)

    def get_mood(self):
        return self.mood["state"], self.mood["intensity"]

    def set_mood(self, new_mood, intensity=0.5):
        if new_mood not in ["happy", "neutral", "sad", "angry", "excited", "bored"]:
            return False
        self.mood["state"] = new_mood
        self.mood["intensity"] = float(max(0.0, min(1.0, intensity)))
        self.mood["history"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "mood": new_mood,
            "intensity": self.mood["intensity"]
        })
        self._save_mood(self.mood)
        return True

    def respond_with_emotion(self, message: str) -> str:
        mood, intensity = self.get_mood()
        emoji = {
            "happy": "😄", "sad": "😔", "angry": "😠", "excited": "🔥",
            "bored": "😐", "neutral": "🤖"
        }.get(mood, "🤖")

        modifiers = {
            "happy": ["радісно", "з приємністю"],
            "sad": ["з гіркотою", "повільно"],
            "angry": ["різко", "суворо"],
            "excited": ["ентузіастично", "енергійно"],
            "bored": ["монотонно", "байдуже"],
            "neutral": [""]
        }
        mood_line = random.choice(modifiers.get(mood, [""]))
        prefix = f"{emoji} ({mood_line}) " if mood_line else f"{emoji} "
        return prefix + message

    def auto_adjust_mood(self, input_text: str):
        lowered = input_text.lower()
        triggers = {
            "happy": ["дякую", "вдячний", "молодець", "чудово", "добре"],
            "sad": ["сумно", "погано", "втомився", "самотній", "боляче"],
            "angry": ["ненавиджу", "дратує", "злий", "чорт", "непотрібно"],
            "excited": ["ура", "відмінно", "свято", "успіх"],
            "bored": ["нудно", "нічого", "байдуже", "все набридло"]
        }

        matched_mood = "neutral"
        intensity = 0.5

        for mood, keywords in triggers.items():
            for kw in keywords:
                if kw in lowered:
                    matched_mood = mood
                    intensity = random.uniform(0.6, 1.0)
                    break

        self.set_mood(matched_mood, intensity)

    def get_mood_history(self, limit=5):
        return self.mood["history"][-limit:]



# Глобальний екземпляр емоційного двигуна
emotion_engine = EmotionEngine()

def update_emotional_state(user_input: str):
    """Оновлює емоційний стан на основі вводу користувача."""
    emotion_engine.auto_adjust_mood(user_input)

def get_emotional_prefix() -> str:
    """Повертає емоційний префікс (emoji + стиль) для відповіді."""
    mood, intensity = emotion_engine.get_mood()
    emoji_map = {
        "happy": "😄",
        "sad": "😔",
        "angry": "😠",
        "excited": "🔥",
        "bored": "😐",
        "neutral": "🤖"
    }
    emoji = emoji_map.get(mood, "🤖")
    return f"{emoji} "