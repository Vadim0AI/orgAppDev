from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        btn = Button(text='Перейти к следующему экрану')
        btn.bind(on_release=self.switch_to_next)
        self.add_widget(btn)

    def switch_to_next(self, *args):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        btn = Button(text='Перейти к предыдущему экрану')
        btn.bind(on_release=self.switch_to_previous)
        self.add_widget(btn)

    def switch_to_previous(self, *args):
        self.manager.current = 'main'

class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

if __name__ == '__main__':
    MyApp().run()
