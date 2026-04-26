# Mental Health & Hate Speech Detection Model (Ver 2.0)

## 📊 Thông tin mô hình
- **Base Model:** PhoBERT-base (VinAI)
- **Architecture:** Multi-task Learning (Emotion Recognition & Hate Speech Detection)
- **Best Accuracy (Avg):** **71.46%**
- **Trạng thái:** Đã tối ưu hóa hàm Clean để giữ nguyên sắc thái từ lóng và icon.

## 📁 Cấu trúc thư mục
- `models/`: Chứa file trọng số `best_model.pt`.
- `data/`: Chứa file từ điển `Xử lý teencode.xlsx` (Ver 2 - Chỉ chứa từ viết tắt).
- `src/`: Chứa mã nguồn xử lý tiền xử lý (`preprocess.py`) và kiến trúc mô hình.
- `inference.py`: File chạy demo dự đoán.

## 🛠 Cách thiết lập nhanh
Để tiết kiệm thời gian, đã viết sẵn script tự động:
## LƯU Ý: thư viện này chỉ hoạt động ở Py 3.12 nên hãy chuyển về 3.12 trước khi chạy nhé
1. Click đúp vào file `setup_env.bat`. Script sẽ tự động:
   - Tạo môi trường ảo `venv`. 
   - Cài đặt toàn bộ thư viện cần thiết (`torch`, `transformers`, `emoji`,...). 
2. Sau khi cài xong, click đúp file `run_demo.bat` để kiểm tra kết quả dự đoán của model 71%.
