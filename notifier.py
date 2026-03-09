from plyer import notification


def notify(player_name):
    notification.notify(
        title="⚔ Düşman Tespit Edildi!",
        message=f"Düşman oyuncu: {player_name}",
        app_name="AlbionAlert",
        timeout=5,
    )
