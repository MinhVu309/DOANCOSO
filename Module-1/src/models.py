import torch.nn as nn
from transformers import AutoModel
import torch

class PhoBERTMultiTask(nn.Module):
    def __init__(self, num_emotion_labels, num_hate_labels):
        super(PhoBERTMultiTask, self).__init__()
        # Backbone PhoBERT
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base", use_safetensors=True)
        
        hidden_size = self.phobert.config.hidden_size # Thường là 768
        intermediate_size = 256 # Kích thước lớp ẩn trung gian

        # --- Nâng cấp Head cho Emotion ---
        self.emotion_head = nn.Sequential(
            nn.Linear(hidden_size, intermediate_size),
            nn.BatchNorm1d(intermediate_size), # Giúp mô hình hội tụ nhanh và ổn định
            nn.ReLU(),
            nn.Dropout(0.3), # Giảm hiện tượng học vẹt (overfitting)
            nn.Linear(intermediate_size, num_emotion_labels)
        )

        # --- Nâng cấp Head cho Hate Speech ---
        self.hate_head = nn.Sequential(
            nn.Linear(hidden_size, intermediate_size),
            nn.BatchNorm1d(intermediate_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(intermediate_size, num_hate_labels)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.phobert(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state # [batch, seq_len, 768]

        # --- Kỹ thuật Mean Pooling ---
        # Tạo mask để không tính trung bình trên các token Padding
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        mean_pooled = sum_embeddings / sum_mask

        emo_logits = self.emotion_head(mean_pooled)
        hate_logits = self.hate_head(mean_pooled)

        return emo_logits, hate_logits