import numpy as np

# Tarama aralığı (saniye)
SCAN_INTERVAL = 0.5

# Düşman ismi kırmızı renk HSV aralığı
# Albion Online'da düşman isimleri kırmızı görünür
ENEMY_RED_LOWER = np.array([0, 100, 100])
ENEMY_RED_UPPER = np.array([10, 255, 255])
ENEMY_RED_LOWER2 = np.array([160, 100, 100])
ENEMY_RED_UPPER2 = np.array([180, 255, 255])

# Aynı düşman için tekrar bildirim bekleme süresi (saniye)
COOLDOWN_SECONDS = 30

# İzlenecek ekran bölgesi (None = tüm ekran)
# Örnek: {"top": 0, "left": 0, "width": 1920, "height": 1080}
MONITOR_REGION = None

# Minimum metin uzunluğu (gürültüyü filtrele)
MIN_NAME_LENGTH = 3

# Tesseract config
TESSERACT_CONFIG = "--psm 6 --oem 3"
