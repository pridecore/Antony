### core/state.py
class State:
    def __init__(self):
        self.mood = "спокійний"
        self.last_intent = None

    def update_state(self, intent):
        self.last_intent = intent
        if intent == "greeting":
            self.mood = "дружній"
        elif intent == "exit":
            self.mood = "нейтральний"
        elif intent == "unknown":
            self.mood = "збентежений"
        else:
            self.mood = "зосереджений"

    def get_state(self):
        return {"mood": self.mood, "last_intent": self.last_intent}

