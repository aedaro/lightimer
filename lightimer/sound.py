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


def _play_with_pygame(sound_path: str) -> None:
    import pygame

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(_resource_path(sound_path))
    pygame.mixer.music.play()


def play_notification(sound_path: str = SOUND_PATH) -> None:
    """Play the *timesup* notification sound in a background thread."""
    if sys.platform not in {"linux", "win32"}:
        logger.warning("No sound player available for platform %s", sys.platform)
        return
    threading.Thread(target=_play_with_pygame, args=(sound_path,), daemon=True).start()
