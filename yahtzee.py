from random import *
from tkinter import *
from turtle import *
from time import *

# Future implementations:

# Basic best-score-for-now approach
# - Account for bonus for top section

# Artificially Intelligent Game
# - Come up with a data type for describing:
#     1. The number of each face required to score a non-zero value for each
#        scoring section.
#     2. Whether we are adding up all faces, or just the required faces
# - Integrate bellman equation to determine:
#     1. Best score to go for
#     2. Which dice to hold


# Default parameters for each die
SIDES = 6 # Number of sides of the die
DEFAULT_FACE = 6 # The number displayed on the dice at the beginning
DIE_SIZE = 50 # The pixel width/height of each die
FACE_SIDES = 4 # Number of sides of the face showing
FULL_ROTATION = 360 # Degrees for a full rotation
PADDING = 5 # Padding around each die

# Default parameters for the dice
DIE_NUM = 5 # The number of dice we're playing with
DICE_WIDTH = DIE_NUM * DIE_SIZE + (DIE_NUM + 1) * PADDING # Width of the dice
                                                          # widget
DICE_HEIGHT = DIE_SIZE + 2 * PADDING # Height of the dice widget

# Default parameters for the score sheet
SCORE_SHEET_HEIGHT = 400 # Height of the score sheet widget
SCORE_SHEET_WIDTH = 100 # Width of the score sheet widget

# Default parameters for the board
END_TURN_TEXT = "You must select a category to score this turn under!" # Text
                                                                       # that
                                                                       # appears
                                                                       # at the
                                                                       # end of
                                                                       # a turn
GAME_OVER_TEXT = "Game Over! Roll to start a new game" # Text that appears at
                                                       # game over
                                                       
# Default parameters for the holding buttons
HELD_COLOUR = 'red' # Colour of the die when it is held
NOT_HELD_COLOUR = 'black' # Colour of the die when it isn't held
HOLD_DIE_HEIGHT_FACTOR = 0.02 # Hold button to die size factor for height
HOLD_DIE_WIDTH_FACTOR = 0.1 # Hold button to die size factor for width

# Default parameters for rolling
ALLOWED_ROLLS = 3 # Maximum number of rolls allowed on each turn
ROLL_TEXT = 'Roll' # The text that appears on the roll button
ROLL_NUMBER_TEXT = 'Roll number' # The text that prefixes the roll number
STARTING_ROLL_NUMBER = 0 # The first roll number

# Bonus and totals titles
BONUS = '35 Bonus' # Bonus on upper section label
TOTAL = 'Total' # Denotes the total of the upper section before bonus
TOTAL_OF = 'Total of ' # Denotes the total of a section
UPPER_SECTION = 'Upper Section' # The title for the upper section
LOWER_SECTION = 'Lower Section' # The title for the lower section
GRAND_TOTAL = 'Grand Total' # The title for the grand total

# Upper section titles
ONES = 'Ones' # Title for ones
TWOS = 'Twos' # Title for twos
THREES = 'Threes' # Title for threes
FOURS = 'Fours' # Title for fours
FIVES = 'Fives' # Title for fives
SIXES = 'Sixes' # Title for sixes

# Lower section titles
THREE_OF_A_KIND = '3 of a kind' # Title for three of a kind
FOUR_OF_A_KIND = '4 of a kind' # Title for four of a kind
FULL_HOUSE = 'Full House' # Title for full house
LOW_STRAIGHT = 'Low Straight' # Title for low straight
HIGH_STRAIGHT = 'High Straight' # Title for high straight
YAHTZEE = 'Yahtzee' # Title for Yahtzee
CHANCE = 'Chance' # TItle for chance
YAHTZEE_BONUS = 'Yahtzee Bonus' # Title for Yahtzee bonus

# All section titles
SECTIONS = {UPPER_SECTION : [ONES,
                             TWOS,
                             THREES,
                             FOURS,
                             FIVES,
                             SIXES,
                             TOTAL,
                             BONUS,
                             TOTAL_OF + UPPER_SECTION],
            LOWER_SECTION : [THREE_OF_A_KIND,
                             FOUR_OF_A_KIND,
                             FULL_HOUSE,
                             LOW_STRAIGHT,
                             HIGH_STRAIGHT,
                             YAHTZEE,
                             CHANCE,
                             YAHTZEE_BONUS,
                             TOTAL_OF + LOWER_SECTION,
                             TOTAL_OF + UPPER_SECTION],
            '' : [GRAND_TOTAL]} # Denotes the section and subsection titles

# Upper section bonus parameters
BONUS_THRESH = (SIDES * (SIDES + 1) // 2) * 3 # Denotes the threshold for a
                                              # bonus
BONUS_SCORE = 35 # Denote the score received from reaching the threshold


class Die :
    """A die object for each die on the board."""

    def __init__(self, number, held=False) : 
        """Construct a die object with the given number.

        Parameters:
            number (int) -> the number of the face currently displayed on the die.
        """
        self.number = number

        # Describes whether we want to keep this dice at the current value for
        # the next roll or not
        self.held = held

        # RawTurtle object for drawing the die
        self._drawer = None

        # The side length of the die
        self.sideLength = None

    def get_number(self) :
        """Returns the number on the die currently displayed."""
        return self.number

    def get_held(self) :
        """Determines if we are holding this die or not."""
        return self.held

    def set_number(self, number) :
        """Sets the number displayed on the die to number.

        Parameters:
            number (int) -> the new number to be set to.
        """
        self.number = number

    def hold(self) :
        """Sets the class parameter held."""
        self.held = True

    def toggle_hold(self) :
        """Toggles the value of self.held"""
        self.held = not self.held

    def unhold(self) :
        """Clears the class parameter held."""
        self.held = False

    def roll(self) :
        """Randomises the number displayed on the die (if is not being held)."""
        if not self.get_held() :
            self.set_number(randint(1, SIDES))

    def get_size(self) :
        """Gets the side length of the die."""
        return self.sideLength

    def draw(self, screen, x, y, sideLength) :
        """Draws itself.

        Parameters:
            screen (TurtleScreen) -> a turtle screen to wrap the turtle in.
            x (int) -> the x position (in pixels).
            y (int) -> the y position (in pixels).
            sideLength (int) -> the side length of the die.
        """

        self.sideLength = sideLength

        # If we have drawn before, clear the drawing
        if self._drawer is not None :
            self._drawer.clear()
        else :
            # Set up the turtle
            self._drawer = RawTurtle(screen)
            self._drawer.hideturtle()
            screen.tracer(0)

        # Go to the desired position
        self._drawer.penup()
        self._drawer.goto(x, y)
        self._drawer.pendown()

        # Determines the color to show if the die is being held or not
        if self.held :
            self._drawer.color(HELD_COLOUR)
        else :
            self._drawer.color(NOT_HELD_COLOUR)

        # Draw a square for the die
        for _ in range(FACE_SIDES) :
            self._drawer.forward(sideLength)
            self._drawer.left(FULL_ROTATION // FACE_SIDES)

        # Draw the pattern
        self.draw_face(self._drawer, x, y, sideLength)
        screen.update()

    def draw_face(self, turtle, x, y, length) :
        """Draws the face of the die.

        Parameters:
            turtle (Turtle) -> the turtle object to draw with.
            x (int) -> the x position (in pixels).
            y (int) -> the y position (in pixels).
            length (int) -> the length of the die.
        """
        # Set up dot parameters
        dotRadius = length // 10
        spacing = (length - 6 * dotRadius) // 4
        turtle.penup()
        
        if self.number == 1 :
            # Draw a one on the face of the die
            dots = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        elif self.number == 2 :
            # Draw a two on the face of the die
            dots = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
        elif self.number == 3 :
            # Draw a three on the face of the die
            dots = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        elif self.number == 4 :
            # Draw a four on the face of the die
            dots = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
        elif self.number == 5 :
            # Draw a five on the face of the die
            dots = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        elif self.number == 6 :
            # Draw a six on the face of the die
            dots = [[1, 0, 1], [1, 0, 1], [1, 0, 1]]

        self.draw_dots(x, y, turtle, dots, dotRadius, spacing)

    def draw_dots(self, x, y, turtle, dots, dotRadius, spacing) :
        """Draws dots in a grid like fashion based on the input dots.

        Parameters:
            x (int) -> the x position (in pixels).
            y (int) -> the y position (in pixels).
            turtle (Turtle) -> the turtle object to draw with.
            dots (list<list<int>>) -> a list of lists of integers which represents
                                    a grid layout of dots (1 means a dot is
                                    there, 0 it's not)

                                    example ->

                                    dots = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                                         -> a three to be drawn as the face.
            dotRadius (int) -> the radius of each dot.
            spacing (int) -> the spacing between each dot.
        """
        for height, row in enumerate(dots) :
            # Iterate through each row
            for width, col in enumerate(row) :
                # Iterate through each column of that row
                if (col == 1) :
                    # Only draw circle if we are meant to
                    turtle.goto(x + spacing * (width + 1) + 2 * dotRadius *
                                width + dotRadius,
                                y + spacing * (height + 1) + 2 * dotRadius *
                                height )
                    turtle.pendown()
                    turtle.begin_fill()
                    turtle.circle(dotRadius)
                    turtle.end_fill()
                    turtle.penup()

    def __lt__(self, other) :
        return self.number < other.number

    def __sub__(self, other) :
        return self.number - other.number
            

class Dice :
    """An object to encompass the dice on the board."""

    def __init__(self, number=DIE_NUM, length=DIE_SIZE, padding=PADDING, dice=None) :
        """Construct a dice object which contains number die of x pixels wide
        by y pixels high each with padding pixels inbetween consecutive die.

        Parameters:
            number (int) -> the number of die to create (default is five for a
                          standard game of Yahtzee).
            length (int) -> the side length of each die in pixels.
            padding (int) -> the padding between consecutive die in pixels.
            dice (List<Die>) -> the dice to be represented.
        """
        self.number = number
        self._size = length
        self._padding = padding

        if not dice :
            # Creates each die
            self.create_dice()
        else :
            self._dice = dice

        # The canvas to draw the dice on
        self.canvas = None

    def count_all(self) :
        """Sums the value on the face of each die."""
        total = 0
        for die in self.get_dice() :
            total += die.get_number()

        return total

    def count(self, faceNumber) :
        """Counts the points w.r.t the face number.

        Parameters:
            faceNumber (int) -> the value of the face we wish to count.
        """
        total = 0
        for die in self.get_dice() :
            if die.get_number() == faceNumber :
                total += die.get_number()

        return total

    def get_number(self) :
        """Returns the number of die we're playing with."""
        return self.number

    def get_die_size(self) :
        """Returns the side length of each die."""
        return self._size

    def get_padding(self) :
        """Returns the padding between consecutive die."""
        return self._padding

    def create_dice(self) :
        """Creates each die.""" 
        # Sets the default value of the die to 6 when starting a new game
        self._dice = [Die(DEFAULT_FACE) for _ in range(self.number)]

    def roll(self) :
        """Rolls each of the die."""
        [die.roll() for die in self._dice]

    def get_dice(self) :
        """Returns the list of die owned."""
        return self._dice

    def change_value(self, die, value) :
        """Changes the value of a die to a given value.

        Parameters:
            die (int) -> the index in the dice list to change.
            value (int) -> the face value of the die to change to.
        """
        die.set_number(value)

    def draw(self, parent, width, height) :
        """Draws itself.

        Parameters:
            parent (Frame) -> the frame to put the dice in.
            width (int) -> the width of the dice widget.
            height (int) -> the height of the dice widget.
        """

        # Create a new canvas
        if self.canvas is None :
            self.canvas = Canvas(master = parent, width = width, height = height)
            self.canvas.pack(anchor=CENTER, pady=PADDING)

        # Set up the screen
        screen = TurtleScreen(self.canvas)
        startX = - width // 2
        startY = - height // 2

        # Draw each die
        for num, die in enumerate(self._dice) :
            die.draw(screen, startX + self._padding + num * (self._padding +
                     self._size), startY + self._padding, self._size)

    def clear(self) :
        """Clears the canvas.
        """
        self.canvas.delete("all")
        self.canvas = None

        for die in self._dice :
            die._drawer = None

    def copy(self) :
        """Creates a shallow copy of the object.
        """
        return Dice(self.number, self._size, self._padding, self._dice)

class Board :
    """An object to encompass all the elements of the game."""

    def __init__(self, width, height, scoreSheetWidth=SCORE_SHEET_WIDTH,
                 scoreSheetHeight=SCORE_SHEET_HEIGHT, scoreSheetX=None,
                 scoreSheetY=None, dieLength=DIE_SIZE, dicePadding=PADDING,
                 diceNumber=DIE_NUM, diceWidth=DICE_WIDTH,
                 diceHeight=DICE_HEIGHT) : 
        """Construct a board object of the given width and height on the root
        display (top left corner of board).

        Parameters:
            width (int) -> the width of the board.
            height (int) -> the height of the board.
            dieLength (int) -> the side length of each die.
            dicePadding (int) -> the padding between consecutive die.
            diceNumber (int) -> The number of die.
            diceWidth (int) -> The width of the dice widget.
            diceHeight (int) -> The height of the dice widget.
        """
        
        # Set up each element of the board
        self._dice = Dice(diceNumber, dieLength, dicePadding)
        self._scoreSheet = ScoreSheet(self._dice)
        self.rollButton = None
        self.parent = None
        self.rollNumber = 0
        self.rollNumberText = None
        self.holdButtonWidget = None
        self.hold_buttons = []

        # Save important parameters for the board
        self.width = width
        self.height = height
        
        # Save important parameters for the dice
        self.diceWidth = diceWidth
        self.diceHeight = diceHeight

    def get_score_sheet(self) :
        """Returns the score sheet object."""
        return self._scoreSheet

    def get_dice(self) :
        """Returns the dice object."""
        return self._dice

    def draw(self, parent) :
        """Draws itself.

        Parameters:
            parent (Frame) -> the frame which to put the board in.
        """
        self.parent = parent
        
        # Draw the dice widget and each die
        self.diceButtonWidget = Frame(self.parent)
        self.diceButtonWidget.pack(side=RIGHT, pady=50*PADDING, padx=PADDING,
                                   expand=True, fill=Y)
        self.redraw_dice()

        # Draw the hold buttons
        self.draw_hold_buttons()

        # Draw the score sheet
        self._scoreSheet.draw(self.parent)

        # Draw the roll button
        if self.rollButton is None :
            self.rollButton = Button(self.diceButtonWidget, text=ROLL_TEXT,
                                     command=self.roll_dice)
            self.rollButton.pack(pady=PADDING)
            self._scoreSheet.set_roll_button(self.rollButton)

        # Add a label to the game over widget
        self._scoreSheet.gameOverText = StringVar()
        self._scoreSheet.gameOverText.set("")
        self._scoreSheet.gameOverLabel = Label(self.parent,
                                    textvariable=self._scoreSheet.gameOverText)
        self._scoreSheet.gameOverLabel.pack()

        # Draw the roll label
        self.rollNumberText = StringVar()
        self.rollNumberText.set("{}: {}".format(ROLL_NUMBER_TEXT,
                                                self.rollNumber))
        self.rollLabel = Label(self.diceButtonWidget, textvariable=self.rollNumberText)
        self.rollLabel.pack(side=BOTTOM, padx=PADDING, pady=PADDING)

    def is_game_over(self) :
        """Determines if the game is over or not."""
        for section in self._scoreSheet.get_selection_buttons().keys() :

            # Check each subsection
            for subSection in self._scoreSheet.get_selection_buttons()[
                section].keys() :

                # If any radio buttons exist, then we still have at least one
                # turn left to use
                widgetType = self._scoreSheet.get_selection_buttons()[section][
                    subSection]
                if isinstance(widgetType, Radiobutton) :
                    return False

        return True
                
    def roll_dice(self) :
        """Rolls each of the die in the board's dice."""

        # Game over actions
        if self.is_game_over() :
            self.reset()
            self.rollNumber = STARTING_ROLL_NUMBER
            self._scoreSheet.gameOverText.set("")
            self._scoreSheet.reset_scores()

        # Update the roll number and roll the dice
        self.update_roll_number()
        self.get_dice().roll()
        self.redraw_dice()
        self.rollNumberText.set("{}: {}".format(ROLL_NUMBER_TEXT,
                                                self.rollNumber))

        # Enables the player to select which score to tally turn under
        if self.rollNumber != 0 :
            self._scoreSheet.enable_selection()

        # Only allows three rolls
        if self.rollNumber == ALLOWED_ROLLS :

            # Disable roll button until a selection is made
            self.rollButton['state'] = 'disabled'
            self._scoreSheet.gameOverText.set(END_TURN_TEXT)
            
            # Implement selecting which tab to score under
            self.reset()
            self.rollNumber = 0
            
    def game_over(self) :
        """Handles the game over case.
        """
        self.gameOverText.set(GAME_OVER_TEXT)
            

    def update_roll_number(self) :
        """Increments the roll number up to 3 iff we have not selected a tab
        to put the current roll as a score in."""
        if self._scoreSheet.need_to_reset() :
            self.reset()
            self.rollNumber = 1
        else :
            self.rollNumber += 1

    def reset(self) :
        """Resets the dice for the next round."""
        for die in self.get_dice().get_dice() :
            die.unhold()

    def draw_hold_buttons(self) :
        """Draws the hold buttons."""

        # Only draw the hold button widget if it isn't already there
        if self.holdButtonWidget is None :
            self.holdButtonWidget = Frame(self.diceButtonWidget)
            self.holdButtonWidget.pack()

        # Make a button for each die, then pack it to the left of the widget
        # above
        for die in self.get_dice().get_dice() :
            button = Button(self.holdButtonWidget,
                            command=lambda x=die: [self.toggle_hold(x),
                                                   self.redraw_dice()],
                            height=int(die.get_size() * HOLD_DIE_HEIGHT_FACTOR),
                            width=int(die.get_size() * HOLD_DIE_WIDTH_FACTOR))
            button.pack(side=LEFT, pady=PADDING, padx=PADDING)
            self.hold_buttons.append(button)

    def redraw_dice(self) :
        """Redraws the dice."""
        self._dice.draw(self.diceButtonWidget, self.diceWidth, self.diceHeight)

    def toggle_hold(self, die) :
        """Toggles the hold value of the respective die.

        Parameters:
            die (Die) -> the die object to toggle the hold value.
        """
        if self.rollNumber != 0 :
            die.toggle_hold()
            
        self.redraw_dice()                


class ScoreSheet :
    """An object to draw and update the score sheet of the current game."""

    def __init__(self, dice) :
        """Construct a score sheet object.

        Parameters:
            dice (List<Die>): the dice which will be scored.
        """
        
        self.dice = dice
        
        # The frame to encapsulate the score sheet widget
        self.frame = None

        # The frame which will display the score sheet widget
        self.parent = None

        # Determines if we need to reset the score sheet
        self.needToReset = False

        # Represents the current game's scores
        self.scores = {section : {subsection : 0 for subsection in
                                  SECTIONS[section]}
                       for section in SECTIONS}
        self.scoreLabels = {section : {subsection : StringVar() for subsection
                                       in SECTIONS[section]}
                            for section in SECTIONS}

        # Section frames
        self.sectionFrames = {}
        self.sectionNameFrames = {}
        self.sectionScoreFrames = {}
        self.sectionSelectFrames = {}
        self.sectionLabels = {}

        # Sub-section frames
        self.subNameFrames = {}
        self.subScoreFrames = {}
        self.subSelectFrames = {}
        self.selectNames = {}
        self.subScoreLabels = {}
        self.subLabels = {}
        self.selectButtons = {}
        self.selectVals = {}

    def set_roll_button(self, button) :
        """So the score sheet can re-enable the roll button."""
        self.rollButton = button

    def need_to_reset(self) :
        """Tells the board whether we have to reset for the next turn."""
        temp = self.needToReset
        self.needToReset = False
        return temp

    def draw(self, parent) :
        """Draws itself.

        Parameters:
            parent (Frame) -> the frame to put the score board on.
        """
        self.parent = parent

        # Creates a frame for the score sheet
        if self.frame is None :
            self.frame = Frame(self.parent)
            self.frame.pack(anchor=NW)

        self.shared = StringVar()
        self.shared.set('not chosen')

        # Create a frame for each section
        for sectNum, section in enumerate(self.scores.keys()) :

            # Section frame
            sectionFrame = Frame(self.frame)
            sectionFrame.pack(pady=PADDING)
            self.sectionFrames[section] = sectionFrame

            # Section name and subsection names
            sectionNameFrame = Frame(sectionFrame)
            sectionNameFrame.pack(anchor=NW)
            self.sectionNameFrames[section] = sectionNameFrame

            # Section labels
            sectionLabel = Label(sectionNameFrame, text=section)
            sectionLabel.pack()            
            self.sectionLabels[section] = sectionLabel

            # Section scores
            scoreFrame = Frame(sectionFrame)
            scoreFrame.pack(side=RIGHT, padx=15*PADDING)
            self.sectionScoreFrames[section] = scoreFrame

            # Section selection buttons
            selectFrame = Frame(sectionFrame)
            selectFrame.pack(side=RIGHT)
            self.sectionSelectFrames[section] = selectFrame        

            # Create nested dictionaries
            self.subNameFrames[section] = {}
            self.subScoreFrames[section] = {}
            self.subSelectFrames[section] = {}
            self.selectVals[section] = {}
            self.subScoreLabels[section] = {}
            self.subLabels[section] = {}
            self.selectButtons[section] = {}

            # Create a frame for each subsection
            for subNum, sub in enumerate(self.scoreLabels[section].keys()) :

                # Create a frame for each subsection name
                subNameFrame = Frame(sectionFrame)
                subNameFrame.pack(anchor=NW)
                self.subNameFrames[section][sub] = subNameFrame

                # Create a frame for each subsection score
                subScoreFrame = Frame(scoreFrame)
                subScoreFrame.pack(anchor=NE)
                self.subScoreFrames[section][sub] = subScoreFrame

                # Create a frame for each subsection button
                subSelectFrame = Frame(selectFrame)
                subSelectFrame.pack(anchor=NE)
                self.subSelectFrames[section][sub] = subSelectFrame
                var = IntVar()
                self.selectVals[section][sub] = var

                # Add each score
                self.scoreLabels[section][sub].set('0')
                scoreLabel = Label(scoreFrame, textvariable=self.scoreLabels[section][sub])
                scoreLabel.pack(anchor=NE, pady=2)
                self.subScoreLabels[section][sub] = scoreLabel

                # Add each name
                subName = Label(subNameFrame, text=sub)
                subName.pack(anchor=W, pady=3)
                self.subLabels[section][sub] = subName

                # Add each button (not for totals)
                if sub.find('Total') < 0 and sub[0:2] != '35' :
                    button = Radiobutton(subSelectFrame, value=sub,
                                         variable=self.shared,
                                         command=self.enable_confirmed)
                    button.configure(state=DISABLED)
                    button.pack(anchor=E, pady=1)
                    self.selectButtons[section][sub] = button

                else :
                    # Blank as we don't need a button here -> to keep the
                    # spacing looking right
                    blankSelect = Label(subSelectFrame)
                    blankSelect.pack(anchor=E)
                    self.selectButtons[section][sub] = blankSelect

        # Draw confirm button
        self.confirmButton = Button(scoreFrame, text='CONFIRM',
                                    command=self.update);
        self.confirmButton['state'] = 'disabled'
        self.confirmButton.pack(anchor=NW)

    def enable_confirmed(self) :
        """Enables the confirm button to be pressed."""
        self.confirmButton['state'] = 'normal'

    def reset_scores(self) :
        """Resets the scores for a new game."""
        for sNum, section in enumerate(self.scores.keys()) :
            for ssNum, sub in enumerate(self.scores[section].keys()) :

                # Reset scores
                self.scoreLabels[section][sub].set('{}'.format(0))
                self.scores[section][sub] = 0

                # Add each radio button (except for totals and bonuses)
                if sub.find('Total') < 0 and sub[0:2] != '35' :
                    subSelectFrame = self.subSelectFrames[section][sub]
                    button = Radiobutton(subSelectFrame, value=sub,
                                         variable=self.shared,
                                         command=self.enable_confirmed)
                    button.configure(state=DISABLED)
                    button.pack(anchor='e')
                    self.selectButtons[section][sub] = button
                
        self.shared.set('not chosen')
        self.disable_selection()
        self.needToReset = True
        self.updateTotals()

    def update(self) :
        """Updates the score based on the option which is selected and faces
        showing on the dice."""
        sectionUpdated, subSectionUpdated, score = None, None, None
        for section, sectionName in enumerate(self.get_selection_buttons().keys()) :
            for sub in self.get_selection_buttons()[sectionName].keys() :

                # Get the score for the selected subsection
                widgetType = self.get_selection_buttons()[sectionName][sub]
                if (isinstance(widgetType, Radiobutton) and widgetType['value'] ==
                   self.shared.get()):

                    # Update the score on the scoreboard
                    score = self.score_by_section(sectionName, self.shared.get())
                    self.scoreLabels[sectionName][self.shared.get()].set('{}'.format(
                        score))
                    self.scores[sectionName][self.shared.get()] = score

                    # Set the section and subsection updated
                    sectionUpdated, subSectionUpdated = sectionName, sub

                    # Remove the radio button
                    widgetType.destroy()
                    self.get_selection_buttons()[sectionName][sub] = None
                    break

        # Reset selection and allow for rolling
        self.disable_selection()
        self.needToReset = True
        self.updateTotals(sectionUpdated, subSectionUpdated, score)
        self.rollButton['state'] = 'normal'
        
        # Check game over
        self.gameOverText.set("")
        gameOver = True
        for section, frame in enumerate(self.get_selection_buttons().keys()) :
            for sectFrame in self.get_selection_buttons()[frame].keys() :
                widgetType = self.get_selection_buttons()[frame][sectFrame]
                if isinstance(widgetType, Radiobutton) :
                    gameOver = False

        # Game over condition
        if gameOver :
            self.gameOverText.set(GAME_OVER_TEXT)

    def updateTotals(self, sectionUpdated=None, subSectionUpdated=None,
                     score=None) :
        """Updates the total sections in the scoreboard.

        Parameters:
            sectionUpdated (str) -> the section updated.
            subSectionUpdated (str) -> the subsection updated.
            score (int) -> the new score.
        """

        # Just scored a turn
        if sectionUpdated :

            # Add the new score
            previousScore = self.scores[sectionUpdated][TOTAL_OF +
                                                        sectionUpdated]

            # Update section total
            if sectionUpdated != LOWER_SECTION :

                # Check if we just got the bonus
                if sectionUpdated == UPPER_SECTION and \
                   previousScore < BONUS_THRESH and \
                   previousScore + score >= BONUS_THRESH :

                    # Set the bonus
                    score += BONUS_SCORE
                    self.scores[sectionUpdated][BONUS] = BONUS_SCORE
                    self.scoreLabels[sectionUpdated][BONUS].set('{}'.format(
                        BONUS_SCORE))
                
                # Update the section total
                previousScore += score
                self.scores[sectionUpdated][TOTAL_OF + sectionUpdated] = \
                                                     previousScore
                self.scoreLabels[sectionUpdated][TOTAL_OF + sectionUpdated].set(
                    '{}'.format(previousScore))
                
            else :
                previousScore += score

            # Update the section total in the bottom section
            self.scores[LOWER_SECTION][TOTAL_OF + sectionUpdated] = \
                                                previousScore
            self.scoreLabels[LOWER_SECTION][TOTAL_OF + sectionUpdated].set(
                '{}'.format(previousScore))

            # Update the grand total
            self.scores[''][GRAND_TOTAL] += score
            self.scoreLabels[''][GRAND_TOTAL].set('{}'.format(self.scores[''][
                GRAND_TOTAL]))

        # Resetting the game
        else :
            for section in self.scores :
                for subSection in self.scores[section] :
                    self.scores[section][subSection] = 0

    def disable_selection(self) :
        """Disables being able to select any of the buttons or the confirm
        button."""

        # Disable the radio buttons
        for section in self.subSelectFrames.keys() :
            for sub in self.subSelectFrames[section].keys() :
                widgetType = self.get_selection_buttons()[section][sub]
                if isinstance(widgetType, Radiobutton) :
                    widgetType.configure(state=DISABLED)

        # Disable the confirmation button
        self.confirmButton['state'] = 'disabled'


    def score_by_section(self, section, subSection) :
        """Scores by section.

        Parameters:
            section (int) -> 0 means it's the upper section, 1 the lower
                             section.
            subSection (string) -> the subsection for the score to go under.
        """
        if section == UPPER_SECTION :
            # Upper section
            if subSection == ONES :
                return self.dice.count(1)
            elif subSection == TWOS :
                return self.dice.count(2)
            elif subSection == THREES :
                return self.dice.count(3)
            elif subSection == FOURS :
                return self.dice.count(4)
            elif subSection == FIVES :
                return self.dice.count(5)
            elif subSection == SIXES :
                return self.dice.count(6)

        else :
            # Lower section
            if subSection == THREE_OF_A_KIND :
                if self.n_of_a_kind(3) :
                    return self.dice.count_all()
            elif subSection == FOUR_OF_A_KIND :
                if self.n_of_a_kind(4) :
                    return self.dice.count_all()
            elif subSection == FULL_HOUSE :
                if self.full_house() :
                    return 25
            elif subSection == LOW_STRAIGHT :
                if self.straight(4) :
                    return 30
            elif subSection == HIGH_STRAIGHT :
                if self.straight(5) :
                    return 40
            elif subSection == YAHTZEE :
                if self.n_of_a_kind(5) :
                    return 50
            elif subSection == CHANCE :
                return self.dice.count_all()
            # Integrate Yahtzee Bonus
            elif subSection == YAHTZEE_BONUS :
                return 0

        return 0

    def n_of_a_kind(self, n) :
        """Checks if n number of die are the same.

        Parameters:
            n (int) -> the number of die which need to have the same face value.
        """
        diceValues = [die.number for die in self.dice.get_dice()]
        for dieValue in diceValues :
            if diceValues.count(dieValue) >= n :
                return True

        return False

    def full_house(self) :
        """Checks if the dice are in a full house state"""
        return len(set([die.number for die in self.dice.get_dice()])) == 2

    def straight(self, n) :
        """Checks if n dice have face values in sequence.

        Parameters:
            n (int) -> the number of dice to be in sequence.
        """
        sortedDice = sorted(set([die.number for die in self.dice.get_dice()]))
        inOrder = 0
        for dieNum, die in enumerate(sortedDice) :

            # Starting or continuing the sequence
            if not inOrder or die - sortedDice[dieNum - 1] == 1 :
                inOrder += 1

                # Met the condition
                if inOrder == n :
                    break

            # Reset the sequence
            else :
                inOrder = 1
                
        return inOrder >= n            
                
    def get_scores(self) :
        """Returns the scores for each section."""
        return self.scores

    def get_selection_buttons(self) :
        """Returns the select buttons."""
        return self.selectButtons

    def enable_selection(self) :
        """Allows all radio buttons to be able to be selected."""
        for frame in self.get_selection_buttons().keys() :
            for sectFrame in self.get_selection_buttons()[frame].keys() :
                if isinstance(self.get_selection_buttons()[frame][sectFrame],
                              Radiobutton) :
                    self.get_selection_buttons()[frame][sectFrame].configure(
                        state=NORMAL)

    def enable_confirmation(self) :
        """Allows the user to confirm the option for their score to be counted
        under."""
        pass
    
        
class GameFrame(Frame) :
    """An object to encompass all the GUIs involved with the game."""

    def __init__(self, parent=None, width=1000, height=700) :
        """Construct a game frame object of the given width and height for
        display.

        Parameters:
            parent (Tk) -> the root tk instance.
            width (int) -> the width of the board (in pixels).
            height (int) -> the height of the board (in pixels).
        """
        # Basic root setup
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.parent.title("Yahtzee")
        self.parent.geometry("{}x{}".format(width, height))
        self.parent.resizable(0, 0)

        # Will eventually setup main menu, highscores etc. but for
        # now, we'll just setup the game screen
        self.board = Board(800, 400)
        self.board.draw(self.parent)

    def get_board(self) :
        """Returns the board associated with the GameFrame."""
        return self.board
        
# This is what is actually run
if __name__ == "__main__" :
    root = Tk()
    game = GameFrame(root)
