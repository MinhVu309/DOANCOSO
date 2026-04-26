import torch
from torch.utils.data import Dataset

class MultiTaskDataset(Dataset):
    def __init__(self, texts, emotion_labels, hate_labels, tokenizer, max_len):
        self.texts = texts
        self.emotion_labels = emotion_labels
        self.hate_labels = hate_labels
        self.tokenizer = tokenizer  
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors=None 
        )

        return {
            'input_ids': torch.tensor(encoding['input_ids'], dtype=torch.long),
            'attention_mask': torch.tensor(encoding['attention_mask'], dtype=torch.long),
            'emotion_labels': torch.tensor(self.emotion_labels[idx], dtype=torch.long),
            'hate_labels': torch.tensor(self.hate_labels[idx], dtype=torch.long)
        }