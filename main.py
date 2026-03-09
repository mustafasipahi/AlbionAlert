import time
import sys
from screen_capture import capture_screen
from text_detector import detect_names
from notifier import notify
from config import SCAN_INTERVAL, COOLDOWN_SECONDS, MONITOR_REGION


def main():
    print("=" * 50)
    print("  AlbionAlert - Düşman Algılama Sistemi")
    print("=" * 50)
    print(f"  Tarama aralığı: {SCAN_INTERVAL}s")
    print(f"  Cooldown: {COOLDOWN_SECONDS}s")
    print("  Durdurmak için Ctrl+C")
    print("=" * 50)

    # İsim -> son bildirim zamanı
    known_enemies = {}

    try:
        while True:
            image = capture_screen(MONITOR_REGION)
            names = detect_names(image)
            now = time.time()

            for name in names:
                last_seen = known_enemies.get(name, 0)
                if now - last_seen > COOLDOWN_SECONDS:
                    print(f"[!] Düşman tespit edildi: {name}")
                    notify(name)
                    known_enemies[name] = now

            # Eski kayıtları temizle (5 dakikadan eski)
            expired = [k for k, v in known_enemies.items() if now - v > 300]
            for k in expired:
                del known_enemies[k]

            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\nAlbionAlert kapatıldı.")
        sys.exit(0)


if __name__ == "__main__":
    main()
