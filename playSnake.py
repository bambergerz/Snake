# playSnake.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Snake

This module contains the subcontroller to manage a single game in the Snake App.
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the snake_body, apples, and walls.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from models import *
from constants import *
import random

# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
	"""An instance controls a single game of Snake.
	 INSTANCE ATTRIBUTES:
		_snake [list of occupied Cell instances]: the snake whose head is controlled by the player. Initially will only consist of the head
		and it will be positioned at the left side of the screen pointing to the right.
		_apples [an instance of class Apple, which is a subclass of Cell]: the items which the player collects to earn points
		and increase the length of the snake. The apples are randomly generated to appear in one of the unoccupied cells.
		_wall [a list of Cell instances which are game borders]: If the snake head (the first item in the list _snake) touches a wall,
		the player loses.

	"""

	def __init__(self):
		"""Initializer: Creates a new Play object"""

		# Creating a 16x16 list using special list-creation notation: list comprehensions
		self._cells = [[None] * CELL_ROWS for _ in range(CELLS_PER_ROW)]
		self._snake = Snake()

		for x in range(CELLS_PER_ROW):
			for y in range(CELL_ROWS):
				self._cells[x][y] = Cell(x, y)

		self.create_apple()

	def draw_me(self, view):
		"""This function's purpose is to draw the bricks, paddle, and ball. The ball will only be drawn if self._ball does not equal None.
		As in, the ball will only be drawn after STATE_COUNTDOWN, where self._ball is no longer None.

		Parameter view: Immutable instance of GView; it is inherited from GameApp. View will be passed on from Breakout.
		Precondition: view is an instance of GView."""

		for row in self._cells:
			for cell in row:
				# print cell
				cell.draw(view)

		self._snake.draw(view)

	def create_apple(self):
		while True:
			xpos = random.randint(0, CELLS_PER_ROW - 1)
			ypos = random.randint(0, CELL_ROWS - 1)
			if self.is_empty_cell(xpos, ypos):
				self._cells[xpos][ypos] = Apple(xpos, ypos)
				break # stop the loop

	def tick(self):
		is_game_over = not self._snake.move()
		if is_game_over:
			return False

		snakehead_pos = self._snake.get_head().get_x(), self._snake.get_head().get_y()
		if isinstance(self._cells[snakehead_pos[0]][snakehead_pos[1]], Apple):
			self._snake.grow()
			self._change_apple_pos(snakehead_pos)

		return True

	def update_snake_direction(self, direction):
		self._snake.change_direction(direction)

	def _change_apple_pos(self, apple_pos):
		self._cells[apple_pos[0]][apple_pos[1]] = Cell(apple_pos[0], apple_pos[1])
		self.create_apple()

	def is_empty_cell(self, xpos, ypos):
		if isinstance(self._cells[xpos][ypos], Apple):
			return False
		if self._snake.is_occupying(xpos, ypos):
			return False
		return True


