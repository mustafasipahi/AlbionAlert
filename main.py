import time
import sys
import traceback
from screen_capture import capture_screen
from text_detector import detect_names
from notifier import notify
from config import SCAN_INTERVAL, COOLDOWN_SECONDS, MONITOR_REGION


def main():
    print("=" * 50)
    print("  AlbionAlert - Dusman Algilama Sistemi")
    print("=" * 50)
    print(f"  Tarama araligi: {SCAN_INTERVAL}s")
    print(f"  Cooldown: {COOLDOWN_SECONDS}s")
    print("  Durdurmak icin Ctrl+C")
    print("=" * 50)
    print()

    known_enemies = {}
    scan_count = 0

    try:
        while True:
            image = capture_screen(MONITOR_REGION)
            names = detect_names(image)
            now = time.time()
            scan_count += 1

            # Her 10 taramada durum göster
            if scan_count % 10 == 0:
                print(f"  [Tarama #{scan_count}] Aktif izleme devam ediyor...")

            for name in names:
                last_seen = known_enemies.get(name, 0)
                if now - last_seen > COOLDOWN_SECONDS:
                    print(f"\n  >>> DUSMAN TESPIT EDILDI: {name} <<<\n")
                    notify(name)
                    known_enemies[name] = now

            expired = [k for k, v in known_enemies.items() if now - v > 300]
            for k in expired:
                del known_enemies[k]

            time.sleep(SCAN_INTERVAL)

    except KeyboardInterrupt:
        print("\nAlbionAlert kapatildi.")

    except Exception:
        print("\n[HATA] Bir sorun olustu:")
        traceback.print_exc()
        print("\nKapatmak icin bir tusa basin...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        print("\nKapatmak icin bir tusa basin...")
        input()
