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
    # Try to load sounds from files
    try:
        select_sound = mixer.Sound('select.wav')
        correct_sound = mixer.Sound('correct.wav')
        wrong_sound = mixer.Sound('wrong.wav')
        timer_sound = mixer.Sound('timer.wav')
    except:
        # Create simple fallback sounds if files are missing
        print("Sound files not found. Creating fallback sounds.")
        
        # Create a short beep sound as fallback
        sample_rate = 44100
        
        # Select sound (short high beep)
        select_buffer = pygame.sndarray.array(pygame.Surface((1, 1)))
        select_sound = mixer.Sound(buffer=select_buffer)
        select_sound.set_volume(0.2)
        
        # Correct sound (two ascending beeps)
        correct_buffer = pygame.sndarray.array(pygame.Surface((1, 1)))
        correct_sound = mixer.Sound(buffer=correct_buffer)
        correct_sound.set_volume(0.2)
        
        # Wrong sound (descending beep)
        wrong_buffer = pygame.sndarray.array(pygame.Surface((1, 1)))
        wrong_sound = mixer.Sound(buffer=wrong_buffer)
        wrong_sound.set_volume(0.2)
        
        # Timer sound (low beep)
        timer_buffer = pygame.sndarray.array(pygame.Surface((1, 1)))
        timer_sound = mixer.Sound(buffer=timer_buffer)
        timer_sound.set_volume(0.2)
except Exception as e:
    # If sound system completely fails, create dummy sound objects that do nothing
    print(f"Sound system error: {e}. Disabling sounds.")
    
    class DummySound:
        def play(self):
            pass
        def stop(self):
            pass
        def set_volume(self, vol):
            pass
    
    select_sound = DummySound()
    correct_sound = DummySound()
    wrong_sound = DummySound()
    timer_sound = DummySound()

# Button rectangles (adjusted for larger screen)
next_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 120, 300, 60)
play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60, 240, 70)
play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 120, 300, 70)

# Hexagon settings
HEXAGON_RADIUS = 50  # Larger hexagons
HEXAGON_MARGIN = 30  # Space between hexagons