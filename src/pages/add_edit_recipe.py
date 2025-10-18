from typing import Literal
import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.state_manager import StateManager

class AddEditIngredientsPage(ft.Column): 
    def __init__(self, mode: Literal["add", "edit"]="add", ingredient_id:int=None):
        super().__init__()
        self.mode = mode
        self.ingredient_id = ingredient_id

        add_row = AddIngredientsRow(mode=mode, ingredient_id=ingredient_id)
        self.controls = [add_row]


class AddIngredientsRow(ft.Row):
    def __init__(self, mode: Literal["add", "edit"] = "add", ingredient_id:int=None):
        super().__init__()
        # self.expand = True

        self.mode = mode
        self.ingredient_id = ingredient_id
        self.ingredient_obj = None

        self.name = ft.TextField(label="Name", value="", text_align=ft.TextAlign.LEFT,width=100, dense=True)
        self.quantity = ft.TextField(label="Quantity", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.fat = ft.TextField(label="Fat", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.carbs = ft.TextField(label="Carbs", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.fiber = ft.TextField(label="Fiber", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.protein = ft.TextField(label="Protein", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.kcal = ft.TextField(label="Kcal", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)

        text_btn = "Add Ingredient" if mode == "add" else "Update Ingredient"

        if self.mode == "edit":
            ingredient = IngredientsRepository.get_ingredient(ingredient_id=ingredient_id)
            self.ingredient_obj = ingredient
            self.name.value = ingredient.name
            self.quantity.value = ingredient.quantity
            self.fat.value = ingredient.fat
            self.carbs.value = ingredient.carbohydrates
            self.fiber.value = ingredient.fiber
            self.protein.value = ingredient.protein
            self.kcal.value = ingredient.kcal

        self.controls = [
            self.name,
            self.quantity,
            self.fat,
            self.carbs,
            self.fiber,
            self.protein,
            self.kcal,
            ft.ElevatedButton(text_btn, on_click=self.add_ingredient)
        ]
    
    def add_ingredient(self, e):
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


        # Clear fields after adding
        self.name.value = ""
        self.quantity.value = "0"
        self.fat.value = "0"
        self.carbs.value = "0"
        self.fiber.value = "0"
        self.protein.value = "0"
        self.kcal.value = "0"
        self.update()

        # Return to IngredientsPage
        # ingredients_page = IngredientsPage()
        StateManager.change_page(StateManager.pages().INGREDIENTS)
        # self.change_page_callback(ingredients_page)