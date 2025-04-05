import pygame
import math
import time
from assets import *

def draw_hexagon(surface, color, center, radius):
    """Draw a hexagon on the given surface."""
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        point = (center[0] + radius * math.cos(angle_rad),
                 center[1] + radius * math.sin(angle_rad))
        points.append(point)
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, BLACK, points, 3)  # Border
    return points

def draw_start_screen(screen):
    """Draw the start screen."""
    screen.fill(WHITE)
    
    # Title
    title_text = title_font.render("NUMBERS IQ", True, BLUE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_text = medium_font.render("A Mathematical Puzzle Game", True, DARK_GRAY)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70))
    screen.blit(subtitle_text, subtitle_rect)
    
    # Play button
    pygame.draw.rect(screen, BLUE, play_button_rect, border_radius=10)
    play_text = medium_font.render("PLAY", True, WHITE)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    screen.blit(play_text, play_text_rect)
    
    # Instructions
    instructions = [
        "Select numbers that equal the target when combined with the operator",
        "You have 20 seconds for each round",
        "The game automatically checks your answer as you select numbers",
        "Game gets harder as you progress!"
    ]
    
    for i, instruction in enumerate(instructions):
        inst_text = small_font.render(instruction, True, DARK_GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180 + i * 35))
        screen.blit(inst_text, inst_rect)

def draw_countdown(screen, countdown_start):
    """Draw the countdown screen before starting the game."""
    screen.fill(WHITE)
    
    time_passed = time.time() - countdown_start
    countdown = 3 - int(time_passed)
    
    if countdown > 0:
        count_text = large_font.render(str(countdown), True, BLUE)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(count_text, count_rect)
    else:
        ready_text = large_font.render("GO!", True, GREEN)
        ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(ready_text, ready_rect)

def draw_game_screen(screen, game):
    """Draw the main game screen during gameplay."""
    screen.fill(WHITE)
    
    # Draw target number
    target_text = large_font.render(f"Target: {game.target_number}", True, BLUE)
    target_rect = target_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(target_text, target_rect)
    
    # Draw operator (make it more prominent)
    op_symbol = ""
    if game.operator == "plus":
        op_symbol = "+"
    elif game.operator == "minus":
        op_symbol = "-"
    elif game.operator == "times":
        op_symbol = "×"
    elif game.operator == "divide":
        op_symbol = "÷"
    
    # Draw operator in a circle to make it stand out
    pygame.draw.circle(screen, PURPLE, (SCREEN_WIDTH // 2, 140), 50)
    op_text = operator_font.render(op_symbol, True, WHITE)
    op_rect = op_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
    screen.blit(op_text, op_rect)
    
    # Draw hexagons with numbers
    for i, (x, y) in enumerate(game.hexagon_positions):
        color = SELECTED_COLOR if i in game.selected_indices else HEXAGON_COLOR
        draw_hexagon(screen, color, (x, y), HEXAGON_RADIUS)
        
        num_text = medium_font.render(str(game.available_numbers[i]), True, WHITE)
        num_rect = num_text.get_rect(center=(x, y))
        screen.blit(num_text, num_rect)
    
    # Apply button removed - game uses automatic checking instead
    
    # Draw score and level
    score_text = small_font.render(f"Score: {game.score}", True, DARK_GRAY)
    screen.blit(score_text, (30, 30))
    
    level_text = small_font.render(f"Level: {game.level}", True, DARK_GRAY)
    screen.blit(level_text, (30, 70))
    
    # Draw round counter
    round_text = small_font.render(f"Round: {game.current_round}/{game.max_rounds}", True, DARK_GRAY)
    round_rect = round_text.get_rect(topright=(SCREEN_WIDTH - 30, 30))
    screen.blit(round_text, round_rect)
    
    # Draw timer
    # If showing the result screen for an incorrect answer, freeze the timer at its last value
    if game.game_state == "result" and game.last_result == "incorrect":
        time_left = 0  # Show empty timer for incorrect answers
    else:
        time_left = max(0, game.round_duration - (time.time() - game.round_start_time))
    
    timer_width = 400  # Wider timer bar
    timer_height = 25  # Taller timer bar
    timer_rect = pygame.Rect(SCREEN_WIDTH // 2 - timer_width // 2, 220, timer_width, timer_height)
    timer_fill_rect = pygame.Rect(SCREEN_WIDTH // 2 - timer_width // 2, 220, 
                                 timer_width * (time_left / game.round_duration), timer_height)
    
    # Timer color changes to red when low on time
    timer_color = GREEN if time_left > 3 else RED
    
    pygame.draw.rect(screen, GRAY, timer_rect)
    pygame.draw.rect(screen, timer_color, timer_fill_rect)
    pygame.draw.rect(screen, DARK_GRAY, timer_rect, 2)  # Border
    
    # Draw time left as text
    if game.game_state == "result" and game.last_result == "incorrect":
        time_text = small_font.render("Time's up!", True, BLACK)
    else:
        time_text = small_font.render(f"{time_left:.1f}s", True, BLACK)
    
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 220 + timer_height // 2))
    screen.blit(time_text, time_rect)
    
    # Selected numbers preview with expression
    if game.selected_indices:
        selected_nums = [str(game.available_numbers[i]) for i in game.selected_indices]
        
        # Display the expression based on the operator
        if game.operator == "plus":
            preview_text = " + ".join(selected_nums)
        elif game.operator == "minus":
            preview_text = " - ".join(selected_nums)
        elif game.operator == "times":
            preview_text = " × ".join(selected_nums)
        elif game.operator == "divide":
            preview_text = " ÷ ".join(selected_nums)
    else:
        preview_text = "Select numbers..."
    
    # Position the preview text at the bottom of the screen, well below any hexagons
    # This ensures it never overlaps with the numbers, even with 3+ rows
    preview_render = small_font.render(preview_text, True, DARK_GRAY)
    preview_rect = preview_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
    
    # Draw a semi-transparent background behind the text for better readability
    bg_rect = pygame.Rect(preview_rect.left - 20, preview_rect.top - 10, 
                          preview_rect.width + 40, preview_rect.height + 20)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((255, 255, 255, 180))
    screen.blit(bg_surface, (bg_rect.left, bg_rect.top))
    
    screen.blit(preview_render, preview_rect)

def draw_result_screen(screen, game):
    """Draw the result screen after each round."""
    # Keep the game screen visible in the background
    draw_game_screen(screen, game)
    
    # Draw a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))  # Semi-transparent white
    screen.blit(overlay, (0, 0))
    
    # Draw the result message
    if game.last_result == "correct":
        result_text = large_font.render("Correct!", True, GREEN)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(result_text, result_rect)
    else:
        # For incorrect answers, show the message and the correct solution
        result_text = large_font.render("Incorrect!", True, RED)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 40))
        screen.blit(result_text, result_rect)
        
        # Show the correct answer
        solution_text = medium_font.render("The correct answer was:", True, DARK_GRAY)
        solution_rect = solution_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 20))
        screen.blit(solution_text, solution_rect)
        
        # Display the correct numbers
        correct_nums = [str(game.available_numbers[i]) for i in game.correct_indices]
        
        # Format based on the operator
        if game.operator == "plus":
            correct_expr = " + ".join(correct_nums)
        elif game.operator == "minus":
            correct_expr = " - ".join(correct_nums)
        elif game.operator == "times":
            correct_expr = " × ".join(correct_nums)
        elif game.operator == "divide":
            correct_expr = " ÷ ".join(correct_nums)
            
        correct_expr_text = medium_font.render(correct_expr + f" = {game.target_number}", True, BLUE)
        correct_expr_rect = correct_expr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70))
        screen.blit(correct_expr_text, correct_expr_rect)
    
    # Draw the continue button (instead of "Next")
    pygame.draw.rect(screen, BLUE, next_button_rect, border_radius=10)
    
    if game.last_result == "correct":
        button_text = medium_font.render("Next", True, WHITE)
    else:
        button_text = medium_font.render("I Understand", True, WHITE)
        
    button_text_rect = button_text.get_rect(center=next_button_rect.center)
    screen.blit(button_text, button_text_rect)

def draw_end_screen(screen, game):
    """Draw the end game screen."""
    screen.fill(WHITE)
    
    # Draw final score
    title_text = large_font.render("Game Over!", True, BLUE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    score_text = medium_font.render(f"Final Score: {game.score}", True, DARK_GRAY)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    level_text = medium_font.render(f"Highest Level: {game.level}", True, DARK_GRAY)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(level_text, level_rect)
    
    # Draw play again button
    pygame.draw.rect(screen, GREEN, play_again_button_rect, border_radius=10)
    play_again_text = medium_font.render("Play Again", True, WHITE)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    screen.blit(play_again_text, play_again_text_rect)