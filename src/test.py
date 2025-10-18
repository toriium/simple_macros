import flet as ft
from abc import abstractmethod, ABC
from dataclasses import dataclass

from src.components.search_bar import CustomSearchBar, SearchBarData

fruits_list = [
    "apple",
    "banana",
    "orange",
    "grape",
    "strawberry",
    "watermelon",
    "kiwi",
    "pineapple",
    "mango",
    "pear",
]


@dataclass
class Fruit:
    id: int
    name: str


class FruitsSearchBar(CustomSearchBar):
    def search_bar_items(self, typed_text: str) -> list[SearchBarData]:
        bar_items: SearchBarData = []

        for i, fruit in enumerate(fruits_list):
            data = Fruit(id=i, name=fruit)
            bar_data = SearchBarData(
                title=fruit,
                subtitle="subtitle: " + fruit,
                data=data,
                img_path=None,
            )
            bar_items.append(bar_data)
        return bar_items


class RecipesTable(ft.Column):
    def __init__(self):
        super().__init__()

        self.search_bar = FruitsSearchBar()
        self.btn = ft.ElevatedButton("Close", on_click=self.bar_change)

        self.display_text = ft.Text("")
        self.controls = [self.search_bar, self.btn, self.display_text]

    def bar_change(self, e):
        selected_data = self.search_bar.selected_data
        self.display_text.value = f"Selected: {selected_data.title}"
        self.update()

def main(page):
    t = RecipesTable()
    page.add(t)


ft.app(main)
