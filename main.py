import pygame
import sys
from assets import *
from game import NumbersIQGame
import ui

def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Numbers IQ Game")
    
    # Create the screen with larger dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create the game instance
    game = NumbersIQGame()
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                game.handle_click(pygame.mouse.get_pos())
        
        # Update game state
        game.update()
        
        # Draw the appropriate screen based on game state
        if game.game_state == "start":
            ui.draw_start_screen(screen)
        
        elif game.game_state == "countdown":
            ui.draw_countdown(screen, game.countdown_start)
        
        elif game.game_state == "play":
            ui.draw_game_screen(screen, game)
        
        elif game.game_state == "result":
            ui.draw_result_screen(screen, game)
        
        elif game.game_state == "end":
            ui.draw_end_screen(screen, game)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()