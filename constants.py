# constants.py
# Walker M. White (wmw2)
# November 12, 2014
"""Constants for Snake

This module contains global constants for the game Snake.  These constants 
need to be used in the model, the view, and the controller. As these
are spread across multiple modules, we separate the constants into
their own module. This allows all modules to access them."""
import sys


######### WINDOW CONSTANTS (all coordinates are in pixels) #########

#: the width of the game display 
GAME_WIDTH = 560
#: the height of the game display
GAME_HEIGHT = 560


######### Cell CONSTANTS #########

#: the width of the cell
CELL_WIDTH = 40
#: the height of the cell
CELL_HEIGHT = 40



######### GAME CONSTANTS #########

#: Snake speed (in cells per second):
SNAKE_SPEED = 4
#: Number of cell rows:
CELL_ROWS = 14
#: Number of cells per row:
CELLS_PER_ROW = 14

#: state before the game has started
STATE_INACTIVE = 0
#: state when we are initializing a new game
STATE_NEWGAME = 1
#: state when we are counting down to the ball serve
STATE_COUNTDOWN = 2
#: state when we are waiting for user to click the mouse
STATE_PAUSED = 3
#: state when the ball is in play and being animated
STATE_ACTIVE = 4
#: state when the ball intentionally paused
STATE_INT_PAUSED = 5
#: state when the game is either lost or won
STATE_COMPLETE = 6



######### Directions #########
# Read about enum! They are cool!
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def opposite_dir(direction):
	if direction == UP:
		return DOWN
	if direction == DOWN:
		return UP
	if direction == LEFT:
		return RIGHT
	if direction == RIGHT:
		return LEFT

######### Snake init position #########
INIT_X = 0
INIT_Y = 8
INIT_DIR = RIGHT



######### COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF BRICKS IN ROW #########
"""sys.argv is a list of the command line arguments when you run
python. These arguments are everything after the work python. So
if you start the game typing

    python Snake.py 4
    
Python puts ['breakout.py', '4'] into sys.argv. Below, we 
take advantage of this fact to change the constant SNKAE_SPEED"""

try:
	if (not sys.argv is None and len(sys.argv) == 2):
		level = int(sys.argv[1])
		if levels > 0 and levels < 11:
			SNAKE_SPEED = 1 + 0.5 * level
except:  # Leave the contants alone
	pass


	######### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY #########
