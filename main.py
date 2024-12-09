from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
import requests
from io import BytesIO

class PlantApp(App):
    def build(self):
        # Create the main layout
        self.layout = BoxLayout(orientation='vertical')

        # File chooser to select an image
        self.file_chooser = FileChooserIconView()
        self.layout.add_widget(self.file_chooser)

        # Label to display results
        self.result_label = Label(text="Select an image for plant identification.")
        self.layout.add_widget(self.result_label)

        # Button to trigger the upload and process the image
        self.upload_button = Button(text="Upload Image")
        self.upload_button.bind(on_press=self.upload_image)
        self.layout.add_widget(self.upload_button)

        return self.layout

    def upload_image(self, instance):
        selected_file = self.file_chooser.selection
        if selected_file:
            file_path = selected_file[0]
            self.process_image(file_path)

    def process_image(self, file_path):
        url = 'http://127.0.0.1:5000/upload'
        
        # Read the image from file path
        with open(file_path, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            plant_name = data['plant_name']
            disease = data['disease']
            result = f"Plant: {plant_name}\nDisease: {disease}"
            self.result_label.text = result
        else:
            self.result_label.text = "Error in processing the image"

if __name__ == '__main__':
    PlantApp().run()
