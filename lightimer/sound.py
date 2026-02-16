"""Platform-aware notification sound playback."""

from __future__ import annotations

import logging
import os
import sys
import threading

from lightimer.config import SOUND_PATH

logger = logging.getLogger(__name__)


def _resource_path(relative_path: str) -> str:
    """Resolve *relative_path* inside a PyInstaller bundle or the project root."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def _play_linux(sound_path: str) -> None:
    from pydub import AudioSegment
    from pydub.playback import play

    sound = AudioSegment.from_wav(_resource_path(sound_path))
    play(sound)


def _play_win(sound_path: str) -> None:
    import winsound  # type: ignore[import-not-found]

    winsound.PlaySound(_resource_path(sound_path), winsound.SND_FILENAME)


_PLATFORM_PLAYER: dict[str, callable] = {
    "linux": _play_linux,
    "win32": _play_win,
}


def play_notification(sound_path: str = SOUND_PATH) -> None:
    """Play the *timesup* notification sound in a background thread."""
    player = _PLATFORM_PLAYER.get(sys.platform)
    if player is None:
        logger.warning("No sound player available for platform %s", sys.platform)
        return
    threading.Thread(target=player, args=(sound_path,), daemon=True).start()
