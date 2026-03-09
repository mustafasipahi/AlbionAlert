@echo off
echo ========================================
echo   AlbionAlert - Windows Build Script
echo ========================================

echo [1/3] Bagimliliklar yukleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: pip install basarisiz. Python kurulu mu?
    pause
    exit /b 1
)

echo [2/3] EXE olusturuluyor...
pyinstaller --onedir --name AlbionAlert --console --noconfirm main.py
if errorlevel 1 (
    echo HATA: PyInstaller basarisiz.
    pause
    exit /b 1
)

echo [3/3] Tesseract kopyalaniyor...
if exist "C:\Program Files\Tesseract-OCR" (
    xcopy /E /I /Y "C:\Program Files\Tesseract-OCR" "dist\AlbionAlert\tesseract"
    echo Tesseract basariyla eklendi.
) else (
    echo UYARI: Tesseract bulunamadi!
    echo Lutfen https://github.com/UB-Mannheim/tesseract/wiki adresinden kurun.
    echo Kurulduktan sonra bu scripti tekrar calistirin.
    pause
    exit /b 1
)

echo ========================================
echo   Build tamamlandi!
echo   dist\AlbionAlert\AlbionAlert.exe
echo ========================================
pause
