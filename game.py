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
        self.round_duration = 20  # seconds (base duration changed to 20)
        self.result_display_time = 0
        self.result_display_duration = 1.5  # seconds
        self.last_result = None  # "correct" or "incorrect"
        
        # Game elements
        self.target_number = 0
        self.operator = ""
        self.available_numbers = []
        self.selected_indices = []
        self.hexagon_positions = []
        self.correct_indices = []
    
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
        # Starting from 20 seconds and decreasing by 1 second every 2 levels
        self.round_duration = max(10, 20 - (self.level - 1) // 2)
    
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
        
        # Generate available numbers based on the operator
        self.available_numbers = []
        
        # Generate valid numbers and target based on the operator
        valid_round = False
        max_attempts = 10  # Prevent infinite loops
        
        for attempt in range(max_attempts):
            try:
                if self.operator == "plus":
                    self.generate_addition_round(num_count, difficulty)
                elif self.operator == "minus":
                    self.generate_subtraction_round(num_count, difficulty)
                elif self.operator == "times":
                    self.generate_multiplication_round(num_count, difficulty)
                elif self.operator == "divide":
                    self.generate_division_round(num_count, difficulty)
                
                # Verify the solution is correct
                solution_numbers = [self.available_numbers[i] for i in self.correct_indices]
                calculated_result = self.calculate_result(solution_numbers, self.operator)
                
                # Ensure the calculated result matches the target
                if calculated_result == self.target_number:
                    valid_round = True
                    break
                else:
                    print(f"Validation failed: {solution_numbers} {self.operator} = {calculated_result}, expected {self.target_number}")
            except Exception as e:
                print(f"Error generating round: {e}")
        
        if not valid_round:
            # Fallback to a simple addition problem if we couldn't generate a valid round
            self.operator = "plus"
            self.available_numbers = [1, 2, 3, 4, 5]
            self.target_number = 3
            self.correct_indices = [0, 1]  # 1+2=3
            
        # Calculate hexagon positions in two columns
        self.arrange_hexagons_in_columns(num_count)
    
    def generate_addition_round(self, num_count, difficulty):
        """Generate numbers for an addition round."""
        # For addition, use larger numbers with higher difficulty
        max_num = 10 + 5 * difficulty
        self.available_numbers = [random.randint(1, max_num) for _ in range(num_count)]
        
        # Choose a subset of numbers that will make the target
        max_subset_size = min(3 + difficulty // 3, num_count)
        subset_size = random.randint(2, max_subset_size)
        subset_indices = random.sample(range(num_count), subset_size)
        subset = [self.available_numbers[i] for i in subset_indices]
        
        # Calculate the target number
        self.target_number = sum(subset)
        self.correct_indices = subset_indices
    
    def generate_subtraction_round(self, num_count, difficulty):
        """Generate numbers for a subtraction round."""
        max_num = 10 + 5 * difficulty
        self.available_numbers = [random.randint(1, max_num) for _ in range(num_count)]
        
        # Choose a subset of numbers that will make the target
        max_subset_size = min(3 + difficulty // 3, num_count)
        subset_size = random.randint(2, max_subset_size)
        subset_indices = random.sample(range(num_count), subset_size)
        subset = [self.available_numbers[i] for i in subset_indices]
        
        # For higher difficulty, make more complex subtraction chains
        if difficulty >= 5 and len(subset) > 2:
            # A - B - C - ...
            self.target_number = subset[0]
            for num in subset[1:]:
                self.target_number -= num
        else:
            # Simple subtraction: First number minus the rest
            self.target_number = subset[0] - sum(subset[1:])
        
        self.correct_indices = subset_indices
    
    def generate_multiplication_round(self, num_count, difficulty):
        """Generate numbers for a multiplication round."""
        # For multiplication, adjust number range based on difficulty
        if difficulty <= 3:
            # Easier levels: small numbers (1-5)
            self.available_numbers = [random.randint(1, 5) for _ in range(num_count)]
        else:
            # Higher levels: larger numbers (1-10)
            self.available_numbers = [random.randint(1, 10) for _ in range(num_count)]
        
        # Choose a subset of numbers that will make the target
        max_subset_size = min(3 + difficulty // 3, num_count)
        subset_size = random.randint(2, max_subset_size)
        subset_indices = random.sample(range(num_count), subset_size)
        subset = [self.available_numbers[i] for i in subset_indices]
        
        # Calculate the target number
        result = 1
        for num in subset:
            result *= num
        self.target_number = result
        self.correct_indices = subset_indices
    
    def generate_division_round(self, num_count, difficulty):
        """Generate numbers for a division round that results in a whole number."""
        # Start with the target number (what we want the result to be)
        if difficulty <= 5:
            # Easier levels: simple divisions with small results
            target = random.randint(1, 10)
        else:
            # Higher levels: harder divisions
            target = random.randint(1, 20)
        
        # Choose a subset size (how many numbers to divide)
        max_subset_size = min(3, num_count)
        subset_size = random.randint(2, max_subset_size)
        
        # Start with divisors
        divisors = [random.randint(1, 5) for _ in range(subset_size - 1)]
        
        # Calculate the dividend so that result equals target
        dividend = target
        for divisor in divisors:
            dividend *= divisor
        
        # Create the full set of available numbers, including the dividend
        self.available_numbers = []
        for _ in range(num_count - subset_size):
            # Add some random numbers that won't be part of the solution
            self.available_numbers.append(random.randint(1, 20))
        
        # Add divisors to available numbers
        self.available_numbers.extend(divisors)
        # Add dividend to available numbers
        self.available_numbers.append(dividend)
        
        # Shuffle to randomize positions
        random.shuffle(self.available_numbers)
        
        # Find the indices of our solution numbers
        dividend_index = self.available_numbers.index(dividend)
        divisor_indices = []
        for divisor in divisors:
            # Find each divisor (first occurrence only)
            divisor_index = self.available_numbers.index(divisor)
            # If a divisor appears multiple times, we need to handle that
            # by temporarily replacing the value to avoid finding it again
            self.available_numbers[divisor_index] = -divisor  # Mark as found
            divisor_indices.append(divisor_index)
        
        # Restore the original values
        for i, idx in enumerate(divisor_indices):
            self.available_numbers[idx] = divisors[i]
        
        # Set the target and correct indices
        self.target_number = target
        # The dividend must be first for correct division order
        self.correct_indices = [dividend_index] + divisor_indices
    
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
        
        # Fix for overlap issue - move the hexagons down by adding vertical offset
        # Add more space between timer bar and hexagons when there are 3 rows
        vertical_offset = 30  # Base offset
        if rows >= 3:
            vertical_offset += 40  # Extra space for 3 or more rows
        
        # Starting position (top-left of the grid)
        start_x = center_x - grid_width // 2 + HEXAGON_RADIUS
        start_y = center_y - grid_height // 2 + HEXAGON_RADIUS + vertical_offset
        
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
                        # If deselecting a number
                        self.selected_indices.remove(i)
                    else:
                        # If selecting a new number
                        self.selected_indices.append(i)
                    
                    select_sound.play()
                    
                    # Automatically check the answer after each selection/deselection
                    if self.selected_indices:
                        self.check_answer_automatically()
                    return
        
        elif self.game_state == "result" and next_button_rect.collidepoint(mouse_pos):
            if self.current_round < self.max_rounds:
                self.start_new_round()
            else:
                self.game_state = "end"
        
        elif self.game_state == "end" and play_again_button_rect.collidepoint(mouse_pos):
            self.reset_game()
    
    def check_answer_automatically(self):
        """Automatically check if the selected numbers give the correct answer or are invalid."""
        selected_numbers = [self.available_numbers[i] for i in self.selected_indices]
        result = self.calculate_result(selected_numbers, self.operator)
        
        # If we have a valid result and it equals the target
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
                    
            self.game_state = "result"
            self.result_display_time = time.time()
            
        # If the result is now impossible (for example, in a multiplication if product exceeds target)
        elif self.is_answer_impossible(selected_numbers, result):
            self.last_result = "incorrect"
            wrong_sound.play()
            self.game_state = "result"
            self.result_display_time = time.time()
    
    def is_answer_impossible(self, selected_numbers, current_result):
        """Check if it's impossible to reach the target with the current selections."""
        if current_result is None:
            return False
            
        if self.operator == "plus":
            # For addition, if current sum already exceeds target, it's impossible
            return current_result > self.target_number
            
        elif self.operator == "minus":
            # For subtraction, if we have all numbers and result isn't target, it's wrong
            # (Hard to determine otherwise without knowing order)
            if len(selected_numbers) >= len(self.correct_indices):
                return current_result != self.target_number
            return False
            
        elif self.operator == "times":
            # For multiplication, if product already exceeds target, it's impossible
            return current_result > self.target_number
            
        elif self.operator == "divide":
            # For division, only mark as wrong when all expected numbers are selected
            # This allows players to build up their division operation step by step
            if len(selected_numbers) == len(self.correct_indices):
                # Only check if all numbers in the correct solution are selected
                return current_result != self.target_number
            return False
        
        return False
    
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
            # Auto-advance ONLY if the answer was correct
            # For incorrect answers, require the player to click "I Understand"
            if self.last_result == "correct" and time.time() - self.result_display_time >= self.result_display_duration:
                if self.current_round < self.max_rounds:
                    self.start_new_round()
                else:
                    self.game_state = "end"
    
    def calculate_result(self, nums, op):
        """Calculate the result of applying the operator to the numbers."""
        if not nums or len(nums) < 2:
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
            
            # Round to handle floating point imprecision
            result = round(result, 10)
            # Convert to int if it's a whole number
            if result == int(result):
                result = int(result)
                
            return result
    
    def point_in_hexagon(self, point, center, radius):
        """Check if a point is inside a hexagon."""
        # Simple distance-based check (not perfect but sufficient for clicks)
        return math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2) <= radius