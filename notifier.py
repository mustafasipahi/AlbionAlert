import sys
import threading
from plyer import notification


def _play_alert_sound():
    if sys.platform == "win32":
        import winsound
        # 3 kez bip sesi - dikkat çekici
        for _ in range(3):
            winsound.Beep(1000, 300)
            winsound.Beep(1500, 300)


def notify(player_name):
    # Windows bildirim (sağ altta popup)
    notification.notify(
        title="DUSMAN TESPIT EDILDI!",
        message=f"Dusman oyuncu: {player_name}",
        app_name="AlbionAlert",
        timeout=10,
    )

    # Ses bildirimini ayrı thread'de çal (ana döngüyü bloklamasın)
    sound_thread = threading.Thread(target=_play_alert_sound, daemon=True)
    sound_thread.start()
