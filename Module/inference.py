import os
import json

import numpy as np
import torch
from transformers import AutoTokenizer

from src.models import PhoBERTMultiTask
from src.preprocess import TextCleaner

EMOTION_LABELS = [
    'amusement', 'excitement', 'joy', 'love', 'desire', 'optimism',
    'caring', 'pride', 'admiration', 'gratitude', 'relief', 'approval',
    'realization', 'surprise', 'curiosity', 'confusion', 'fear',
    'nervousness', 'remorse', 'embarrassment', 'disappointment',
    'sadness', 'grief', 'disgust', 'anger', 'annoyance',
    'disapproval', 'neutral',
]

HATE_LABELS = ['Clean', 'Offensive', 'Hate']

NUM_EMOTION_LABELS = len(EMOTION_LABELS)  # 28


class EmotionHatePredictor:

    def __init__(
        self,
        model_path: str,
        dict_path: str,
        threshold_path: str = None,
        device=None,
        default_threshold: float = 0.5,
    ):
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.cleaner = TextCleaner(dict_path)

        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
        self.max_len = 192

        self.model = PhoBERTMultiTask(
            num_hate_labels=3,
            num_emotion_labels=NUM_EMOTION_LABELS,
        )
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        # Per-label threshold — load từ JSON nếu có
        self.thresholds = np.full(NUM_EMOTION_LABELS, default_threshold)
        if threshold_path and os.path.exists(threshold_path):
            with open(threshold_path, 'r', encoding='utf-8') as f:
                thresh_data = json.load(f)
            if isinstance(thresh_data, dict):
                for i, label in enumerate(EMOTION_LABELS):
                    if label in thresh_data:
                        self.thresholds[i] = thresh_data[label]
            elif isinstance(thresh_data, list):
                self.thresholds = np.array(thresh_data[:NUM_EMOTION_LABELS])

    def predict(self, text: str) -> dict:
        cleaned = self.cleaner.clean(text)

        encoding = self.tokenizer(
            cleaned,
            max_length=self.max_len,
            padding=True,
            truncation=True,
            return_tensors='pt',
        )
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            emo_logits, hate_logits = self.model(input_ids, attention_mask)

        # Emotion: sigmoid → so sánh với per-label threshold
        emo_probs = torch.sigmoid(emo_logits).squeeze().cpu().numpy()

        predicted_emotions = [
            EMOTION_LABELS[j]
            for j in range(NUM_EMOTION_LABELS)
            if emo_probs[j] > self.thresholds[j]
        ]
        # Fallback: nếu không nhãn nào vượt threshold → lấy nhãn có prob cao nhất
        if not predicted_emotions:
            top_idx = int(np.argmax(emo_probs))
            predicted_emotions = [EMOTION_LABELS[top_idx]]

        # Tất cả 28 điểm, sắp xếp giảm dần — dùng bởi backend để lấy primary score
        emotion_scores = sorted(
            [
                {"label": EMOTION_LABELS[j], "confidence": round(float(emo_probs[j]), 4)}
                for j in range(NUM_EMOTION_LABELS)
            ],
            key=lambda x: x["confidence"],
            reverse=True,
        )

        # Hate: softmax → argmax
        hate_probs = torch.softmax(hate_logits, dim=-1).squeeze().cpu().numpy()
        hate_idx = int(np.argmax(hate_probs))
        hate_label = HATE_LABELS[hate_idx]
        hate_score = round(float(hate_probs[hate_idx]), 4)

        return {
            "original_text": text,
            "cleaned_text": cleaned,
            "emotions": predicted_emotions,
            "emotion_scores": emotion_scores,
            # backward-compat aliases cho backend hiện tại
            "hate": hate_label,
            "hate_speech": hate_label,
            "hate_score": hate_score,
            "hate_confidence": hate_score,
        }


if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(__file__)
    predictor = EmotionHatePredictor(
        model_path=os.path.join(BASE_DIR, 'Model', 'best_multitask_model.pth'),
        threshold_path=os.path.join(BASE_DIR, 'Model', 'emotion_thresholds.json'),
        dict_path=os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx'),
    )

    tests = [
        "Hôm nay tôi cảm thấy rất vui vẻ!",
        "Buồn quá, không biết phải làm sao nữa huhu",
        "Tao ghét mày, đừng bao giờ liên lạc với tao nữa.",
        "Tôi lo lắng không biết kết quả thi thế nào.",
    ]
    for t in tests:
        r = predictor.predict(t)
        print(f"\n📝 {r['original_text']}")
        print(f"   😊 Emotions:   {r['emotions']}")
        print(f"   🚨 Hate:       {r['hate']} (score={r['hate_score']})")
