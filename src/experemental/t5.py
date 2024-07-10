from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class SimpleApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Hello, Kivy!')
        self.layout.add_widget(self.label)

        self.button = Button(text='Click me!')
        self.button.bind(on_press=self.on_button_press)
        self.layout.add_widget(self.button)

        return self.layout

    def on_button_press(self, instance):
        self.label.text = 'Button clicked!'


if __name__ == '__main__':
    SimpleApp().run()
