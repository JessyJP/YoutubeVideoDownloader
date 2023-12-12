# Import Kivy App and Label modules
from kivy.app import App
from kivy.uix.label import Label

# Define the app
class MyFirstKivyApp(App):
    def build(self):
        return Label(text='Hello, Kivy!')

# Run the app
if __name__ == '__main__':
    MyFirstKivyApp().run()
