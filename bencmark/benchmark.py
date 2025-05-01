import os
from dotenv import load_dotenv
from comet_ml import Experiment
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from models.mock_llm.model import MockLLMClassifier
import tempfile

load_dotenv()

class BenchmarkRunner:
    def __init__(self, model, experiment_name="text_classification_benchmark"):
        self.model = model
        self.experiment = Experiment(
            api_key=os.getenv("COMET_API_KEY"),
            project_name=os.getenv("COMET_PROJECT"),
            workspace=os.getenv("COMET_WORKSPACE"),
            auto_output_logging="native",
        )
        # self.experiment.set_name(experiment_name)
        self.experiment.log_parameter("model_name", getattr(self.model, "model_name", "unknown"))

    def load_data(self):
        self.df = pd.DataFrame({
            "text": [
                "I love this product!", "Worst service ever.", "Very happy with the support.",
                "Not worth the money.", "Fantastic experience.", "Terrible response time."
            ],
            "label": ["positive", "negative", "positive", "negative", "positive", "negative"]
        })
        
    def index_to_example(self, index):
        row = self.df.iloc[index]
        return f"Text: '{row['text']}', True: {row['true']}, Pred: {row['pred']}"

    def evaluate(self):
        self.load_data()
        y_true = self.df["label"]
        
        self.df["prediction"] = self.df["label"].apply(self.model.predict)
        self.df["success"] = self.df["label"] == self.df["prediction"]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.df["modle_name"] = self.experiment.name
            self.df.to_csv(f.name, index=False)
            self.experiment.log_asset(file_data=f.name, file_name="predictions.csv", metadata={"description": "Predictions and labels"})
            
        y_pred = self.df["prediction"]
        y_true = self.df["label"]
            
        acc = accuracy_score(y_true, y_pred)
        self.experiment.log_metric("accuracy", acc)
        
        # Get unique sorted labels for consistent ordering
        labels = sorted(self.df['label'].unique().tolist() + self.df['prediction'].unique().tolist())
        labels = sorted(set(labels))

        # Compute confusion matrix
        cm = confusion_matrix(self.df['label'], self.df['prediction'], labels=labels)
        self.experiment.log_confusion_matrix(matrix=cm, labels=labels, index_to_example_function=self.index_to_example)
        
        for i, (text, true, pred, success) in enumerate(zip(self.df["text"], self.df["label"], self.df["prediction"], self.df["success"])):
            self.experiment.log_text(
                f"Example {i}",
                f"Text: {text} | True: {true} | Pred: {pred} | Success: {success}"
            )

        self.experiment.end()

if __name__ == "__main__":
    model = MockLLMClassifier(model_name="mock-gpt-lite-v2")
    runner = BenchmarkRunner(model)
    runner.evaluate()
