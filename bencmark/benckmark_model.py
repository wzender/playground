import os
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from comet_ml import Experiment
import random

# 🔧 CONFIGURATION
COMET_API_KEY = os.getenv("COMET_API_KEY")
PROJECT_NAME = "text-classification-benchmark"
WORKSPACE = "wzender"

# 🔁 Comet experiment
experiment = Experiment(
    api_key=COMET_API_KEY,
    project_name=PROJECT_NAME,
    workspace=WORKSPACE,
    auto_output_logging="native"
)

# 📄 Simulated test dataset
data = {
    "text": [
        "I love this product!", "Worst service ever.", "Very happy with the support.",
        "Not worth the money.", "Fantastic experience.", "Terrible response time."
    ],
    "label": ["positive", "negative", "positive", "negative", "positive", "negative"]
}
df = pd.DataFrame(data)

# 🧠 Mock model (randomly guesses positive/negative)
def mock_model_predict(texts):
    return [random.choice(["positive", "negative"]) for _ in texts]

# 🧪 Benchmark
y_true = df["label"]
y_pred = mock_model_predict(df["text"])

acc = accuracy_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred, labels=["positive", "negative"])

# 📈 Log to Comet
experiment.log_parameter("dataset_size", len(df))
experiment.log_metric("accuracy", acc)
experiment.log_confusion_matrix(y_true.tolist(), y_pred, labels=["positive", "negative"])

# 📝 Optional: log predictions
for i, (text, true, pred) in enumerate(zip(df["text"], y_true, y_pred)):
    experiment.log_text(f"Example {i}", f"Text: {text} | True: {true} | Pred: {pred}")

experiment.end()
