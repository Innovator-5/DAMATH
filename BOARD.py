from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

# Set the window size
Window.size = (1370, 680)  # width, height


# Center the window on the screen
def center_window():
    screen_width = Window.system_size[1]
    screen_height = Window.system_size[1]
    window_width, window_height = Window.size
    x = (screen_width - window_width) / 20
    y = (screen_height - window_height) / 2
    Window.left = x
    Window.top = y


center_window()


# Damath Design Board Main
class DamathApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_background_color(main_layout, (166 / 255, 166 / 255, 166 / 255, 1))

        self.blue_score = 0
        self.red_score = 0
        self.current_turn = 'blue'  # Track whose turn it is


        # Scoring area
        scoring_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=200, spacing=10,
                                   pos_hint={'center_x': 0.1})

        # Player 1 Score and Label
        self.blue_score_label = Label(text="0 pts", font_size=35, color=[1, 1, 1, 1], bold=True, size_hint=(None, None),
                                      size=(250, 50))
        self.blue_label = Label(text="Player 1", font_size=35, color=[1, 1, 1, 1], bold=True, size_hint=(None, None),
                                size=(250, 50))
        self.add_background_color(self.blue_score_label, (0, 0, 1, 1))
        self.add_background_color(self.blue_label, (0, 0, 1, 1))

        # Center "vs" Label
        vs_label = Label(text="vs", font_size=26, color=[1, 1, 0, 1], bold=True, size_hint=(None, None), size=(60, 40))
        self.add_background_color(vs_label, (0, 0, 0, 1))

        # Player 2 Score and Label
        self.red_score_label = Label(text="0 pts", font_size=35, color=[1, 1, 1, 1], bold=True, size_hint=(None, None),
                                     size=(250, 50))
        self.red_label = Label(text="Player 2", font_size=35, color=[1, 1, 1, 1], bold=True, size_hint=(None, None),
                               size=(250, 50))
        self.add_background_color(self.red_score_label, (1, 0, 0, 1))
        self.add_background_color(self.red_label, (1, 0, 0, 1))

        # Add indicators
        self.blue_indicator = Indicator(color=[0.5, 0.5, 0.5, 1])  # Gray indicator for blue side
        self.red_indicator = Indicator(color=[0.5, 0.5, 0.5, 1])  # Gray indicator for red side

        # Add everything to scoring_layout
        scoring_layout.add_widget(self.blue_score_label)
        scoring_layout.add_widget(self.blue_indicator)
        scoring_layout.add_widget(self.blue_label)
        scoring_layout.add_widget(vs_label)
        scoring_layout.add_widget(self.red_label)
        scoring_layout.add_widget(self.red_indicator)
        scoring_layout.add_widget(self.red_score_label)

        # Container layout to center the board and numbers
        board_container = BoxLayout(orientation='vertical', size_hint=(None, None), width=450, height=550,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # BG Layout Number Size
        board = DamathBoard(app=self)  # Pass the app instance to the board
        bottom_numbers = NumbersLayout(orientation='horizontal', size=(496, 40))
        right_numbers = NumbersLayout(orientation='vertical', size=(45, 451.5))

        # Sub-container for Right Numbers
        board_with_right_numbers = BoxLayout(orientation='horizontal', size_hint=(None, None), width=495, height=450)
        board_with_right_numbers.add_widget(board)
        board_with_right_numbers.add_widget(right_numbers)

        board_container.add_widget(board_with_right_numbers)
        board_container.add_widget(bottom_numbers)

        main_layout.add_widget(scoring_layout)
        main_layout.add_widget(board_container)

        self.update_indicators()  # Set initial indicator colors
        return main_layout

    def add_background_color(self, widget, color):
        with widget.canvas.before:
            Color(*color)
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def update_score(self, color, points):
        pass

    def update_indicators(self):
        if self.current_turn == 'blue':
            self.blue_indicator.set_color([1, 1, 0, 1])  # Light up blue indicator
            self.red_indicator.set_color([0.5, 0.5, 0.5, 1])  # Turn red indicator to gray
        else:
            self.blue_indicator.set_color([0.5, 0.5, 0.5, 1])  # Turn blue indicator to gray
            self.red_indicator.set_color([1, 1, 0, 1])  # Light up red indicator

    def show_warning(self, message):
        content = BoxLayout(orientation='vertical', padding=10)

        # Set background color to white
        with content.canvas.before:
            Color(1, 1, 1, 1)
            content.rect = Rectangle(size=content.size, pos=content.pos)
            content.bind(pos=self.update_rect, size=self.update_rect)

        label = Label(text=message, font_size=20, color=[0, 0, 0, 1])  # Black text color
        content.add_widget(label)
        close_button = Button(text='OK', size_hint=(None, None), size=(100, 40), pos_hint={'center_x': 0.5})
        content.add_widget(close_button)

        popup = Popup(title='Invalid Move!',
                      content=content,
                      size_hint=(None, None),
                      size=(300, 200),
                      auto_dismiss=False)
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def update_rect(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


# Board Position
class Board(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.board_layout = DamathBoard(size_hint=(None, None), size=(450, 450))
        self.add_widget(self.board_layout)


# Black Square
class BlackSquares(Label):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# Brown Square
class BrownSquares(Button):
    def __init__(self, background_color, text_color, text, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = background_color
        self.color = text_color
        self.text = text
        self.font_size = 40
        self.bold = True


# Numbers Layout for Bottom and Right
class NumbersLayout(BoxLayout):
    def __init__(self, orientation='horizontal', **kwargs):
        super().__init__(orientation=orientation, size_hint=(None, None), **kwargs)
        self.spacing = 2
        self.add_background_color([0.8, 0.7, 0.5, 1])
        self.add_border()
        number_color = [0, 0, 0, 1]

        # Bottom Numbers
        if orientation == 'horizontal':
            for col in range(8):
                number_label = Label(text=str(col), color=number_color, font_size=20, size_hint_x=None, width=54.5,
                                     bold=True)
                self.add_widget(number_label)
        # Right Numbers
        else:
            for row in range(7, -1, -1):
                number_label = Label(text=str(row), color=number_color, font_size=20, size_hint_y=None, height=54.5,
                                     bold=True)
                self.add_widget(number_label)

    def add_background_color(self, color):
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_border(self):
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)
            self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)


# Damath Board Layout
class DamathBoard(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.cols = 8
        self.rows = 8
        self.add_border()
        self.selected_chip = None
        self.app = app  # Store a reference to the app
        self.create_board()

    # Border around the board
    def add_border(self):
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=3)
            self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def create_board(self):
        self.cells = []
        operations = [['+', '-', '-'], ['+', '-', '+'], ['-', '+', '+'], ['-', '+', '-'],
                      ['+', '-', '-'], ['+', '-', '+'], ['-', '+', '+'], ['-', '+', '-']]

        # Color of the Board
        brown_color = [0.8, 0.7, 0.5, 1]
        black_color = (0, 0, 0, 1)
        # Color of the Chips
        red_color = [1, 0, 0, 1]
        blue_color = [0, 0, 1, 1]
        # Chips number and position
        red_numbers = [1, 6, 8, 4, 10, 5, 2, 11, 9, 3, 7, 12]
        blue_numbers = [1, 6, 8, 4, 5, 2, 11, 10, 9, 3, 7, 12]

        self.red_positions = [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3), (1, 5), (1, 7),
                              (2, 0), (2, 2), (2, 4), (2, 6)]
        self.blue_positions = [(5, 1), (5, 3), (5, 5), (5, 7), (6, 0), (6, 2), (6, 4), (6, 6),
                               (7, 1), (7, 3), (7, 5), (7, 7)]
        # Chips Design
        for row in range(8):
            row_cells = []
            for col in range(8):
                cell_layout = AnchorLayout()
                if (row + col) % 2 == 0:
                    text = operations[row][col % 3]
                    square = BrownSquares(background_color=brown_color, text_color=(0, 0, 0, 1), text=text)
                    cell_layout.add_widget(square)
                    if (row, col) in self.red_positions:
                        number = red_numbers.pop()
                        chip = Chip(color=red_color, number=number, size_hint=(None, None), size=(40, 40), player='red')
                        chip.row = row
                        chip.col = col
                        cell_layout.add_widget(chip)
                    elif (row, col) in self.blue_positions:
                        number = blue_numbers.pop()
                        chip = Chip(color=blue_color, number=number, size_hint=(None, None), size=(40, 40),
                                    player='blue')
                        chip.row = row
                        chip.col = col
                        cell_layout.add_widget(chip)
                    square.bind(on_press=self.on_square_press)
                else:
                    square = BlackSquares(color=black_color)
                    cell_layout.add_widget(square)
                self.add_widget(cell_layout)
                row_cells.append(cell_layout)
            self.cells.append(row_cells)

    # Chips Functions
    def on_square_press(self, instance):
        cell = instance.parent
        row, col = self.get_cell_position(cell)
        if self.selected_chip:
            if self.is_valid_move(row, col):
                old_cell = self.cells[self.selected_chip.row][self.selected_chip.col]
                old_cell.remove_widget(self.selected_chip)
                cell.add_widget(self.selected_chip)
                self.selected_chip.row = row
                self.selected_chip.col = col
                self.update_positions()

                # Check for jumps (eaten chips)
                self.check_jumps(old_cell, cell)

                # Check if the chip reached the end row and make it a king
                if (self.selected_chip.player == 'blue' and row == 0) or (
                        self.selected_chip.player == 'red' and row == 7):
                    self.selected_chip.is_king = True

                self.selected_chip = None
                self.switch_turn()
            else:
                self.selected_chip = None  # Cancel the chip selection if the move is invalid
        else:
            for chip in cell.children:
                if isinstance(chip, Chip) and chip.player == self.app.current_turn:
                    self.selected_chip = chip
                    break

    def is_same_color_chip_in_path(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            return False  # No chip can be in the path for single-step moves

        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        mid_cell = self.cells[mid_row][mid_col]

        for chip in mid_cell.children:
            if isinstance(chip, Chip) and chip.player == self.selected_chip.player:
                return True  # There's a chip of the same color in the path

        return False

    def capture_chip(self, chip):
        # Remove the captured chip from the board
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if chip in self.cells[row][col].children:
                    self.cells[row][col].remove_widget(chip)
                    if chip.player == 'blue':
                        self.blue_positions.remove((row, col))
                    elif chip.player == 'red':
                        self.red_positions.remove((row, col))
                    return

    def is_valid_king_move(self, start_row, start_col, end_row, end_col):
        # Check if the move is diagonal
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        direction_row = 1 if end_row > start_row else -1
        direction_col = 1 if end_col > start_col else -1

        current_row = start_row + direction_row
        current_col = start_col + direction_col

        while current_row != end_row and current_col != end_col:
            for widget in self.cells[current_row][current_col].children:
                if isinstance(widget, Chip):
                    if widget.player == self.selected_chip.player:
                        self.app.show_warning("Invalid Move! A king cannot jump over a chip of the same color.")
                        return False
                    else:
                        # Capture the chip
                        self.capture_chip(widget)
            current_row += direction_row
            current_col += direction_col

        return True

    def is_valid_move(self, row, col):
        # Check if the target cell is empty
        target_cell = self.cells[row][col]
        for widget in target_cell.children:
            if isinstance(widget, Chip):
                self.app.show_warning("The target cell is occupied!")
                return False  # Invalid move if the target cell is occupied by any chip

        # Calculate row and column difference
        row_diff = row - self.selected_chip.row
        col_diff = col - self.selected_chip.col

        is_backward_move = (self.selected_chip.player == 'blue' and row_diff > 0) or (
                self.selected_chip.player == 'red' and row_diff < 0)

        if self.selected_chip.is_king:
            # King chips can move diagonally in any direction and capture chips
            if abs(row_diff) == abs(col_diff):
                # Check if there's an opposite color chip in the diagonal path
                direction_row = 1 if row_diff > 0 else -1
                direction_col = 1 if col_diff > 0 else -1
                current_row = self.selected_chip.row + direction_row
                current_col = self.selected_chip.col + direction_col
                while current_row != row and current_col != col:
                    for chip in self.cells[current_row][current_col].children:
                        if isinstance(chip, Chip) and chip.player != self.selected_chip.player:
                            # Capture the chip
                            self.capture_chip(chip)
                            return True

                self.app.show_warning("Invalid Move! No capture in diagonal path.")
                return False

            self.app.show_warning("Invalid Move! Kings can only move diagonally.")
            return False

        else:
            # Check if the move is a valid forward diagonal move (one square)
            if abs(row_diff) == 1 and abs(col_diff) == 1 and not is_backward_move:
                return True
            # Check if the move is a valid capture move (two squares)
            elif abs(row_diff) == 2 and abs(col_diff) == 2:
                mid_row = (self.selected_chip.row + row) // 2
                mid_col = (self.selected_chip.col + col) // 2
                if (mid_row, mid_col) in self.red_positions or (mid_row, mid_col) in self.blue_positions:
                    if not self.is_same_color_chip_in_path(self.selected_chip.row, self.selected_chip.col, row, col):
                        return True

            self.app.show_warning("Invalid Move! Try Again.")  # Call show_warning method
            return False

    def check_jumps(self, old_cell, new_cell):
        old_row, old_col = self.get_cell_position(old_cell)
        new_row, new_col = self.get_cell_position(new_cell)

        if abs(old_row - new_row) == 2 and abs(old_col - new_col) == 2:
            jumped_row = (old_row + new_row) // 2
            jumped_col = (old_col + new_col) // 2
            jumped_cell = self.cells[jumped_row][jumped_col]

            for chip in jumped_cell.children:
                if isinstance(chip, Chip) and chip.player != self.app.current_turn:
                    self.apply_operation(self.selected_chip, chip, new_row, new_col)
                    jumped_cell.remove_widget(chip)
                    break

    def apply_operation(self, capturing_chip, captured_chip, row, col):
        cell = self.cells[row][col]
        operations = [child.text for child in cell.children if isinstance(child, BrownSquares)]

        results = []
        for operation in operations:
            if operation == '+':
                result = capturing_chip.number + captured_chip.number
            elif operation == '-':
                result = capturing_chip.number - captured_chip.number
            results.append(result)

        best_result = max(results)  # Choose the best result (you can change this to min if needed)

        # Update the scoreboard directly
        if capturing_chip.player == 'blue':
            self.app.blue_score += best_result
            self.app.blue_score_label.text = f"{self.app.blue_score} pts"
        elif capturing_chip.player == 'red':
            self.app.red_score += best_result
            self.app.red_score_label.text = f"{self.app.red_score} pts"

    def get_cell_position(self, cell):
        for row in range(8):
            for col in range(8):
                if self.cells[row][col] == cell:
                    return row, col
        return None

    def update_positions(self):
        self.red_positions = [(chip.row, chip.col) for row in self.cells for cell in row for chip in cell.children if
                              isinstance(chip, Chip) and chip.color == [1, 0, 0, 1]]
        self.blue_positions = [(chip.row, chip.col) for row in self.cells for cell in row for chip in cell.children if
                               isinstance(chip, Chip) and chip.color == [0, 0, 1, 1]]

    def switch_turn(self):
        self.app.current_turn = 'red' if self.app.current_turn == 'blue' else 'blue'
        self.app.update_indicators()


# Chips
class Chip(Widget):
    def __init__(self, color, number, player, **kwargs):
        super().__init__(**kwargs)
        self.number = number  # Number assigned to the chip
        self.color = color  # Color assigned to the chip
        self.player = player  # Assign player to the chip
        self.is_king = False  # New property to indicate if the chip has reached the end row
        with self.canvas:
            Color(*color)
            size = 40  # Adjusted size to fit within the box
            self.ellipse = Ellipse(size=(size, size), pos=self.pos)
            self.bind(pos=self._update_ellipse, size=self._update_ellipse)
            # Add a border around the chip
            Color(0, 0, 0, 1)
            self.border = Line(circle=(self.center_x, self.center_y, size / 2), width=2)
            self.bind(pos=self._update_border, size=self._update_border)
        self.label = Label(text=str(self.number), color=(0, 0, 0, 1), font_size=20, bold=True)
        self.add_widget(self.label)

    def _update_ellipse(self, instance, value):
        size = min(instance.size)
        self.ellipse.pos = (instance.center_x - size / 2, instance.center_y - size / 2)
        self.ellipse.size = (size, size)
        self.label.size = self.size
        self.label.pos = (self.center_x - self.label.width / 2, self.center_y - self.label.height / 2)

    def _update_border(self, instance, value):
        size = min(instance.size)
        self.border.circle = (instance.center_x, instance.center_y, size / 2)

    def remove(self):
        # Remove the chip from its parent widget (i.e., the cell layout)
        self.parent.remove_widget(self)


# Indicator Circle
class Indicator(Label):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.size_hint = (None, None)
        self.width = self.height = 40
        with self.canvas.before:
            Color(*color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

    def set_color(self, color):
        self.color = color
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            self.bind(pos=self.update_circle, size=self.update_circle)


if __name__ == '__main__':
    DamathApp().run()