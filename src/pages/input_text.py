import flet as ft


class InputPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.text_field = ft.TextField(label="Type something")
        self.output_text = ft.Text("")

        self.controls = [
            ft.Text("📝 Type something below:", size=20),
            self.text_field,
            ft.ElevatedButton("Show", on_click=self.show_text),
            self.output_text,
        ]

    def show_text(self, e):
        self.output_text.value = f"You typed: {self.text_field.value}"
        self.update()