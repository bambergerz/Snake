# snake.py
# Created by Zachary Bamberger (zeb3) and Yishai Gronich

"""Primary module for Breakout application

This module contains the main controller class for the Snake application."""

from playSnake import *


class Snake(GameApp):
	def start(self):
		"""Initializes the application.

		This method is distinct from the built-in initializer __init__ (which you
		should not override or change). This method is called once the game is running.
		You should use it to initialize any game specific attributes.

		This method should make sure that all of the attributes satisfy the given
		invariants. When done, it sets the _state to STATE_INACTIVE and create a message
		(in attribute _mssg) saying that the user should press to play a game."""
		# IMPLEMENT ME

		# create opening text:
		print 'initiating game...'
		initial_text = 'Press any Key to play!!!'
		initial_font_size = 24
		initial_font_name = 'TimesBoldItalic.ttf'
		initial_bold = True
		initial_halign = 'center'
		initial_valign = 'middle'

		self._time = 0
		self._is_paused = False
		self._keys_in_last_frame = 0

		self._state = STATE_INACTIVE
		self._game = None
		self._mssg = GLabel(x=GAME_WIDTH / 2, y=GAME_HEIGHT / 2, text=initial_text,
		                    font_size=initial_font_size, font_name=initial_font_name,
		                    bold=initial_bold, halign=initial_halign, valign=initial_valign)

		Clock.schedule_interval(self.tick, 1. / SNAKE_SPEED)

	def update(self, dt):
		"""Animates a single frame in the game.

		It is the method that does most of the work. It is NOT in charge of playing the
		game.  That is the purpose of the class Play.  The primary purpose of this
		game is to determine the current state, and -- if the game is active -- pass
		the input to the Play object _game to play the game.

		As part of the assignment, you are allowed to add your own states.  However, at
		a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
		STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
		thing, and so should have its own helper.  We describe these below.

		STATE_INACTIVE: This is the state when the application first opens.  It is a
		paused state, waiting for the player to start the game.  It displays a simple
		message on the screen.

		STATE_NEWGAME: This is the state creates a new game and shows it on the screen.
		This state only lasts one animation frame before switching to STATE_COUNTDOWN.

		STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is
		served.  The player can move the paddle during the countdown, but there is no
		ball on the screen.  Paddle movement is handled by the Play object.  Hence the
		Play class should have a method called updatePaddle()

		STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
		paddle and the ball moves on its own about the board.  Both of these
		should be handled by methods inside of class Play (NOT in this class).  Hence
		the Play class should have methods named updatePaddle() and updateBall().

		STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
		still visible on the screen.

		The rules for determining the current state are as follows.

		STATE_INACTIVE: This is the state at the beginning, and is the state so long
		as the player never presses a key.  In addition, the application switches to
		this state if the previous state was STATE_ACTIVE and the game is over
		(e.g. all balls are lost or no more bricks are on the screen).

		STATE_NEWGAME: The application switches to this state if the state was
		STATE_INACTIVE in the previous frame, and the player pressed a key.

		STATE_COUNTDOWN: The application switches to this state if the state was
		STATE_NEWGAME in the previous frame (so that state only lasts one frame).

		STATE_ACTIVE: The application switches to this state after it has spent 3
		seconds in the state STATE_COUNTDOWN.

		STATE_INT_PAUSED: The application switches to this state if the state was STATE_ACTIVE
		in the previous frame, and the player pressed 'escape' to pause the game intentionally.
		Leaving this state will require pressing the spacebar.

		STATE_PAUSED: The application switches to this state if the state was
		STATE_ACTIVE in the previous frame, the ball was lost, and there are still
		some tries remaining.

		STATE_COMPLETE: The application switches to this state if the state was STATE_ACTIVE
		in the previous frame, the ball was lost, and there are no lives remaining. Alternatively,
		the player can reach this stage by destroying all the bricks.

		You are allowed to add more states if you wish. Should you do so, you should
		describe them here.

		Parameter dt: The time in seconds since last update
		Precondition: dt is a number (int or float)
		"""

		# Assertions:
		assert type(dt) == int or type(dt) == float
		print 'self._state is ' + str(self._state)

		# from STATE_INACTIVE to STATE_NEWGAME:
		if self._state == STATE_INACTIVE and self._from_inactive_to_newgame():
			self._state = STATE_NEWGAME
			self._time = 0
			self._game = Play()

		# from STATE_NEWGAME to STATE_COUNTDOWN:
		elif self._state == STATE_NEWGAME:
			self._state = STATE_COUNTDOWN

		# from STATE_COUNTDOWN to STATE_ACTIVE
		elif self._state == STATE_COUNTDOWN:
			self._countdown(self._time)

		elif self._state == STATE_ACTIVE:
			if self.input.key_count == 1:
				direction = None
				if self.input.is_key_down('left'):
					direction = LEFT
				elif self.input.is_key_down('right'):
					direction = RIGHT
				elif self.input.is_key_down('up'):
					direction = UP
				elif self.input.is_key_down('down'):
					direction = DOWN
				if direction is not None:
					self._game.update_snake_direction(direction)
		elif self._state == STATE_COMPLETE:
			if self.input.is_key_down('spacebar'):
				self._state = STATE_NEWGAME
				self._time = 0
				self._game = Play()


	def draw(self):
		"""Draws the game objects to the view.

		Every single thing you want to draw in this game is a GObject.  To draw a GObject
		g, simply use the method g.draw(self.view).  It is that easy!

		Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play.
		In order to draw them, you either need to add getters for these attributes or you
		need to add a draw method to class Play.  We suggest the latter.  See the example
		subcontroller.py from class."""
		# IMPLEMENT ME
		# print str(self._state)
		if self._state == STATE_INACTIVE:
			self._mssg.draw(self.view)
		elif self._state == STATE_NEWGAME:
			self._game.draw_me(self.view)
		elif self._state == STATE_COUNTDOWN:
			self._game.draw_me(self.view)
			self._mssg.draw(self.view)
		elif self._state == STATE_ACTIVE:
			self._game.draw_me(self.view)
		elif self._state == STATE_COMPLETE:
			self._game.draw_me(self.view)
			self._mssg.draw(self.view)

	def _from_inactive_to_newgame(self):
		"""Returns: True if a key has been pressed and no key was pressed in previous frame, False otherwise.

		implemented on the basis of Walker White's "State" module, written on Movember 17, 2015. Worked around notion
		of checking the number of frames in both the current and previous screen. Implemented the idea that we should
		only consider instances in which a new key is pressed in the current frame, but none were in the previous one.

		Parameter old_keys: the number of keys pressed in the previous frame. This is an optional parameter, and will initially be 0.
		Precondition: old_keys is an integer greater than or equal to 0."""


		# change occurs if at least one key is being pressed and the amount of keys pressed in the last frame was 0
		new_keys = self.input.key_count
		# print 'old_keys is ' + str(old_keys)
		# print 'new_keys is ' + str(new_keys)
		validity = new_keys > 0 and self._keys_in_last_frame == 0
		self._keys_in_last_frame = new_keys
		return validity

	def _countdown(self, time):
		"""During STATE_COUNTDOWN, Counts down from 3 to 0 on the screen and then switches to STATE_ACTIVE.

		There are 62.5 frames per second assuming update goes through one fram every 16 miliseconds. Therefore,
		every second we will change the text that is to be displayed on the screen. Once three seconds have gone by,
		we will change the state to active

		Parameter time: The amount of time which has passed since self._State has become STATE_COUNTDOWN
		Precondition: time is a float greater than or equal to zero"""

		# print 'state is countdown'
		if time < 62.5:
			text = '3'
		# print 'text = 3'
		# print 'time = ' + str(time)
		elif 62.5 <= time < 125.0:
			text = '2'
		# print 'text = 2'
		# print 'time = ' + str(time)
		elif 125.0 <= time < 187.5:
			text = '1'
		# print 'text = 1'
		# print 'time = ' + str(time)
		else:
			self._state = STATE_ACTIVE
			text = 'LAUNCH!!!'
		self._mssg.text = text
		self._mssg.font_size = 24

		self._time += 1

	def tick(self, dt):

		if self._state == STATE_ACTIVE:
			if not self._game.tick():
				self.end_game()

			return True

	def end_game(self):
		self._state = STATE_COMPLETE
		self._mssg.font_size = 24
		self._mssg.text = "GAME OVER: Press Space-Bar to Restart"
		
=======
# snake.py
# Created by Zachary Bamberger (zeb3) and Yishai Gronich

"""Primary module for Breakout application

This module contains the main controller class for the Snake application."""

from playSnake import *


class Snake(GameApp):
	def start(self):
		"""Initializes the application.

		This method is distinct from the built-in initializer __init__ (which you
		should not override or change). This method is called once the game is running.
		You should use it to initialize any game specific attributes.

		This method should make sure that all of the attributes satisfy the given
		invariants. When done, it sets the _state to STATE_INACTIVE and create a message
		(in attribute _mssg) saying that the user should press to play a game."""
		# IMPLEMENT ME
		assert (isinstance(self.view, GView) or self.view is None, 'view is not an instance of GView or None')
		assert (isinstance(self.input, GInput) or self.input is None, 'input is not an instance of GInput or None')

		# create opening text:
		print 'initiating game...'
		initial_text = 'Press any Key to play!!!'
		initial_font_size = 36
		initial_font_name = 'TimesBoldItalic.ttf'
		initial_bold = True
		initial_halign = 'center'
		initial_valign = 'middle'

		self._time = 0
		self._is_paused = False
		self._keys_in_last_frame = 0

		self._state = STATE_INACTIVE
		self._game = None
		self._mssg = GLabel(x=GAME_WIDTH / 2, y=GAME_HEIGHT / 2, text=initial_text,
		                    font_size=initial_font_size, font_name=initial_font_name,
		                    bold=initial_bold, halign=initial_halign, valign=initial_valign)

		Clock.schedule_interval(self.tick, 1. / SNAKE_SPEED)

	def update(self, dt):
		"""Animates a single frame in the game.

		It is the method that does most of the work. It is NOT in charge of playing the
		game.  That is the purpose of the class Play.  The primary purpose of this
		game is to determine the current state, and -- if the game is active -- pass
		the input to the Play object _game to play the game.

		As part of the assignment, you are allowed to add your own states.  However, at
		a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
		STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
		thing, and so should have its own helper.  We describe these below.

		STATE_INACTIVE: This is the state when the application first opens.  It is a
		paused state, waiting for the player to start the game.  It displays a simple
		message on the screen.

		STATE_NEWGAME: This is the state creates a new game and shows it on the screen.
		This state only lasts one animation frame before switching to STATE_COUNTDOWN.

		STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is
		served.  The player can move the paddle during the countdown, but there is no
		ball on the screen.  Paddle movement is handled by the Play object.  Hence the
		Play class should have a method called updatePaddle()

		STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
		paddle and the ball moves on its own about the board.  Both of these
		should be handled by methods inside of class Play (NOT in this class).  Hence
		the Play class should have methods named updatePaddle() and updateBall().

		STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
		still visible on the screen.

		The rules for determining the current state are as follows.

		STATE_INACTIVE: This is the state at the beginning, and is the state so long
		as the player never presses a key.  In addition, the application switches to
		this state if the previous state was STATE_ACTIVE and the game is over
		(e.g. all balls are lost or no more bricks are on the screen).

		STATE_NEWGAME: The application switches to this state if the state was
		STATE_INACTIVE in the previous frame, and the player pressed a key.

		STATE_COUNTDOWN: The application switches to this state if the state was
		STATE_NEWGAME in the previous frame (so that state only lasts one frame).

		STATE_ACTIVE: The application switches to this state after it has spent 3
		seconds in the state STATE_COUNTDOWN.

		STATE_INT_PAUSED: The application switches to this state if the state was STATE_ACTIVE
		in the previous frame, and the player pressed 'escape' to pause the game intentionally.
		Leaving this state will require pressing the spacebar.

		STATE_PAUSED: The application switches to this state if the state was
		STATE_ACTIVE in the previous frame, the ball was lost, and there are still
		some tries remaining.

		STATE_COMPLETE: The application switches to this state if the state was STATE_ACTIVE
		in the previous frame, the ball was lost, and there are no lives remaining. Alternatively,
		the player can reach this stage by destroying all the bricks.

		You are allowed to add more states if you wish. Should you do so, you should
		describe them here.

		Parameter dt: The time in seconds since last update
		Precondition: dt is a number (int or float)
		"""

		# Assertions:
		assert type(dt) == int or type(dt) == float

		# from STATE_INACTIVE to STATE_NEWGAME:
		if self._state == STATE_INACTIVE and self._from_inactive_to_newgame():
			self._state = STATE_NEWGAME
			self._time = 0
			self._game = Play()

		# from STATE_NEWGAME to STATE_COUNTDOWN:
		elif self._state == STATE_NEWGAME:
			self._state = STATE_COUNTDOWN

		# from STATE_COUNTDOWN to STATE_ACTIVE
		elif self._state == STATE_COUNTDOWN:
			self._countdown(self._time)

		elif self._state == STATE_ACTIVE:
			if self.input.key_count == 1:
				direction = None
				if self.input.is_key_down('left'):
					direction = LEFT
				elif self.input.is_key_down('right'):
					direction = RIGHT
				elif self.input.is_key_down('up'):
					direction = UP
				elif self.input.is_key_down('down'):
					direction = DOWN
				if direction is not None:
					self._game.update_snake_direction(direction)
		elif self._state == STATE_COMPLETE:
			if self.input.is_key_down('spacebar'):
				self._state = STATE_NEWGAME
				self._time = 0
				self._game = Play()


	def draw(self):
		"""Draws the game objects to the view.

		Every single thing you want to draw in this game is a GObject.  To draw a GObject
		g, simply use the method g.draw(self.view).  It is that easy!

		Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play.
		In order to draw them, you either need to add getters for these attributes or you
		need to add a draw method to class Play.  We suggest the latter.  See the example
		subcontroller.py from class."""
		# IMPLEMENT ME
		# print str(self._state)
		if self._state == STATE_INACTIVE:
			self._mssg.draw(self.view)
		elif self._state == STATE_NEWGAME:
			self._game.draw_me(self.view)
		elif self._state == STATE_COUNTDOWN:
			self._game.draw_me(self.view)
			self._mssg.draw(self.view)
		elif self._state == STATE_ACTIVE:
			self._game.draw_me(self.view)
		elif self._state == STATE_COMPLETE:
			self._game.draw_me(self.view)
			self._mssg.draw(self.view)

	def _from_inactive_to_newgame(self):
		"""Returns: True if a key has been pressed and no key was pressed in previous frame, False otherwise.

		implemented on the basis of Walker White's "State" module, written on Movember 17, 2015. Worked around notion
		of checking the number of frames in both the current and previous screen. Implemented the idea that we should
		only consider instances in which a new key is pressed in the current frame, but none were in the previous one.

		Parameter old_keys: the number of keys pressed in the previous frame. This is an optional parameter, and will initially be 0.
		Precondition: old_keys is an integer greater than or equal to 0."""


		# change occurs if at least one key is being pressed and the amount of keys pressed in the last frame was 0
		new_keys = self.input.key_count
		# print 'old_keys is ' + str(old_keys)
		# print 'new_keys is ' + str(new_keys)
		validity = new_keys > 0 and self._keys_in_last_frame == 0
		self._keys_in_last_frame = new_keys
		return validity

	def _countdown(self, time):
		"""During STATE_COUNTDOWN, Counts down from 3 to 0 on the screen and then switches to STATE_ACTIVE.

		There are 62.5 frames per second assuming update goes through one fram every 16 miliseconds. Therefore,
		every second we will change the text that is to be displayed on the screen. Once three seconds have gone by,
		we will change the state to active

		Parameter time: The amount of time which has passed since self._State has become STATE_COUNTDOWN
		Precondition: time is a float greater than or equal to zero"""

		# print 'state is countdown'
		if time < 62.5:
			text = '3'
		# print 'text = 3'
		# print 'time = ' + str(time)
		elif 62.5 <= time < 125.0:
			text = '2'
		# print 'text = 2'
		# print 'time = ' + str(time)
		elif 125.0 <= time < 187.5:
			text = '1'
		# print 'text = 1'
		# print 'time = ' + str(time)
		else:
			self._state = STATE_ACTIVE
			text = 'LAUNCH!!!'
		self._mssg.text = text
		self._mssg.font_size = 36

		self._time += 1

	def tick(self, dt):

		if self._state == STATE_ACTIVE:
			if not self._game.tick():
				self.end_game()

			return True

	def end_game(self):
		self._state = STATE_COMPLETE
		self._mssg.font_size = 24
		self._mssg.text = "GAME OVER: Press Space-Bar to Restart"

