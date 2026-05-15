import torch
import torch.nn as nn
from transformers import AutoModel


class PhoBERTMultiTask(nn.Module):
    def __init__(self, num_hate_labels=3, num_emotion_labels=28):
        super().__init__()
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base-v2", use_safetensors=True)
        hidden_size = 768

        # Emotion head — khớp đúng checkpoint: Sequential 3 Linear (768→384→256→28)
        # State-dict keys: 0.*, 3.*, 6.*  (GELU+Dropout không có weight → index 1,2 và 4,5)
        self.emotion_head = nn.Sequential(
            nn.Linear(hidden_size, 384),  # index 0
            nn.GELU(),                    # index 1 (no params)
            nn.Dropout(0.4),              # index 2 (no params)
            nn.Linear(384, 256),          # index 3
            nn.GELU(),                    # index 4 (no params)
            nn.Dropout(0.4),              # index 5 (no params)
            nn.Linear(256, num_emotion_labels),  # index 6
        )

        # Hate head — khớp đúng checkpoint: Linear+BatchNorm+ReLU+Dropout+Linear
        # State-dict keys: 0.*, 1.* (BatchNorm), 4.*
        self.hate_head = nn.Sequential(
            nn.Linear(hidden_size, 256),  # index 0
            nn.BatchNorm1d(256),          # index 1
            nn.ReLU(),                    # index 2 (no params)
            nn.Dropout(0.3),              # index 3 (no params)
            nn.Linear(256, num_hate_labels),  # index 4
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.phobert(input_ids=input_ids, attention_mask=attention_mask)

        # Mean pooling
        last_hidden = outputs.last_hidden_state
        mask_exp = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
        pooled = torch.sum(last_hidden * mask_exp, 1) / torch.clamp(mask_exp.sum(1), min=1e-9)

        emo_logits = self.emotion_head(pooled)
        hate_logits = self.hate_head(pooled)
        return emo_logits, hate_logits
