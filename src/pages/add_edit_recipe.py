from typing import Literal
import flet as ft

from src.data.db_orm.query_obj import create_writing_session
from src.data.db_orm.tables.tbl_recipe_ingredients import TblRecipeIngredients
from src.data.db_orm.tables.tbl_recipes import TblRecipes
from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.state_manager import StateManager
from src.components.search_bar import CustomSearchBar, SearchBarData
from utils.table_builder import TableBuilder


class AddEditRecipePage(ft.Column): 
    def __init__(self, mode: Literal["add", "edit"]="add", recipe_id:int=None):
        super().__init__()
        self.mode = mode
        self.recipe_id = recipe_id

        self.ingredients_table = IngredientsTable()
        self.search_bar = IngredientsSearchBar(click_callback_func=self.ingredients_table.add_ingredient)

        self.recipe_info = RecipeInfoRow(mode=mode)
        self.add_row = AddUpdateRecipeRow(recipe_info=self.recipe_info, ingredients_table=self.ingredients_table, mode=mode, recipe_id=recipe_id)

        self.controls = [self.search_bar, self.recipe_info, self.add_row, self.ingredients_table]

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
                data=ingredient,
                img_path=None,
            )
            bar_items.append(bar_data)
        return bar_items
    
    def click_callback(self):
        data: TblIngredients = self.selected_data.data
        self.click_callback_func(data)


class IngredientsTable(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.columns = []

        self.used_ingredients: list[TblIngredients] = []

        columns = [ft.DataColumn(ft.Text(col)) for col in TblIngredients().columns()]
        columns.append(ft.DataColumn(ft.Text("DELETE")))

        self.data_table = ft.DataTable(columns=columns, rows=[])
        
        text = ft.Text("Ingredients", size=30)
        self.controls = [text, self.data_table]
    
    def did_mount(self):
        self.update_table()

    def update_table(self):
        table = TableBuilder(table=TblIngredients, data_list=self.used_ingredients)

        self.data_table.rows.clear()
        for ingredient, fields in table.data_table:
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Delete",
                on_click=lambda e, ing=ingredient: self.delete_ingredient(ing)
            )
            
            row_cells = [ft.DataCell(ft.Text(str(item))) for item in fields]
            row_cells.append(ft.DataCell(delete_btn))
            self.data_table.rows.append(ft.DataRow(cells=row_cells))
        
        self.update()
    
    def add_ingredient(self, ingredient: TblIngredients):
        self.used_ingredients.append(ingredient)
        self.update_table()


    def delete_ingredient(self, ingredient: TblIngredients):
        """
        Just remove from the list not DB 
        """
        self.used_ingredients.remove(ingredient)
        self.update_table()




class RecipeInfoRow(ft.Row):
    def __init__(self, mode: Literal["add", "edit"] = "add", recipe: TblRecipes=None):
        super().__init__()
        # self.expand = True

        self.mode = mode
        self.recipe = recipe

        self.name = ft.TextField(label="Name", value="", text_align=ft.TextAlign.LEFT,width=100, dense=True)
        # self.quantity = ft.TextField(label="Quantity", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        
        # self.fat = ft.TextField(label="Fat", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        # self.carbs = ft.TextField(label="Carbs", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        # self.fiber = ft.TextField(label="Fiber", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        # self.protein = ft.TextField(label="Protein", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        # self.kcal = ft.TextField(label="Kcal", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)

        if self.mode == "edit":
            self.name.value = self.recipe.name
            # self.quantity.value = ingredient.quantity
            # self.fat.value = ingredient.fat
            # self.carbs.value = ingredient.carbohydrates
            # self.fiber.value = ingredient.fiber
            # self.protein.value = ingredient.protein
            # self.kcal.value = ingredient.kcal

        self.controls = [
            self.name,
            # self.quantity,
            # self.fat,
            # self.carbs,
            # self.fiber,
            # self.protein,
            # self.kcal,
        ]

class AddUpdateRecipeRow(ft.Row):
    def __init__(self,recipe_info: RecipeInfoRow, ingredients_table: IngredientsTable, mode: Literal["add", "edit"] = "add", recipe_id:int=None):
        super().__init__()

        self.mode = mode
        self.recipe_id = recipe_id
        self.recipe_info = recipe_info
        self.ingredients_table = ingredients_table


        text_btn = "Add Recipe" if mode == "add" else "Update Recipe"

        if self.mode == "edit":
            ...

        self.controls = [
            ft.ElevatedButton(text_btn, on_click=self.add_recipe)
        ]
    
    def add_recipe(self, e):
        recipe = TblRecipes(name=self.recipe_info.name.value)

        recipe_ingredients: list[TblRecipeIngredients] = []
        for ingredient in self.ingredients_table.used_ingredients:
            recipe_ingredient = TblRecipeIngredients(recipe=recipe, ingredient=ingredient, quantity=200, unit="g")
            recipe_ingredients.append(recipe_ingredient)
        
        with create_writing_session() as session:
            session.add(recipe)
            session.add_all(recipe_ingredients)
            session.commit()