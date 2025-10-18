from typing import Literal
import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.state_manager import StateManager
from src.components.search_bar import CustomSearchBar, SearchBarData
from utils.table_builder import TableBuilder


class AddEditRecipePage(ft.Column): 
    def __init__(self, mode: Literal["add", "edit"]="add", recipe_id:int=None):
        super().__init__()
        self.mode = mode
        self.ingredient_id = recipe_id

        self.search_bar = IngredientsSearchBar()
        self.controls = [self.search_bar]

        add_row = AddIngredientsRow(mode=mode, ingredient_id=recipe_id)
        self.controls = [add_row]

class IngredientsSearchBar(CustomSearchBar):
    def __init__(self, click_callback_func:callable):
        super().__init__()
        self.click_callback_func = click_callback_func

    def search_bar_items(self, typed_text: str) -> list[SearchBarData]:
        bar_items: SearchBarData = []

        ingredients = IngredientsRepository.get_all_ingredients()

        for ingredient in ingredients:
            bar_data = SearchBarData(
                title=ingredient.name,
                subtitle="subtitle: " + ingredient.name,
                data=ingredient.name,
                img_path=None,
            )
            bar_items.append(bar_data)
        return bar_items
    
    def click_callback(self):
        self.click_callback_func(self.selected_data)


class IngredientsTable(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.columns = []

        columns = [ft.DataColumn(ft.Text(col)) for col in TblIngredients().columns()]
        columns.append(ft.DataColumn(ft.Text("DELETE")))
        columns.append(ft.DataColumn(ft.Text("EDIT")))

        self.data_table = ft.DataTable(columns=columns, rows=[])
        # self.update_table()
        
        text = ft.Text("Ingredients Page", size=30)
        self.controls = [text, self.data_table]
    
    def did_mount(self):
        self.update_table()

    def update_table(self):
        ingredients = IngredientsRepository.get_all_ingredients()
        table = TableBuilder(table=TblIngredients, data_list=ingredients)

        self.data_table.rows.clear()
        
        for ingredient in table.data_table:
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Delete",
                on_click=lambda e, ing=ingredient: self.delete_ingredient(ing)
            )
            edit_btn = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Edit",
                on_click=lambda e, ing=ingredient: self.edit_ingredient(ing)
            )
            row_cells = [ft.DataCell(ft.Text(str(item))) for item in ingredient]
            row_cells.append(ft.DataCell(delete_btn))
            row_cells.append(ft.DataCell(edit_btn))
            self.data_table.rows.append(ft.DataRow(cells=row_cells))
        
        self.update()


    def delete_ingredient(self, ingredient: TblIngredients):
        # IngredientsRepository.delete_ingredient(ingredient.id)
        IngredientsRepository.delete_ingredient(ingredient[0])
        self.update_table()


    def edit_ingredient(self, ingredient: TblIngredients):
        page = StateManager.pages().ADD_EDIT
        StateManager.change_page(page, mode="edit", ingredient_id=ingredient[0])
    
class AddIngredientsRow(ft.Row):
    def __init__(self, mode: Literal["add", "edit"] = "add", recipe_id:int=None):
        super().__init__()

        self.mode = mode
        self.recipe_id = recipe_id
        self.recipe_obj = None


        text_btn = "Add Recipe" if mode == "add" else "Update Recipe"

        if self.mode == "edit":
            ...

        self.controls = [
            ft.ElevatedButton(text_btn, on_click=self.add_recipe)
        ]
    
    def add_recipe(self, e):
        values = {
            "name": self.name.value,
            "quantity": float(self.quantity.value),
            "fat": float(self.fat.value),
            "carbohydrates": float(self.carbs.value),
            "fiber": float(self.fiber.value),
            "protein": float(self.protein.value),
            "kcal": float(self.kcal.value)
        }

        if self.mode == "add":
            ingredient_obj = TblIngredients(**values)
            IngredientsRepository.add_ingredient(ingredient_obj)
        elif self.mode == "edit":
        #     ingredient_obj = TblIngredients(
        #         id=self.ingredient_id,
        #         **values
        #     )
            IngredientsRepository.update_ingredient(values=values, ingredient_id=self.ingredient_id)

        self.update()

        # Return to IngredientsPage
        # ingredients_page = IngredientsPage()
        StateManager.change_page(StateManager.pages().INGREDIENTS)
        # self.change_page_callback(ingredients_page)