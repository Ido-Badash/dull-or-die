import pygame
from pathlib import Path
from typing import Tuple
from PIL import Image
from io import BytesIO


def load_sprite(path: str):
    p = Path(path)
    if p.exists():
        return pygame.image.load(path).convert_alpha()
    else:
        print(f"Warning: Sprite not found: {path}")
        return None


def mid_pos(screen_size: Tuple[int, int], rect: pygame.Rect) -> Tuple[int, int]:
    return (
        screen_size[0] // 2 - rect.w // 2,
        screen_size[1] // 2 - rect.h // 2,
    )


def load_gif_from_bytes(byte_data):
    img = Image.open(BytesIO(byte_data))
    frames = []

    try:
        while True:
            frame = img.copy().convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            frames.append(pygame_image)
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return frames
