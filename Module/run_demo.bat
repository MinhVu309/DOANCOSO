@echo off
title Chạy Demo Dự Đoán Emotion & Hate Speech
CHCP 65001 > nul

if not exist "venv" (
    echo [LỖI] Chưa có môi trường ảo. Hãy chạy setup_env.bat trước!
    pause
    exit /b
)

echo [*] Đang kích hoạt môi trường và khởi động Model...
call venv\Scripts\activate
python inference.py
pause