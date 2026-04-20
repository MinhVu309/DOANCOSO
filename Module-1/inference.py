import torch
from transformers import AutoTokenizer

from src.models import PhoBERTMultiTask
from src.preprocess import TextCleaner


class EmotionHatePredictor:
    EMOTIONS = ['Anger', 'Disgust', 'Enjoyment', 'Fear', 'Other', 'Sadness', 'Surprise']
    HATE_LABELS = ['Clean', 'Offensive', 'Hate']

    def __init__(self, model_path: str, dict_path: str, device=None):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.cleaner = TextCleaner(dict_path)

        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

        self.model = PhoBERTMultiTask(
            num_emotion_labels=len(self.EMOTIONS),
            num_hate_labels=len(self.HATE_LABELS),
        )
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str) -> dict:
        cleaned_text = self.cleaner.clean(text)

        encoding = self.tokenizer(
            cleaned_text,
            max_length=256,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            emo_logits, hate_logits = self.model(input_ids, attention_mask)

        emo_probs = torch.softmax(emo_logits, dim=-1).squeeze().tolist()
        hate_probs = torch.softmax(hate_logits, dim=-1).squeeze().tolist()

        # Tất cả nhãn, sắp xếp theo confidence giảm dần
        emotion_scores = sorted(
            [{"label": label, "confidence": round(prob, 4)}
             for label, prob in zip(self.EMOTIONS, emo_probs)],
            key=lambda x: x["confidence"],
            reverse=True,
        )
        hate_scores = sorted(
            [{"label": label, "confidence": round(prob, 4)}
             for label, prob in zip(self.HATE_LABELS, hate_probs)],
            key=lambda x: x["confidence"],
            reverse=True,
        )

        return {
            "original_text": text,
            "cleaned_text": cleaned_text,
            # Nhãn chính (top-1) — dùng cho filter logic
            "emotion": emotion_scores[0]["label"],
            "emotion_confidence": emotion_scores[0]["confidence"],
            "hate_speech": hate_scores[0]["label"],
            "hate_confidence": hate_scores[0]["confidence"],
            # Toàn bộ nhãn kèm confidence
            "emotion_scores": emotion_scores,
            "hate_scores": hate_scores,
        }


if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(__file__)

    predictor = EmotionHatePredictor(
        model_path=os.path.join(BASE_DIR, 'Model', 'best_multitask_model.pth'),
        dict_path=os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx'),
    )

    tests = [
        "Hôm nay tôi cảm thấy rất vui vẻ!",
        "Dmm làm ăn như thế à :)))",
        "Tôi không muốn sống nữa, mọi thứ quá tệ",
    ]
    for t in tests:
        print(predictor.predict(t))
