import flet as ft

from data.db_orm.populate_db import populate_db
from data.db_orm.run_migration import run_migration
from src.base_layout import BaseLayout


def db_things():
    run_migration()
    populate_db()

def main(page: ft.Page):
    db_things()

    page.title = "Simple Macros"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.DARK
    page.expand = True

    app_layout = BaseLayout()
    page.add(app_layout)


ft.app(target=main)
