# Numbers IQ Game

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A fast-paced math puzzle game that challenges your mental arithmetic skills through engaging number combinations.

<p align="center">
  <img src="https://via.placeholder.com/800x600.png?text=Numbers+IQ+Game" alt="Numbers IQ Game Screenshot" width="600"/>
</p>

## 🎮 Game Overview

Numbers IQ Game tests your ability to quickly identify number combinations that satisfy mathematical equations. Select numbers that, when combined with the given operator, equal the target value.

**Features:**
- Multiple operations: addition, subtraction, multiplication, and division
- Progressive difficulty system
- Automatic answer validation as you select numbers
- Hexagon-based user interface
- Detailed feedback on incorrect answers

## 🚀 Installation & Running

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Clone & Run
```bash
# Clone the repository
git clone https://github.com/rubenahrens/numbers-iq-game.git
cd numbers-iq-game

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## 🎯 How to Play

1. When the game starts, you'll see:
   - A target number at the top
   - An operator (plus, minus, times, divide) in a purple circle
   - Several numbers in hexagonal shapes

2. Click on hexagons to select numbers that, when combined with the operator, equal the target number
   - For example, if the target is 12, operator is "+", select numbers like 7 and 5
   - Numbers are automatically evaluated as you select them

3. You have 20 seconds for each round

4. If your answer is correct, you advance to the next round
   - For incorrect answers, you'll see the correct solution and need to click "I Understand" to continue

5. The game gets progressively harder as you score points

## 🧠 Strategies to Excel at Numbers IQ Game

### General Techniques

1. **Quick Scanning**
   - Before selecting any numbers, quickly scan all options
   - Look for obvious combinations first

2. **Backward Calculation**
   - Start with the target and work backward
   - For multiplication: think factors of the target
   - For division: multiply the target by possible divisors

### Operation-Specific Strategies

#### Addition (+)
- **Chunking**: Group numbers to make round numbers (like 10, 100)
- **Complement finding**: If target is 17 and you see 9, look for 8

#### Subtraction (-)
- **First number rule**: The first number is what you subtract from
- **Size check**: First number must be larger than the target (for single-subtraction problems)

#### Multiplication (×)
- **Factor pairs**: Know your multiplication tables cold (7×8=56, 9×6=54)
- **Decomposition**: Break complicated multiplications (7×8 = 7×4×2 = 28×2 = 56)

#### Division (÷)
- **Dividend first**: Always select the largest number (dividend) first
- **Think multiplication**: What multiplied by the divisor equals the dividend?

### Memory Mnemonics

1. **Visualization**
   - Picture numbers combining (5 and 5 joining to make 10)
   - Create mental pictures for common combinations

2. **Number Patterns**
   - Addition pairs that sum to 10 (1+9, 2+8, 3+7, 4+6, 5+5)
   - Multiplication table patterns (9's digit sum always equals 9)

3. **Quick Math Tricks**
   - Division by 5: multiply by 2, then divide by 10
   - Division by 9: add digits, if sum is divisible by 9, the number is too

## 📈 Level Progression

The game increases in difficulty as you progress:

| Level | Operations | Number Range | Time Limit |
|-------|------------|--------------|------------|
| 1-2   | +, ×       | 1-15         | 20s        |
| 3-4   | +, -, ×    | 1-25         | 20s        |
| 5+    | +, -, ×, ÷ | 1-40+        | 20s        |

## 💻 Project Structure

The game is divided into four main Python files:

- `main.py` - Entry point and game loop
- `game.py` - Game logic and state management
- `ui.py` - Rendering and display functionality
- `assets.py` - Game constants, colors, and resources

## 🔧 Customization

You can customize the game by modifying these values in `assets.py`:
- Screen dimensions
- Colors
- Difficulty progression
- Timer duration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ✨ Credits

Developed as a math-learning tool to improve mental arithmetic skills.

---

<p align="center">
  <i>Enhance your math skills while having fun!</i>
</p>