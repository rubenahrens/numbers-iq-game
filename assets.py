import pygame
from pygame import mixer

# Initialize pygame for font and mixer
pygame.init()
mixer.init()

# Window settings - Increased window size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 255)
LIGHT_BLUE = (100, 180, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (180, 60, 220)
HEXAGON_COLOR = (70, 130, 180)
SELECTED_COLOR = (255, 165, 0)

# Fonts - Larger for better visibility
title_font = pygame.font.SysFont('Arial', 70)
large_font = pygame.font.SysFont('Arial', 56)
medium_font = pygame.font.SysFont('Arial', 42)
small_font = pygame.font.SysFont('Arial', 28)
operator_font = pygame.font.SysFont('Arial', 80)  # Special font for the operator

# Sounds
try:
    select_sound = mixer.Sound('select.wav')
    correct_sound = mixer.Sound('correct.wav')
    wrong_sound = mixer.Sound('wrong.wav')
    timer_sound = mixer.Sound('timer.wav')
except:
    # If sounds aren't available, use placeholder sounds
    select_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    correct_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    wrong_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    timer_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))

# Button rectangles (adjusted for larger screen)
apply_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 120, 200, 60)
next_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 120, 200, 60)
play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60, 240, 70)
play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 120, 300, 70)

# Hexagon settings
HEXAGON_RADIUS = 50  # Larger hexagons
HEXAGON_MARGIN = 30  # Space between hexagons
