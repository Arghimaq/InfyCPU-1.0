import json
from collections import deque
import pygame

with open("settings.json", "r") as f:
    _settings = json.load(f)
Window_Width = int(_settings.get("window_width", 720))
Window_Length = int(_settings.get("window_length", 600))
Screen_Width = int(_settings.get("screen_width", 48))
Screen_Length = int(_settings.get("screen_length", 40))
Width_Scale = Window_Width / Screen_Width
Length_Scale = Window_Length / Screen_Length
Window_Size = (Window_Width, Window_Length)
_RENDER_EVERY =  int(_settings.get("render_every")) # CPU instructions between visual refreshes

Color_palette = {
    0: (0, 0, 0),
    1: (235, 235, 235),
    2: (255, 70, 70),
    3: (250, 220, 70),
    4: (70, 230, 110),
    5: (60, 220, 235),
    6: (80, 130, 255),
    7: (205, 90, 235),
}

screen = None
_lowres = None
_pending_keys = deque(maxlen=64)
_quit_requested = False
_update_calls = 0



def load_data():
    """Compatibility function expected by Processor.py."""
    global Window_Width, Window_Length, Screen_Width, Screen_Length
    global Width_Scale, Length_Scale, Window_Size
    with open("settings.json", "r") as f:
        cfg = json.load(f)
    Window_Width = int(cfg.get("window_width", 720))
    Window_Length = int(cfg.get("window_length", 600))
    Screen_Width = int(cfg.get("screen_width", 48))
    Screen_Length = int(cfg.get("screen_length", 40))
    Width_Scale = Window_Width / Screen_Width
    Length_Scale = Window_Length / Screen_Length
    Window_Size = (Window_Width, Window_Length)


def initialize():
    global screen, _lowres
    pygame.init()
    screen = pygame.display.set_mode(Window_Size)
    pygame.display.set_caption("InfyCPU-2 — Tetris")
    _lowres = pygame.Surface((Screen_Width, Screen_Length))
    _lowres.fill(Color_palette[0])


def draw_screen(VRAM):
    if _lowres is None:
        return
    # Draw at logical resolution, then scale once rather than drawing one
    # window-sized rectangle per pixel on every CPU cycle.
    for i, value in enumerate(VRAM[:Screen_Width * Screen_Length]):
        x = i % Screen_Width
        y = i // Screen_Width
        _lowres.set_at((x, y), Color_palette.get(value, Color_palette[0]))
    scaled = pygame.transform.scale(_lowres, Window_Size)
    screen.blit(scaled, (0, 0))


def update(VRAM):
    global _update_calls
    _update_calls += 1
    if _update_calls % _RENDER_EVERY:
        return
    draw_screen(VRAM)
    pygame.display.flip()


def check_quit():
    global _quit_requested
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _quit_requested = True
        elif event.type == pygame.KEYDOWN:
            _pending_keys.append(pygame.key.name(event.key))
    return not _quit_requested


def listen():
    global _quit_requested
    if _pending_keys:
        return _pending_keys.popleft()
    # Also poll here so this works if used outside the standard CPU cycle.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _quit_requested = True
        elif event.type == pygame.KEYDOWN:
            _pending_keys.append(pygame.key.name(event.key))
    if _pending_keys:
        return _pending_keys.popleft()
    return False


def blitter(x, y):
    return y * Screen_Width + x


def listen():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			return pygame.key.name(event.key)
