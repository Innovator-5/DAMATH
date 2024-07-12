from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock

# Loading Screen
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        layout = RelativeLayout()
        splash_label = Label(text='loading...', font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(splash_label)
        self.add_widget(layout)

# 1st Window\Start Window
class StartWindow(Screen):
    def __init__(self, **kwargs):
        super(StartWindow, self).__init__(**kwargs)
        layout = RelativeLayout()

        # Window Background Color
        Window.clearcolor = (166/255, 166/255, 166/255, 1)
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

        # Logo image
        logo_image = AsyncImage(source='LOGO.png', pos_hint={'center_x': 0.5, 'center_y': 0.6}, size_hint=(1000, 1000))
        layout.add_widget(logo_image)

        # Start Button
        start_button = Button(text='Start', size_hint=(0.1, 0.090), font_name='Roboto-Bold', font_size=30,
                              pos_hint={'center_x': 0.5, 'center_y': 0.2},
                              background_color=(0xD6/255, 0xAF/255, 0x72/255, 1))
        layout.add_widget(start_button)

        start_button.bind(on_press=self.start_game)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'main_app'
        print('Game started!')

# 2nd Window\Home Window
class HomeWindow(Screen):
    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        # DAMATH title
        title_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        title_label = Label(text='DAMATH', font_name='Roboto-Bold', color=(12/255, 11/255, 4/255, 1), font_size=80,
                            padding=[0, 50, 0, 0])
        title_layout.add_widget(title_label)
        main_layout.add_widget(title_layout)

        # Board Image
        board_image = Image(source='BOARD.png', size_hint=(1, 2), allow_stretch=True)
        main_layout.add_widget(board_image)

        # Play Button
        left_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        play_button = Button(text='PLAY', size_hint=(None, None), font_name='Roboto-Bold', width=200, height=60,
                             font_size=30, background_color=(0xD6/255, 0xAF/255, 0x72/255, 1))
        play_button.bind(on_release=self.on_play_button)
        left_button_layout.add_widget(play_button)

        # About Button
        right_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        about_button = Button(text='ABOUT', size_hint=(None, None), font_name='Roboto-Bold', width=200, height=60,
                              font_size=30, background_color=(0xD6/255, 0xAF/255, 0x72/255, 1))
        about_button.bind(on_release=self.on_about_button)
        right_button_layout.add_widget(about_button)

        # Play and About Buttons
        button_container = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), padding=[0, 0, 0, 85])
        button_container.add_widget(left_button_layout)
        button_container.add_widget(right_button_layout)
        main_layout.add_widget(button_container)

        self.add_widget(main_layout)

    def on_play_button(self, instance):
        print('Play button pressed')

    def on_about_button(self, instance):
        print('About button pressed')
        self.manager.current = 'about_window'

# 3rd Window\About Window
class AboutWindow(Screen):
    def __init__(self, **kwargs):
        super(AboutWindow, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        # Title
        title = Label(text='USER MANUAL', font_size=40, size_hint=(1, 0.2))
        layout.add_widget(title)

        # Game explanation
        explanation = Label(text='Rules of Damath:\n'
                                 "1. The objective is to have the highest score when the game ends.\n"
                                 "2. Points are scored for each capture made during play and for each piece still on "
                                 "the board at the end of the game.\n"
                                 "3. When capturing an opponent's piece, the capturing piece ('Taker') must move over"
                                 " the opponent's piece ('Taken') and utilize any of the two operations that exist at"
                                 " the end of the taken piece.\n"
                                 "4. If a piece is a 'Dama', then the total score is increased. "
                                 "Correspondingly, if both the taker and the taken piece are 'Dama', "
                                 "the overall score is quadrupled.\n"
                                 "5. It is necessary to take the move with the most number of captured "
                                 "pieces in the capture.\n"
                                 "6. The remaining pieces of the players are added to their respective "
                                 "scores. If the remaining piece is a 'Dama', then its score is also doubled.\n"
                                 "7. The game concludes if a player does not have any pieces left "
                                 "(or is unable to make a legal move).\n",
                                 font_size=19, color=(0, 0, 0, 1), size_hint=(None, None), size=(680, 600),
                                 text_size=(660, None), pos_hint={'center_x': 0.5, 'center_y': 0.2})

        explanation.bind(size=explanation.setter('text_size'))
        layout.add_widget(explanation)
        # Adjust text size to fit

        # Buttons Layout
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1.8), spacing=850)

        # Back Button
        back_button = Button(text='Back', size_hint=(0.5, 1), font_size=30,
                             background_color=(0xD6 / 255, 0xAF / 255, 0x72 / 255, 1))
        back_button.bind(on_release=self.on_back_button)
        buttons_layout.add_widget(back_button)

        # Picture Manual Button
        picture_button = Button(text='Picture Manual', size_hint=(0.5, 1), font_size=30,
                                background_color=(0xD6 / 255, 0xAF / 255, 0x72 / 255, 1))
        picture_button.bind(on_release=self.on_picture_button)
        buttons_layout.add_widget(picture_button)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def on_back_button(self, instance):
        self.manager.current = 'main_app'

    def on_picture_button(self, instance):
        self.manager.current = 'picture_window'

# 4th Window\Picture Window
class Picture(Screen):
    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        image = Image(source='manual.png', size_hint=(None, None), size=(1000, 580),
                          pos_hint={'center_x': 0.5, 'top': 0.8})
        layout.add_widget(image)

        button_layout = BoxLayout(size_hint=(None, None), height=50, width=300,
                                  pos_hint={'center_x': 0.5, 'top': 0.7},
                                  spacing=40)
        back_btn = Button(text='Back', size_hint=(None, None), size=(140, 50), color=(1, 1, 1, 1),
                          background_color=(0.4, 0.2, 0.0, 1.0))  # White text color, brown background
        back_btn.bind(on_press=self.on_back_button)
        button_layout.add_widget(back_btn)

        exit_btn = Button(text='Exit', size_hint=(None, None), size=(140, 50), color=(1, 1, 1, 1),
                          background_color=(0.4, 0.2, 0.0, 1.0))  # White text color, brown background
        exit_btn.bind(on_press=self.exit_app)
        button_layout.add_widget(exit_btn)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_back_button(self, instance):
        self.manager.current = 'about_window'

    def exit_app(self, instance):
        App.get_running_app().stop()
        Window.close()


class Damath(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(StartWindow(name='start_window'))
        sm.add_widget(HomeWindow(name='main_app'))
        sm.add_widget(AboutWindow(name='about_window'))
        sm.add_widget(Picture(name='picture_window'))

        sm.current = 'splash'

        Clock.schedule_once(self.go_to_start_window, 5)

        return sm

    def go_to_start_window(self, dt):
        self.root.current = 'start_window'


if __name__ == '__main__':
    Damath().run()
