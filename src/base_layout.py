import flet as ft

from pages.add_edit_ingredient import AddEditIngredientsPage
from src.pages.ingredients import IngredientsPage
from src.pages.home import HelloPage
from src.pages.input_text import InputPage
from src.state_manager import StateManager


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
                ft.NavigationRailDestination(icon=ft.Icons.LIST_ALT, label="Ingredients"),
                ft.NavigationRailDestination(icon=ft.Icons.EDIT, label="Add/Edit"),
            ],
            on_change=self.on_nav_change,
        )

        self.content = ft.Container(content=self.get_page_default(0), expand=True, padding=20)

        layout = ft.Row(
            [
                self.sidebar,
                ft.VerticalDivider(),
                self.content,
            ],
            expand=True,
        )

        StateManager.base_layout = self
        self.controls = [layout]

    def change_page(self, page: any):
        self.sidebar.selected_index = 0 # Update it in the future
        self.content.content = page
        self.update()

    def on_nav_change(self, e):
        index = e.control.selected_index
        self.content.content = self.get_page_default(index)
        self.update()

    def get_page_default(self, index: int):
        if index == 0:
            return HelloPage()
        elif index == 1:
            return InputPage()
        elif index == 2:
            return IngredientsPage(change_page_callback=self.change_page)
        elif index == 3:
            return AddEditIngredientsPage(change_page_callback=self.change_page)  
        else:
            return ft.Text("Page not found")

    def did_mount(self):
    # Called after the control is added to the page
        print("BaseLayout mounted")
