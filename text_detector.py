import os
import sys
import cv2
import pytesseract
import re
from config import (
    ENEMY_RED_LOWER, ENEMY_RED_UPPER,
    ENEMY_RED_LOWER2, ENEMY_RED_UPPER2,
    MIN_NAME_LENGTH, TESSERACT_CONFIG,
)


def _get_tesseract_path():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    bundled = os.path.join(base, "tesseract", "tesseract.exe")
    if os.path.exists(bundled):
        return bundled
    return None


_tess_path = _get_tesseract_path()
if _tess_path:
    pytesseract.pytesseract.tesseract_cmd = _tess_path


def filter_red_text(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, ENEMY_RED_LOWER, ENEMY_RED_UPPER)
    mask2 = cv2.inRange(hsv, ENEMY_RED_LOWER2, ENEMY_RED_UPPER2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Gürültü temizleme
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask


def detect_names(image):
    mask = filter_red_text(image)

    # Konturları bul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    names = set()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 30 or h < 8 or w > 400 or h > 50:
            continue

        # Bölgeyi kırp ve OCR uygula
        roi = mask[y:y + h, x:x + w]
        # Beyaz arka plan üzerinde siyah metin yap (OCR doğruluğu için)
        roi_inverted = cv2.bitwise_not(roi)

        # Padding ekle
        padded = cv2.copyMakeBorder(roi_inverted, 10, 10, 10, 10,
                                     cv2.BORDER_CONSTANT, value=255)

        text = pytesseract.image_to_string(padded, config=TESSERACT_CONFIG).strip()

        # Temizle: sadece alfanümerik ve boşluk
        text = re.sub(r'[^a-zA-Z0-9\s_\-]', '', text).strip()

        if len(text) >= MIN_NAME_LENGTH:
            names.add(text)

    return names
