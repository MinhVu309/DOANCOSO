import numpy as np
import torch
from sklearn.utils.class_weight import compute_class_weight

def get_emotion_weights(labels):
    """
    labels: List hoặc Array chứa nhãn của toàn bộ tập Train (VD: [0, 1, 2, 0, 6...])
    """
    # Tính toán trọng số bằng sklearn để đảm bảo chuẩn thuật toán
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    
    # Chuyển sang Tensor để dùng với PyTorch Loss
    weights_tensor = torch.tensor(class_weights, dtype=torch.float)
    return weights_tensor

# Giả sử 'train_labels' là danh sách nhãn Emotion trong tập dữ liệu của 
# emotion_weights = get_emotion_weights(train_labels).to(device)