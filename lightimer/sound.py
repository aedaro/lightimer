"""Platform-aware notification sound playback."""

from __future__ import annotations

import logging
import sys
import threading

from lightimer.config import SOUND_PATH
from lightimer.utils import resource_path

logger = logging.getLogger(__name__)


def _play_with_pygame(sound_path: str) -> None:
    import pygame

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(resource_path(sound_path))
    pygame.mixer.music.play()


def play_notification(sound_path: str = SOUND_PATH) -> None:
    """Play the *timesup* notification sound in a background thread."""
    if sys.platform not in {"linux", "win32"}:
        logger.warning("No sound player available for platform %s", sys.platform)
        return
    threading.Thread(target=_play_with_pygame, args=(sound_path,), daemon=True).start()
