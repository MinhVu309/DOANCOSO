# AI Pipeline — NhatKi

Tài liệu này mô tả luồng xử lý của 2 model AI, các API endpoint, schema request/response, và cơ chế tích lũy dự đoán theo thời gian.

---

## Tổng quan luồng

```
Người dùng viết nhật ký
        │
        ▼
Backend :8000  POST /api/entries/{id}/analyze
        │
        ▼  HTTP (httpx)
AI Service :8001  POST /api/analyze
        │
        ├─ Module-1: EmotionHatePredictor
        │       ├── Tiền xử lý: TextCleaner (teencode dict, regex)
        │       ├── PhoBERT tokenize (max_length=256)
        │       ├── PhoBERTMultiTask → softmax
        │       ├── Emotion (7 nhãn) + Hate Speech (3 nhãn)
        │       └── Lọc triggered_emotions: confidence > 0.3 & ngoài {Enjoyment, Other}
        │
        └─ Module-2: MentalHealthPredictor  (chỉ chạy khi needs_assessment=True)
                ├── Tiền xử lý: TextCleaner
                ├── PhoBERT tokenize (max_length=128)
                ├── MentalHealthMultiLabelClassifier → sigmoid
                └── Top-5 conditions từ 58 nhãn sức khỏe tâm thần
        │
        ▼
Backend lưu kết quả vào analysis_results
        │
        ▼
aggregate_user_conditions() — tích lũy conditions 30 ngày
        │
        ▼
user_conditions: confirmed=True khi xuất hiện >= 3 lần
```

---

## Module-1 — Emotion & Hate Speech Detection

### Model

| Thông số | Giá trị |
|---|---|
| Base model | `vinai/phobert-base` |
| Kiến trúc | PhoBERTMultiTask — 2 classification head độc lập |
| Pooling | Mean pooling có mask |
| File trọng số | `Module/Model/best_multitask_model.pth` (~517 MB) |
| Tokenizer max_length | 256 |

### Nhãn đầu ra

**Emotion (7 nhãn):** `Anger · Disgust · Enjoyment · Fear · Other · Sadness · Surprise`

**Hate Speech (3 nhãn):** `Clean · Offensive · Hate`

### Logic kích hoạt Module-2

```python
SAFE_EMOTIONS     = {'Enjoyment', 'Other'}
SAFE_HATE_LABEL   = 'Clean'
EMOTION_THRESHOLD = 0.3

# triggered_emotions = nhãn cảm xúc có confidence > 0.3, ngoài SAFE_EMOTIONS
triggered_emotions = [
    label for label, conf in emotion_scores
    if conf > EMOTION_THRESHOLD and label not in SAFE_EMOTIONS
]

needs_assessment = bool(triggered_emotions) or hate_speech != 'Clean'
```

Ví dụ:
- `Sadness=0.82, Fear=0.41, Enjoyment=0.20` → `triggered_emotions = ["Sadness", "Fear"]` → gọi Module-2
- `Enjoyment=0.75, Other=0.15` → `triggered_emotions = []`, `hate="Clean"` → **không** gọi Module-2

---

## Module-2 — Mental Health Assessment

### Model

| Thông số | Giá trị |
|---|---|
| Base model | `vinai/phobert-base` |
| Kiến trúc | MentalHealthMultiLabelClassifier (Dropout → Linear → ReLU → Dropout → Linear) |
| Output activation | Sigmoid (multi-label) |
| Số nhãn | 58 tình trạng sức khỏe tâm thần |
| File trọng số | `Module/Model/best_mental_health_multilabel.pth` (~516 MB) |
| Label map | `Module/Model/label_names.pkl` |
| Tokenizer max_length | 128 |

### Nhãn đầu ra (ví dụ)

Rối loạn trầm cảm · Rối loạn lo âu · Mất ngủ · Căng thẳng Stress · Rối loạn lưỡng cực · PTSD · OCD · ADHD · Tâm thần phân liệt · Bệnh Alzheimer · Bệnh Parkinson · *(và 47 nhãn khác)*

---

## API Endpoints — AI Service (:8001)

### POST /api/analyze

Endpoint chính, nhận text từ backend, chạy Module-1 và tự động gọi Module-2 nếu cần.

**Request**
```json
{
  "text": "Tôi cảm thấy rất buồn, không muốn làm gì cả"
}
```

**Response**
```json
{
  "original_text": "Tôi cảm thấy rất buồn, không muốn làm gì cả",
  "cleaned_text": "Tôi cảm thấy rất buồn không muốn làm gì cả",
  "emotion": "Sadness",
  "emotion_confidence": 0.82,
  "hate_speech": "Clean",
  "hate_confidence": 0.91,
  "emotion_scores": [
    { "label": "Sadness",   "confidence": 0.82 },
    { "label": "Fear",      "confidence": 0.41 },
    { "label": "Disgust",   "confidence": 0.22 },
    { "label": "Anger",     "confidence": 0.18 },
    { "label": "Other",     "confidence": 0.12 },
    { "label": "Surprise",  "confidence": 0.08 },
    { "label": "Enjoyment", "confidence": 0.05 }
  ],
  "hate_scores": [
    { "label": "Clean",     "confidence": 0.91 },
    { "label": "Offensive", "confidence": 0.06 },
    { "label": "Hate",      "confidence": 0.03 }
  ],
  "triggered_emotions": ["Sadness", "Fear"],
  "needs_assessment": true,
  "assessment": {
    "condition": "Rối loạn trầm cảm",
    "confidence": 0.87,
    "severity": null,
    "conditions": [
      { "label": "Rối loạn trầm cảm", "confidence": 0.87 },
      { "label": "Mất ngủ",           "confidence": 0.65 },
      { "label": "Rối loạn lo âu",    "confidence": 0.58 },
      { "label": "Căng thẳng Stress", "confidence": 0.44 },
      { "label": "PTSD",              "confidence": 0.31 }
    ]
  }
}
```

> Khi `needs_assessment=false`, trường `assessment` sẽ là `null` và Module-2 không chạy.

---

### POST /api/assess

Gọi Module-2 trực tiếp, bỏ qua bước lọc của Module-1. Dùng để test hoặc gọi nội bộ.

**Request**
```json
{
  "text": "Tôi cảm thấy rất buồn, không muốn làm gì cả",
  "emotions": ["Sadness", "Fear"],
  "hate_speech": "Clean"
}
```

**Response**
```json
{
  "condition": "Rối loạn trầm cảm",
  "confidence": 0.87,
  "severity": null,
  "conditions": [
    { "label": "Rối loạn trầm cảm", "confidence": 0.87 },
    { "label": "Mất ngủ",           "confidence": 0.65 },
    { "label": "Rối loạn lo âu",    "confidence": 0.58 },
    { "label": "Căng thẳng Stress", "confidence": 0.44 },
    { "label": "PTSD",              "confidence": 0.31 }
  ]
}
```

---

## API Endpoints — Backend (:8000)

### POST /api/entries/{id}/analyze

Trigger phân tích AI cho một bài nhật ký. Backend gọi `/api/analyze` trên AI Service rồi lưu kết quả.

**Response** — trả về `AnalysisResult`:
```json
{
  "emotion_label": "Sadness",
  "emotion_score": 0.82,
  "hate_label": "Clean",
  "needs_assessment": true,
  "mood_label_vi": "Buồn bã",
  "mood_color": "#7986CB",
  "ai_summary": "Bài viết thể hiện cảm xúc buồn bã...",
  "ai_tags": ["tâm trạng", "cảm xúc"],
  "condition": "Rối loạn trầm cảm",
  "condition_confidence": 0.87,
  "conditions": [
    { "label": "Rối loạn trầm cảm", "confidence": 0.87 },
    { "label": "Mất ngủ",           "confidence": 0.65 }
  ],
  "analyzed_at": "2026-04-26T10:30:00Z"
}
```

### GET /api/trends/mental-health

Trả về tình trạng tâm thần được tích lũy từ nhiều bài viết của user trong 30 ngày qua.

**Response**
```json
{
  "window_days": 30,
  "min_occurrences": 3,
  "conditions": [
    {
      "condition_name": "Rối loạn trầm cảm",
      "occurrence_count": 5,
      "avg_confidence": 0.75,
      "first_seen_at": "2026-03-26T08:00:00Z",
      "last_seen_at": "2026-04-25T21:00:00Z",
      "confirmed": true
    },
    {
      "condition_name": "Mất ngủ",
      "occurrence_count": 2,
      "avg_confidence": 0.58,
      "first_seen_at": "2026-04-10T09:00:00Z",
      "last_seen_at": "2026-04-20T22:00:00Z",
      "confirmed": false
    }
  ]
}
```

> `confirmed=true` khi `occurrence_count >= 3` trong cửa sổ 30 ngày.
> `confirmed=false` là đang theo dõi, chưa đủ bằng chứng.

---

## Cơ chế tích lũy conditions

Sau mỗi lần `POST /api/entries/{id}/analyze` thành công, backend tự động chạy `aggregate_user_conditions()`:

```
Bài viết 1  →  conditions: [Trầm cảm 0.87, Mất ngủ 0.65, ...]
Bài viết 2  →  conditions: [Trầm cảm 0.72, Lo âu 0.55, ...]
Bài viết 3  →  conditions: [Trầm cảm 0.91, Mất ngủ 0.60, ...]
                                    ↓
              user_conditions: Trầm cảm — 3 lần — TB 83% — confirmed ✓
                               Mất ngủ  — 2 lần — TB 63% — đang theo dõi
                               Lo âu    — 1 lần — TB 55% — đang theo dõi
```

**Ngưỡng lọc:**

| Tham số | Giá trị | Ý nghĩa |
|---|---|---|
| `CONDITION_WINDOW_DAYS` | 30 | Chỉ xét bài viết trong 30 ngày gần nhất |
| `CONDITION_MIN_OCCURRENCES` | 3 | Cần >= 3 lần để `confirmed=True` |
| `CONDITION_MIN_CONFIDENCE` | 0.3 | Bỏ qua condition có confidence < 30% |

---

## Xử lý lỗi

| Tình huống | Hành vi |
|---|---|
| Module-2 lỗi / chưa khởi động | `assessment=null`, Module-1 vẫn trả kết quả bình thường |
| AI Service (:8001) không phản hồi | Backend lưu `AnalysisResult` rỗng, entry vẫn được tạo |
| Model file không tồn tại | Server crash khi startup — cần đặt đủ file `.pth` vào `Module/Model/` |

---

## Lưu ý kỹ thuật

- Cả 2 model được **pre-load khi server khởi động** (`lifespan` event), lần đầu mất 30–60 giây
- Inference PyTorch chạy trong **thread pool** (`run_in_executor`) để không block async event loop
- Model singleton được cache bằng `lru_cache(maxsize=1)` — chỉ load một lần duy nhất
- Module-2 hiện **không dùng** `emotions` và `hate_speech` trong quá trình inference — chỉ dùng `text`. Các tham số này được truyền vào để chuẩn bị cho phiên bản sau
