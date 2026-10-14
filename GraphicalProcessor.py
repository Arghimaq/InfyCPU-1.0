import json

#Screen Variables

with open("settings.json", 'r') as f:
	settings = json.load(f)

Window_Width = settings.get("window_width")
Window_Length = settings.get("window_length")
Screen_Width = settings.get("screen_width")
Screen_Length = settings.get("screen_length")
Width_Scale = Window_Width / Screen_Width
Length_Scale = Window_Length / Screen_Length

Window_Size = (Window_Width, Window_Length)

def load_data():
	with open("settings.json", 'r') as f:
		settings = json.load(f)

		Window_Width = settings.get("window_width")
		Window_Length = settings.get("window_length")
		Screen_Width = settings.get("screen_width")
		Screen_Length = settings.get("screen_length")
		Width_Scale = Window_Width / Screen_Width
		Length_Scale = Window_Length / Screen_Length

		Window_Size = (Window_Width, Window_Length)

#Color Palette

Color_palette = {
	0: (0,0,0),
	1: (255,255,255),
	2: (255,0,0),
	3: (255,255,0),
	4: (0,255,0),
	5: (0,255,255),
	6: (0,0,255),
	7: (255,0,255)
}

import pygame

def initialize():
	pygame.init()

screen = pygame.display.set_mode(Window_Size)
pygame.display.set_caption("Screen Emulator for GPU")

def draw_screen(VRAM):
	screen.fill((0,0,0))
	i = 0
	for pixel in VRAM:	
		y = i // Screen_Width
		x = i % Screen_Width
		draw(x, y,Color_palette.get(pixel))
		i+=1

def update(VRAM):
	draw_screen(VRAM)
	pygame.display.flip()
	
def check_quit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	
def draw(x, y, color):
	scaledx = x * Width_Scale
	scaledy = y * Length_Scale
	pygame.draw.rect(screen, color, (scaledx, scaledy, Width_Scale, Length_Scale))
	
def blitter(x, y):
	return y * Screen_Width + x

def listen():
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			return pygame.key.name(event.key)
