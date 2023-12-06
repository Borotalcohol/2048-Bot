# 🧩 2048-Bot
This repository houses the source code for a 2048-playing bot, designed to autonomously play the popular 2048 puzzle game, recreated in Python using Pygame

<img src="resources/demo.gif" width="400"/>

## 1. Folders
In this repository you'll find three folders:
- 📁 **base**: Here you can find the base code for the 2048 game implemented in Pygame, with NO automation. You can play it using the keyboard arrows.
- 📁 **automatic**: Here you can find the code for the 2048 game which is played by the Expectiminimax bot.
- 📁 **experiments**: A little extra, this was my first experiment using Reinforcement Learning. For the ones interested in giving this method a second chance, here you can find the code that I used, including a custom Gymnasium Environment for the game.

## 2. Execution
In order to execute the code of one of the above folders, you can follow these instructions:

- Open a terminal and navigate in your desired directory
- Clone this repository using `git clone https://github.com/Borotalcohol/2048-Bot.git`
- Move inside the just cloned repository with `cd 2048-Bot`
- Move inside one of the desired folder, for example, `automatic` -> `cd automatic`
- Create a Python virtual environment using `python3 -m venv venv`
- Activate the virtual environment with `source venv/bin/activate` (Linux and MacOS) or `./venv/Scripts/activate` (Windows)
- Install the packages with `pip install -r requirements.txt`
- Run the main script in the folder: `python3 main.py`

## 3. Explanation
This is a brief explanation of the standard solution adopted in the bot implemented in the `automatic` folder:

### 3.1 2048 Game Introduction
2048 is a puzzle game played on a 4x4 grid. Your mission is simple: slide tiles left, right, up, or down to merge those with matching numbers. When you do this, they combine into a single tile with double the value.

<img src="resources/2.png" width="400"/>

Your ultimate goal? Reach that prized 2048 tile. What's intriguing is that once you achieve it, you face a choice: pause and celebrate your triumph or continue the journey to create even larger tiles like 4096, 8192, and beyond.

Quick Game Recap:

🟡 The game unfolds on a 4x4 grid.<br />
🟡 Two initial tiles with random values set the stage for your journey. 🎲🌟<br />
🟡 Each move that alters the board spawns a new tile randomly (with value 2 with a 90% probability and value 4 with a 10% probability).<br />
🟡 Combining adjacent tiles with identical values results in a single tile with double the value (2 and 2 make 4, 4 and 4 make 8, and so on).<br />
🟡 The game ends when you can no longer make a move that changes the board. ❌🛑<br />

### 3.2 Tic-tac-toe and Minimax
Let's delve deeper into our solution by grasping a pivotal concept in decision theory: Minimax. 🧠

🎲 What is Minimax?

In the realm of game theory, Minimax stands out as a foundational strategy utilized in two-player games with outcomes falling into three categories: win, lose, or tie.
At its core, Minimax involves players strategically pursuing victory. Each player, in their turn, aims to make the optimal move leading to a win while hindering their opponent's progress.

To simplify, at every stage of the game, players aim to:<br />
📈 MAXIMIZE their MINIMUM potential gain.<br />
📉 MINIMIZE their opponent's MAXIMUM potential advantage.<br />

This dual-sided strategy is aptly named "Minimax." 🔄

🎲 Applying Minimax to Tic-tac-toe<br />
How does Minimax relate to the classic Tic-tac-toe game? In Tic-tac-toe, players (let's call them 'X' and 'O') take turns striving to win while blocking the opponent. They make moves to MAXIMIZE their chances of winning and MINIMIZE their opponent's opportunity for victory.

If we consider 'X' on its turn, a MINIMAX algorithm would evaluate all potential moves as follows:
- If a move leads to a win, assign a positive value (e.g., +1) and return.
- If not a winning position, evaluate possible adversary moves:
 - If the adversary can win, return a negative value (e.g., -1).
 - If not, evaluate all possible moves for 'X' from this new position.

This recursive approach continues until reaching a draw, a winning position, or a predetermined maximum depth to manage computational complexity.

The algorithm calculates evaluations for upper nodes by selecting the minimum value during "minimizing" turns (we take the least favorable state evaluation because we are pretty sure that the adversary will probably make the most favorable move for him) and the maximum value during "maximizing" turns (same reasoning but during our turn).

<img src="resources/3.png" width="600"/>

### 3.3 Expectiminimax

<img src="resources/4.png" width="600"/>

Why and how apply Minimax to our 2048 bot? Let's unravel the mystery.

While you might think you're solo in the 2048 game, it's a bit like facing off against the game's algorithm, spawning tiles randomly after each move.

🎲 Now, this "enemy" isn't playing to win; it's just tossing tiles randomly onto your board. So, how does minimax logic fit into this with the UNCERTAINTY of random tile spawns?

Enter the Expectiminimax algorithm.

The name itself reveals a focus on the "expected" value in decision-making, tackling the uncertainty of random tile spawns. Given the 2048 board's current state, we can predict four possible moves (up, down, left, right), but we don't know where or which tile will appear after the move. Probability theory steps in to bridge this gap.

Consider this:

**N**: number of empty tiles after a move
**p_2**: probability of a 2 tile spawning (90%)
**p_4**: probability of a 4 tile spawning (10%)
**B_eval**: a "goodness" score for a specific board configuration
We evaluate each possible outcome with the formula:

**(1 / N) * p_2 * B_eval** -> for a 2 tile spawn
**(1 / N) * p_4 * B_eval** -> for a 4 tile spawn
In simpler terms, we're weighing the "goodness" score by the probability of that configuration appearing after the move.

To determine the best next move, we construct a tree to evaluate future states, considering the uncertainty component:

1️⃣ Start from the current game state (root of the tree)<br />
2️⃣ Determine how the board changes with all 4 moves (excluding the random tile)<br />
3️⃣ These modified boards become the root's children<br />
4️⃣ For each board, the children include all possible tile spawn configurations<br />

This procedure continues until a maximum given depth. Unlike Tic-tac-toe, this is computationally heavy, but with a depth of 1, we achieve decent results, reaching the 2048 tile most times.

Alright, we’re missing a single but very important thing now, how do we evaluate the “goodness” of a board configuration? (That is, how do we determine **B_eval** given a board config?)

### 3.4 Snake Heuristic
Let's unravel the magic behind board evaluations. It's time to talk about the Snake Heuristic!

<img src="resources/5.png" width="600"/>

But first, a quick recap:

In my initial attempt, I tried to evaluate board configurations based on:

1️⃣ Number of empty tiles<br />
2️⃣ Highest tile present<br />
3️⃣ Smoothness of tile placement<br /> 

While this provided some insights, there was room for improvement.

Enter the "Snake Heuristic" a simpler and more effective evaluation function.

🔎 What's a Heuristic?

A heuristic is a practical approach to problem-solving that may not guarantee perfection but is sufficient for reaching immediate goals or approximations.

Now, back to the Snake Heuristic. If you're familiar with 2048, you might have come across the strategy of keeping the highest tile in a corner and forming a "snake" pattern with the lower tiles. This strategy allows for efficient merging, creating a sequence of tile combinations.

👨‍💻 Implementation:

This strategy was easily implemented by multiplying (dot product) the board configuration with a "reference heuristic board" that mirrors this snake-like pattern. The closer a configuration resembles this shape, with the highest tiles adjacent in a snake pattern, the higher the "goodness" score.

🎲 Remember, this isn't the final evaluation. The Snake Heuristic score is then multiplied by a probability factor, accounting for the likelihood of this configuration occurring

### 3.5 Implementation
Let's dive into the behind-the-scenes of implementing Expectiminimax using Python and Pygame. How did we bring this bot to life? Let's break it down!

First things first, we needed a method to determine the best move at any given state. Enter the getBestAction method:

```
For each possible move (direction):
 Compute the new board after this move
 If the new board is different from the current board
  Compute goodness of this new board
  If the goodness is better than the current best score:
   Set this as the new best score and the corresponding action to the best action

Return the best action
```

Now, let's zoom in on the method responsible for calculating the goodness of a given board configuration. Brace yourselves for a journey into the decision-making core:

```
If the board is in a game-over state, return -∞
If the depth is less than 0, return the score calculated by the Snake Heuristics

If processing tree on the directions level:
 For each possible move (direction):
  Compute the new board
  If the new board is different from the current board:
   Compute goodness score of this new board (recursion) reducing the depth

If processing tree on the combinations level:
 For each empty tile on the board:
  Create a clone with a 2 tile in this empty position
  Create a clone with a 4 tile in this empty position
  Compute goodness of both configurations
  Weight the goodness score by the probability factor (1/num of empty tiles)  (p_2 or p_4)  goodness score
  Add up these scores to the total score

Return score and action (direction)
```

### 3.6 Results
In order to obtain reliable statistics, I conducted a 100-simulation experiment, noting the highest tile reached in each game. The results are elegantly displayed in the barplot below ⬇️.

<img src="resources/6.png" width="600"/>

On average, the bot secures victory by reaching the coveted 2048 tile, occasionally pushing beyond to claim the 4096 tile. However, there are instances where it faces challenges, falling short of the 2048 mark.

It's worth noting that these results were achieved with the maximum depth fixed at 1 to maintain optimal speed—any higher, and the bot's performance slowed considerably.

## 4. Contribution
Feel free to fork this repository and work on your own solution!
I will leave the opportunity to contribute open for a while and then move on to implementing a website where I will cite those that helped reaching better results!
