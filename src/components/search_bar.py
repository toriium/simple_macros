import flet as ft
from abc import abstractmethod, ABC

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
    def items_to_show(self, typed_text:str) -> list[str]:
        ...

    def handle_change(self, e: ft.ControlEvent):
        items_to_show = self.items_to_show(e.data.lower())
      
        self.lv.controls.clear()
        for title, data in items_to_show:
            list_tile = ft.ListTile(
                title=ft.Text(f"{title}"), on_click=self.close_anchor, data=data
            )
            self.lv.controls.append(list_tile)
        self.update()

    def open_anchor(self, e: ft.ControlEvent):
        self.open_view()

    def close_anchor(self, e: ft.ControlEvent):
        self.selected_data = e.control.data
        self.close_view(e.control.title.value)