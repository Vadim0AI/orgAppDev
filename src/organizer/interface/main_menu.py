from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from hex_to_rgba import hex_to_rgba


class MenuApp(App):
    def build(self):

        # Устанавливаем цвет фона окна
        Window.clearcolor = hex_to_rgba('#252824')
        Window.size = (250, 250)  # Устанавливаем размер окна

        # Создаем вертикальный контейнер для размещения кнопок
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Создаем пустой виджет для пространства сверху
        layout.add_widget(Widget())

        # TODO: Написать отдельную функцию, которая получает цвет RGBA,
        #  делением на 255

        # Создаем пять кнопок и добавляем их в контейнер
        button_1 = Button(text='Day', size_hint=(None, None),
                        size=(200, 50), pos_hint={'center_x': 0.5},
                        background_color=hex_to_rgba('#238146'),
                        background_normal='')
        layout.add_widget(button_1)

        button_2 = Button(text='Week', size_hint=(None, None),
                          size=(200, 50), pos_hint={'center_x': 0.5},
                          background_color=hex_to_rgba('#238146'),
                          background_normal='')
        layout.add_widget(button_2)

        button_3 = Button(text='Global Week', size_hint=(None, None),
                          size=(200, 50), pos_hint={'center_x': 0.5},
                          background_color=hex_to_rgba('#238146'),
                          background_normal='')
        layout.add_widget(button_3)

        button_4 = Button(text='Global Month', size_hint=(None, None),
                          size=(200, 50), pos_hint={'center_x': 0.5},
                          background_color=hex_to_rgba('#238146'),
                          background_normal='')
        layout.add_widget(button_4)

        # Создаем пустой виджет для пространства снизу
        layout.add_widget(Widget())

        return layout



if __name__ == '__main__':
    MenuApp().run()
