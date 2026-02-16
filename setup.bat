@echo off
echo ========================================
echo  Football Match Predictor - Quick Start
echo ========================================
echo.

echo Step 1: Installing Python packages...
pip install -r requirements.txt --break-system-packages
echo.

echo Step 2: Testing the predictor...
python predictor.py
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start API: python api.py
echo 2. In another terminal, go to flutter_app folder
echo 3. Run: flutter pub get
echo 4. Run: flutter run
echo.
pause
