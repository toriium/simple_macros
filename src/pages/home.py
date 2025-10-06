import flet as ft


class HelloPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.controls = [
            ft.Text("👋 Hello! Welcome to the first tab!", size=24)
        ]

    # def did_mount(self):
    #     # Called after the control is added to the page
    #     print("BaseLayout mounted")