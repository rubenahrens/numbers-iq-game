import random
import time
import math
from assets import *

class NumerosityGame:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reset the game variables for a new game."""
        self.score = 0
        self.level = 1
        self.current_round = 0
        self.max_rounds = 10
        self.game_state = "start"  # "start", "countdown", "play", "result", "end"
        self.countdown_start = 0
        self.round_start_time = 0
        self.round_duration = 10  # seconds (base duration)
        self.result_display_time = 0
        self.result_display_duration = 1.5  # seconds
        self.last_result = None  # "correct" or "incorrect"
        
        # Game elements
        self.target_number = 0
        self.operator = ""
        self.available_numbers = []
        self.selected_indices = []
        self.hexagon_positions = []
    
    def start_countdown(self):
        """Start the countdown before the game."""
        self.game_state = "countdown"
        self.countdown_start = time.time()
    
    def start_new_round(self):
        """Start a new round of the game."""
        self.generate_round(self.level)
        self.selected_indices = []
        self.round_start_time = time.time()
        self.current_round += 1
        self.game_state = "play"
        
        # Adjust round duration based on level (more difficult = less time)
        self.round_duration = max(5, 10 - (self.level - 1) // 2)
    
    def generate_round(self, difficulty):
        """Generate a new round with target number, operator, and available numbers."""
        # Number of available numbers increases with difficulty (3-8)
        num_count = min(3 + difficulty // 2, 8)
        
        # Operators become more varied with difficulty
        if difficulty <= 2:
            # Level 1-2: Only addition and multiplication with small numbers
            operator_choices = ["plus", "times"]
        elif difficulty <= 4:
            # Level 3-4: Add subtraction
            operator_choices = ["plus", "minus", "times"]
        else:
            # Level 5+: All operators
            operator_choices = ["plus", "minus", "times", "divide"]
        
        self.operator = random.choice(operator_choices)
        
        # Generate available numbers based on the operator and difficulty
        self.available_numbers = []
        
        if self.operator == "plus":
            # For addition, use larger numbers with higher difficulty
            max_num = 10 + 5 * difficulty
            self.available_numbers = [random.randint(1, max_num) for _ in range(num_count)]
        
        elif self.operator == "minus":
            # For subtraction, ensure the result is positive
            max_num = 10 + 5 * difficulty
            self.available_numbers = [random.randint(1, max_num) for _ in range(num_count)]
        
        elif self.operator == "times":
            # For multiplication, adjust number range based on difficulty
            if difficulty <= 3:
                # Easier levels: small numbers (1-5)
                self.available_numbers = [random.randint(1, 5) for _ in range(num_count)]
            else:
                # Higher levels: larger numbers (1-10)
                self.available_numbers = [random.randint(1, 10) for _ in range(num_count)]
        
        elif self.operator == "divide":
            # For division, ensure clean division
            if difficulty <= 5:
                # Easier levels: simple divisions
                divisors = [random.randint(1, 5) for _ in range(num_count-1)]
            else:
                # Higher levels: harder divisions
                divisors = [random.randint(1, 10) for _ in range(num_count-1)]
            
            dividend = random.randint(1, 50 * difficulty // 3)
            for divisor in divisors:
                dividend *= divisor
            
            self.available_numbers = divisors + [dividend]
            random.shuffle(self.available_numbers)
        
        # Choose a subset of numbers that will make the target
        max_subset_size = min(3 + difficulty // 3, num_count)
        subset_size = random.randint(2, max_subset_size)
        subset_indices = random.sample(range(num_count), subset_size)
        subset = [self.available_numbers[i] for i in subset_indices]
        
        # Calculate the target number
        if self.operator == "plus":
            self.target_number = sum(subset)
        
        elif self.operator == "minus":
            # For higher difficulty, make more complex subtraction chains
            if difficulty >= 5 and len(subset) > 2:
                # A - B - C - ...
                self.target_number = subset[0]
                for num in subset[1:]:
                    self.target_number -= num
            else:
                # Simple subtraction: First number minus the rest
                self.target_number = subset[0] - sum(subset[1:])
        
        elif self.operator == "times":
            self.target_number = 1
            for num in subset:
                self.target_number *= num
        
        elif self.operator == "divide":
            # For division, construct the problem carefully
            if difficulty >= 5 and len(subset) > 2:
                # More complex division chain for higher levels
                self.target_number = subset[0]
                for num in subset[1:]:
                    if num == 0:  # Prevent division by zero
                        num = 1
                    self.target_number /= num
            else:
                # Simple division
                dividend = max(subset)
                divisors = [n for n in subset if n != dividend]
                
                if not divisors:  # Just in case
                    divisors = [1]
                
                divisor_product = 1
                for n in divisors:
                    divisor_product *= n
                
                self.target_number = dividend / divisor_product
        
        # Ensure target is an integer or has at most 1 decimal place
        self.target_number = round(self.target_number, 1)
        if self.target_number == int(self.target_number):
            self.target_number = int(self.target_number)
        
        # Calculate hexagon positions in two columns
        self.arrange_hexagons_in_columns(num_count)
    
    def arrange_hexagons_in_columns(self, num_count):
        """Arrange the hexagons in two columns."""
        self.hexagon_positions = []
        
        # Determine number of rows and columns
        if num_count <= 6:
            cols = 2
            rows = (num_count + 1) // 2
        else:
            # For more than 6 numbers, use 3 columns
            cols = 3
            rows = (num_count + 2) // 3
        
        # Center position
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Calculate the total width and height of the grid
        grid_width = cols * (2 * HEXAGON_RADIUS + HEXAGON_MARGIN) - HEXAGON_MARGIN
        grid_height = rows * (2 * HEXAGON_RADIUS + HEXAGON_MARGIN) - HEXAGON_MARGIN
        
        # Starting position (top-left of the grid)
        start_x = center_x - grid_width // 2 + HEXAGON_RADIUS
        start_y = center_y - grid_height // 2 + HEXAGON_RADIUS
        
        # Create positions for each hexagon
        for i in range(num_count):
            col = i % cols
            row = i // cols
            
            # Add a slight offset to odd rows for a more hexagonal pattern
            offset = HEXAGON_RADIUS if row % 2 == 1 and cols > 2 else 0
            
            x = start_x + col * (2 * HEXAGON_RADIUS + HEXAGON_MARGIN) + offset
            y = start_y + row * (2 * HEXAGON_RADIUS + HEXAGON_MARGIN)
            
            self.hexagon_positions.append((x, y))
    
    def handle_click(self, mouse_pos):
        """Handle mouse clicks based on game state."""
        if self.game_state == "start" and play_button_rect.collidepoint(mouse_pos):
            self.start_countdown()
            
        elif self.game_state == "play":
            # Check for hexagon clicks
            for i, (x, y) in enumerate(self.hexagon_positions):
                if self.point_in_hexagon(mouse_pos, (x, y), HEXAGON_RADIUS):
                    if i in self.selected_indices:
                        self.selected_indices.remove(i)
                    else:
                        self.selected_indices.append(i)
                    select_sound.play()
                    return
            
            # Check for apply button click
            if apply_button_rect.collidepoint(mouse_pos) and self.selected_indices:
                self.check_answer()
        
        elif self.game_state == "result" and next_button_rect.collidepoint(mouse_pos):
            if self.current_round < self.max_rounds:
                self.start_new_round()
            else:
                self.game_state = "end"
        
        elif self.game_state == "end" and play_again_button_rect.collidepoint(mouse_pos):
            self.reset_game()
    
    def check_answer(self):
        """Check if the selected numbers give the correct answer."""
        selected_numbers = [self.available_numbers[i] for i in self.selected_indices]
        result = self.calculate_result(selected_numbers, self.operator)
        
        if result == self.target_number:
            self.last_result = "correct"
            correct_sound.play()
            self.score += 1
            
            # Increase level based on score, with more frequent increases at lower levels
            if self.score <= 5:
                # Faster progression early on
                if self.score % 1 == 0:
                    self.level = min(self.level + 1, 10)
            else:
                # Slower progression later
                if self.score % 2 == 0:
                    self.level = min(self.level + 1, 10)
        else:
            self.last_result = "incorrect"
            wrong_sound.play()
        
        self.game_state = "result"
        self.result_display_time = time.time()
    
    def update(self):
        """Update game state based on time."""
        if self.game_state == "countdown":
            # Check if countdown is complete
            if time.time() - self.countdown_start >= 3:
                self.start_new_round()
        
        elif self.game_state == "play":
            # Check if time is up
            if time.time() - self.round_start_time >= self.round_duration:
                self.last_result = "incorrect"
                wrong_sound.play()
                self.game_state = "result"
                self.result_display_time = time.time()
        
        elif self.game_state == "result":
            # Auto-advance after result display duration
            if time.time() - self.result_display_time >= self.result_display_duration:
                if self.current_round < self.max_rounds:
                    self.start_new_round()
                else:
                    self.game_state = "end"
    
    def calculate_result(self, nums, op):
        """Calculate the result of applying the operator to the numbers."""
        if not nums:
            return None
        
        if op == "plus":
            return sum(nums)
        
        elif op == "minus":
            # Subtraction: first number minus the rest
            result = nums[0]
            for num in nums[1:]:
                result -= num
            return result
        
        elif op == "times":
            # Multiplication: product of all numbers
            result = 1
            for num in nums:
                result *= num
            return result
        
        elif op == "divide":
            # Division: first number divided by the rest
            result = nums[0]
            for num in nums[1:]:
                if num == 0:  # Prevent division by zero
                    return None
                result /= num
            return result
    
    def point_in_hexagon(self, point, center, radius):
        """Check if a point is inside a hexagon."""
        # Simple distance-based check (not perfect but sufficient for clicks)
        return math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2) <= radius
