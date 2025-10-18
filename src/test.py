import flet as ft
from abc import abstractmethod, ABC
from dataclasses import dataclass

from src.components.search_bar import CustomSearchBar

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
    def items_to_show(self, typed_text: str) -> list[str, Fruit]:
        list_to_show = []
        for i, fruit in enumerate(fruits_list):
            f = Fruit(id=i, name=fruit)
            list_to_show.append((f"[{i}] {fruit}", f))
        return list_to_show


class RecipesTable(ft.Column):
    def __init__(self):
        super().__init__()

        self.search_bar = FruitsSearchBar()
        self.btn = ft.ElevatedButton("Close", on_click=self.bar_change)

        self.display_text = ft.Text("")
        self.controls = [self.search_bar, self.btn, self.display_text]

    def bar_change(self, e):
        selected_data = self.search_bar.selected_data
        self.display_text.value = f"Selected: {selected_data.name}"
        self.update()

def main(page):
    t = RecipesTable()
    page.add(t)


ft.app(main)
