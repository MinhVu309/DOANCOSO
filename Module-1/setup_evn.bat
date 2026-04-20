@echo off
setlocal
CHCP 65001 > nul
title Thiết lập môi trường MentalHealth AI - Project

echo ======================================================
echo    BẮT ĐẦU THIẾT LẬP MÔI TRƯỜNG CHO DỰ ÁN (VER 2.0)
echo ======================================================

:: 1. Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Không tìm thấy Python! Vũ hãy cài đặt Python 3.8+ và add vào PATH nhé.
    pause
    exit /b
)

:: 2. Tạo môi trường ảo venv nếu chưa có
if not exist "venv" (
    echo [*] Đang tạo môi trường ảo venv...
    python -m venv venv
    echo [OK] Đã tạo xong venv.
) else (
    echo [!] Môi trường venv đã tồn tại, bỏ qua bước tạo mới.
)

:: 3. Kích hoạt môi trường và nâng cấp pip
echo [*] Đang kích hoạt venv và nâng cấp pip...
call venv\Scripts\activate
python -m pip install --upgrade pip

:: 4. Cài đặt các thư viện từ requirements.txt
if exist "requirements.txt" (
    echo [*] Đang cài đặt thư viện từ requirements.txt...
    pip install -r requirements.txt
    echo [OK] Cài đặt thư viện hoàn tất.
) else (
    echo [CẢNH BÁO] Không tìm thấy file requirements.txt!
)

echo ======================================================
echo    THIẾT LẬP HOÀN TẤT!
echo    Vũ có thể chạy lệnh: call venv\Scripts\activate 
echo    Sau đó chạy: python inference.py để test model.
echo ======================================================
pause