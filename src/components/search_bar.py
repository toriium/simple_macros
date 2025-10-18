import flet as ft
from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class SearchBarData:
    title: str
    subtitle: str
    data: any
    img_path: str | None = None


class CustomSearchBar(ft.SearchBar, ABC):
    def __init__(self):
        super().__init__()
        self.view_elevation = 4
        self.divider_color = ft.Colors.BLUE
        self.bar_hint_text = "Search..."
        self.view_hint_text = "Start typing to view options..."
        self.on_change = self.handle_change
        self.on_tap = self.open_anchor

        self.selected_data = None

        self.lv = ft.ListView()
        self.controls = [self.lv]

    @abstractmethod
    def search_bar_items(self, typed_text: str) -> list[SearchBarData]: ...

    @abstractmethod
    def click_callback(self): ...

    def handle_change(self, e: ft.ControlEvent):
        search_bar_items = self.search_bar_items(e.data.lower())

        self.lv.controls.clear()
        for data in search_bar_items:
            leading = ft.Image(src=data.img_path, fit="contain") if data.img_path else ft.Icon(ft.Icons.SETTINGS)

            list_tile = ft.ListTile(
                on_click=self.close_anchor,
                data=data,
                leading=leading,
                title=ft.Text(data.title),
                subtitle=ft.Text(data.subtitle),
            )
            self.lv.controls.append(list_tile)
        self.update()

    def open_anchor(self, e: ft.ControlEvent):
        self.open_view()

    def close_anchor(self, e: ft.ControlEvent):
        self.selected_data = e.control.data
        self.click_callback()
        self.close_view(e.control.title.value)
