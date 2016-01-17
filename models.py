"""Models module for Snake

This module contains the model classes for the Snake game. That is anything that you
interact with on the screen is model: the snake, the apples, and any of the walls.

"""
from constants import *
from game2d import *


def move_cell(x, y, direction):
	if direction == UP:
		return x, y + 1
	elif direction == RIGHT:
		return x + 1, y
	elif direction == DOWN:
		return x, y - 1
	else:
		return x - 1, y


class Cell(GImage):
	"""An instance is a cell in the game

	The attributes of this class are those inherited from GRectangle.

	LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
	"""

	# INITIALIZER TO CREATE A NEW PADDLE
	def __init__(self, xcor, ycor):
		"""Initializer: Creates a new Cell object.

		The cell inherits attributes from the GRectangle initializer. We will call the GRectangle initializer
		to construct an object of this class. Note that GRectangle is a subclass of GObject."""

		# LATER ON CHANGE LINECOLOR BACK TO WHITE!!!

		self._color = colormodel.WHITE
		self._xcor = xcor
		self._ycor = ycor

		GImage.__init__(self,
		                left=xcor * CELL_WIDTH,
		                bottom=ycor * CELL_HEIGHT,
		                height=CELL_HEIGHT,
		                width=CELL_WIDTH,
		                source="bark.jpg")

	def get_x(self):
		return self._xcor

	def get_y(self):
		return self._ycor

	def set_x(self, x):
		self._xcor = x
		self.left = self._xcor * CELL_WIDTH  # Updating GObject

	def set_y(self, y):
		self._ycor = y
		self.bottom = self._ycor * CELL_WIDTH  # Updating GObject


class Apple(Cell):
	"""An instance is a randomly appearing apple in the game. Collecting an apple elongates the snake.
	The attributes from this class are inherited from Cell, whose attributes are inherited from GRectangle and GObject."""

	def __init__(self, xcor, ycor):
		Cell.__init__(self, xcor, ycor)
		self.source = "apple.png"


class BodyPart(Cell):

	HEAD = 0
	BODY = 1
	TAIL = 2

	def __init__(self, xcor, ycor, direction, src_direction):
		Cell.__init__(self, xcor, ycor)
		self._direction = direction
		self._src_direction = src_direction

	def get_direction(self):
		return self._direction

	def set_direction(self, direction):
		self._direction = direction

	def set_src_direction(self, src_direction):
		self._src_direction = src_direction

	def get_src_direction(self):
		return self._src_direction

	def _set_image(self, bodypart_type):
		image = None
		if bodypart_type == BodyPart.HEAD:
			image = {
				UP: 'head_top.png',
				DOWN: 'head_bottom.png',
				LEFT: 'head_left.png',
				RIGHT: 'head_right.png'
			}[self._direction]
		elif bodypart_type == BodyPart.TAIL:
			image = {
				UP: 'tail_bottom.png',
				DOWN: 'tail_top.png',
				LEFT: 'tail_right.png',
				RIGHT: 'tail_left.png'
			}[self._direction]
		else:
			if self._has_directions(LEFT, RIGHT):
				image = 'body_horizontal.png'
			elif self._has_directions(UP, DOWN):
				image = 'body_vertical.png'
			elif self._has_directions(DOWN, RIGHT):
				image = 'curve_bottom-right.png'
			elif self._has_directions(DOWN, LEFT):
				image = 'curve_bottom-left.png'
			elif self._has_directions(UP, RIGHT):
				image = 'curve_top-right.png'
			else:
				image = 'curve_top-left.png'
		self.source = image

	def draw_part(self, view, bodypart_type):
		self._set_image(bodypart_type)
		super(BodyPart, self).draw(view)


	def _has_directions(self, dir1, dir2):
		"""
		Checks if the current body part has these directions as src and destination directions.
		Doesn't matter in what order they appear.
		:return:
		"""
		if self._src_direction == dir1 and self._direction == dir2:
			return True
		elif self._src_direction == dir2 and self._direction == dir1:
			return True
		return False


class Snake:
	def __init__(self):
		self._body_parts = [BodyPart(INIT_X, INIT_Y, INIT_DIR, None)]

	def get_head(self):
		return self._body_parts[0]

	def change_direction(self, new_direction):
		head = self.get_head()
		if not new_direction == head.get_src_direction():
			head.set_direction(new_direction)

	def move(self):
		"""
		:return: boolean True if move is successful, False if game over
		"""
		print("Moving")
		# Check movement validity
		head = self._body_parts[0]
		direction = head.get_direction()
		new_pos = move_cell(head.get_x(), head.get_y(), direction)

		if not 0 <= new_pos[0] < CELLS_PER_ROW:
			return False
		if not 0 <= new_pos[1] < CELL_ROWS:
			return False
		for body_part in self._body_parts:
			if new_pos == (body_part.get_x(), body_part.get_y()):
				return False

		old_direction = head.get_direction()
		for body_part in self._body_parts:
			direction = body_part.get_direction()
			new_pos = move_cell(body_part.get_x(), body_part.get_y(), direction)
			body_part.set_x(new_pos[0])
			body_part.set_y(new_pos[1])
			body_part.set_src_direction(opposite_dir(direction))

			tmp = old_direction
			old_direction = body_part.get_direction()
			body_part.set_direction(tmp)

			print("Direction {} src-direction {}".format(body_part.get_direction(), body_part.get_src_direction()))

		return True

	def grow(self):
		tail = self._body_parts[-1]
		new_tail_pos = move_cell(tail.get_x(), tail.get_y(), tail.get_src_direction())
		new_tail = BodyPart(
			new_tail_pos[0],
			new_tail_pos[1],
			opposite_dir(tail.get_src_direction()),
			tail.get_src_direction())
		self._body_parts.append(new_tail)

	def draw(self, view):
		self._body_parts[0].draw_part(view, BodyPart.HEAD)
		for i in range(1, len(self._body_parts) - 1):
			body_i = self._body_parts[i]
			body_i.draw_part(view, BodyPart.BODY)
		if len(self._body_parts) > 1:
			self._body_parts[-1].draw_part(view, BodyPart.TAIL)

	def is_occupying(self, xpos, ypos):
		for body_part in self._body_parts:
			if body_part.get_x() == xpos and body_part.get_y() == ypos:
				return True
		return False
