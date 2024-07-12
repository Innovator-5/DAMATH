from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class Scoreboard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player1_score = 34
        self.player2_score = 27
        self.result = "WINS"
        self.bind(size=self.update_rectangles, pos=self.update_rectangles)
        self.rect1 = None
        self.square1 = None
        self.rect2 = None
        self.square2 = None

    def update_rectangles(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            self.rect1 = Rectangle(pos=(self.center_x - 450, self.center_y + 75), size=(700, 200))

            Color(1, 0, 0, 1)
            self.square1 = Rectangle(pos=(self.center_x + 250, self.center_y + 75), size=(200, 200))

            Color(0.8, 0.8, 0.8, 1)
            self.rect2 = Rectangle(pos=(self.center_x - 450, self.center_y - 175), size=(700, 200))

            Color(0, 0, 1, 1)
            self.square2 = Rectangle(pos=(self.center_x + 250, self.center_y - 175), size=(200, 200))

class ScoreboardApp(App):
    def build(self):
        root = FloatLayout()

        with root.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.bg_rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self.update_background, pos=self.update_background)

        scoreboard_title = Label(text='Scoreboard', color=(1, 1, 1, 1), size_hint=(None, None), size=(400, 100),
                                 pos_hint={'center_x': 0.5, 'top': 0.95}, font_size='60sp', bold=True)
        root.add_widget(scoreboard_title)

        scoreboard = Scoreboard()
        root.add_widget(scoreboard)

        player1_label = Label(text='Player 1', color=(1, 0, 0, 1), size_hint=(None, None), size=(100, 50),
                              pos_hint={'x': 0.30, 'y': 0.70}, font_size='20sp')
        root.add_widget(player1_label)

        player2_label = Label(text='Player 2', color=(0, 0, 1, 1), size_hint=(None, None), size=(100, 50),
                              pos_hint={'x': 0.30, 'y': 0.45}, font_size='20sp')
        root.add_widget(player2_label)

        self.wins_label = Label(text=scoreboard.result, bold=True, font_size='40sp', color=(0, 0, 0, 1), size_hint=(None, None),
                           size=(200, 50), pos_hint={'x': 0.40, 'center_y': 0.7})
        root.add_widget(self.wins_label)

        self.lose_label = Label(text="LOSE" if scoreboard.result == "WINS" else "WINS", bold=True, font_size='40sp', color=(0, 0, 0, 1), size_hint=(None, None),
                           size=(200, 50), pos_hint={'x': 0.40, 'y': 0.4})
        root.add_widget(self.lose_label)

        self.player1_score_label = Label(text=str(scoreboard.player1_score), bold=True, font_size='40sp', color=(1, 1, 1, 1), size_hint=(None, None),
                                         size=(200, 50), pos_hint={'center_x': 0.70, 'center_y': 0.7})
        root.add_widget(self.player1_score_label)

        self.player2_score_label = Label(text=str(scoreboard.player2_score), bold=True, font_size='40sp', color=(1, 1, 1, 1), size_hint=(None, None),
                                         size=(200, 50), pos_hint={'center_x': 0.70, 'center_y': 0.4})
        root.add_widget(self.player2_score_label)

        exit_button = Button(text='Exit', size_hint=(None, None), size=(150, 50),
                             pos_hint={'center_x': 0.35, 'y': 0.2},
                             background_color=(0.6, 0.4, 0.2, 1), border=(16, 16, 16, 16))
        exit_button.bind(on_press=self.exit_game)
        root.add_widget(exit_button)

        play_again_button = Button(text='Play Again', size_hint=(None, None), size=(150, 50),
                                   pos_hint={'center_x': 0.65, 'y': 0.2},
                                   background_color=(0.6, 0.4, 0.2, 1), border=(16, 16, 16, 16))
        play_again_button.bind(on_press=self.play_again)
        root.add_widget(play_again_button)

        self.scoreboard = scoreboard
        return root

    def update_background(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def exit_game(self, instance):
        App.get_running_app().stop()

    def play_again(self, instance):
        self.scoreboard.player1_score = 0
        self.scoreboard.player2_score = 0
        self.scoreboard.result = "WINS"
        self.update_scoreboard()

    def update_scoreboard(self):
        self.player1_score_label.text = str(self.scoreboard.player1_score)
        self.player2_score_label.text = str(self.scoreboard.player2_score)
        self.wins_label.text = self.scoreboard.result
        self.lose_label.text = "LOSE" if self.scoreboard.result == "WINS" else "WINS"

if __name__ == '__main__':
    ScoreboardApp().run()
