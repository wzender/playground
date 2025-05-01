import random

class MockLLMClassifier:
    def __init__(self, model_name="mock-llm-v1"):
        self.model_name = model_name
        self.labels = ["positive", "negative"]

    def predict_list(self, texts):
        return [random.choice(self.labels) for _ in texts]
    
    def predict(self, text):
        return random.choice(self.labels)
