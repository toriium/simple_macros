import flet as ft

from src.pages.home import HelloPage
from src.pages.input_text import InputPage


class BaseLayout(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Hello"),
                ft.NavigationRailDestination(icon=ft.Icons.EDIT, label="Input"),
            ],
            on_change=self.on_nav_change,
        )

        self.content = ft.Container(content=self.get_page(0), expand=True, padding=20)

        layout = ft.Row(
            [
                self.sidebar,
                ft.VerticalDivider(),
                self.content,
            ],
            expand=True,
        )

        self.controls = [layout]

    # Troca o conteúdo dinamicamente
    def on_nav_change(self, e):
        index = e.control.selected_index
        self.content.content = self.get_page(index)
        self.update()

    def get_page(self, index: int):
        if index == 0:
            return HelloPage()
        elif index == 1:
            return InputPage()
        else:
            return ft.Text("Page not found")

    def did_mount(self):
    # Called after the control is added to the page
        print("BaseLayout mounted")
