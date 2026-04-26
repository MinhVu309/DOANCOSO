import pickle
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

from src.preprocess import TextCleaner


class MentalHealthMultiLabelClassifier(nn.Module):
    def __init__(self, num_labels: int, dropout: float = 0.3):
        super().__init__()
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base")
        hidden_size = self.phobert.config.hidden_size
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, num_labels),
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.phobert(input_ids=input_ids, attention_mask=attention_mask)
        mask = attention_mask.unsqueeze(-1).expand(outputs.last_hidden_state.size()).float()
        pooled = torch.sum(outputs.last_hidden_state * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)
        return self.classifier(pooled)


class MentalHealthPredictor:
    def __init__(self, model_path: str, label_path: str, dict_path: str, device=None):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.cleaner = TextCleaner(dict_path)

        with open(label_path, 'rb') as f:
            self.label_names = pickle.load(f)

        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

        self.model = MentalHealthMultiLabelClassifier(num_labels=len(self.label_names))
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str, top_k: int = 5) -> dict:
        cleaned = self.cleaner.clean(text)
        encoding = self.tokenizer(
            cleaned,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)
            probs = torch.sigmoid(logits).cpu().numpy()[0]

        all_conditions = sorted(
            [{"label": label, "confidence": round(float(prob), 4)}
             for label, prob in zip(self.label_names, probs)],
            key=lambda x: x["confidence"],
            reverse=True,
        )

        top = all_conditions[:top_k]
        return {
            "condition": top[0]["label"],
            "confidence": top[0]["confidence"],
            "severity": None,
            "conditions": top,
        }


if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(__file__)

    predictor = MentalHealthPredictor(
        model_path=os.path.join(BASE_DIR, 'Model', 'best_mental_health_multilabel.pth'),
        label_path=os.path.join(BASE_DIR, 'Model', 'label_names.pkl'),
        dict_path=os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx'),
    )

    tests = [
        "Tôi cảm thấy buồn bã, mất ngủ, không muốn gặp ai, nghĩ đến cái chết.",
        "Sợ đi thang máy, mỗi lần thấy nhện là hoảng hốt, tay run.",
        "Hay quên, không nhận ra người thân, lú lẫn.",
    ]
    for t in tests:
        result = predictor.predict(t)
        print(f"\nText: {t[:60]}...")
        print(f"Top condition: {result['condition']} ({result['confidence']:.4f})")
        print("All top-5:", [(c['label'], c['confidence']) for c in result['conditions']])
