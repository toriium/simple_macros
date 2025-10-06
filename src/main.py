import flet as ft

from src.base_layout import BaseLayout


def main(page: ft.Page):
    page.title = "Simple Macros"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.DARK
    page.expand = True

    app_layout = BaseLayout()
    page.add(app_layout)


ft.app(target=main)
