import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository

class AddEditIngredientsPage(ft.Column):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback

        add_row = AddIngredientsRow(navigate_callback=self.navigate_callback)
        self.controls = [add_row]


class AddIngredientsRow(ft.Row):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback

        # self.expand = True

        self.name = ft.TextField(label="Name", value="", text_align=ft.TextAlign.LEFT,width=100, dense=True)
        self.quantity = ft.TextField(label="Quantity", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.fat = ft.TextField(label="Fat", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.carbs = ft.TextField(label="Carbs", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.fiber = ft.TextField(label="Fiber", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.protein = ft.TextField(label="Protein", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)
        self.kcal = ft.TextField(label="Kcal", value=0, text_align=ft.TextAlign.LEFT, width=100, dense=True)

        self.controls = [
            self.name,
            self.quantity,
            self.fat,
            self.carbs,
            self.fiber,
            self.protein,
            self.kcal,
            ft.ElevatedButton("Add Ingredient", on_click=self.add_ingredient)
        ]
    
    def add_ingredient(self, e):
        ingredient_obj = TblIngredients(
            name=self.name.value,
            quantity=float(self.quantity.value),
            fat=float(self.fat.value),
            carbohydrates=float(self.carbs.value),
            fiber=float(self.fiber.value),
            protein=float(self.protein.value),
            kcal=float(self.kcal.value)
        )
        IngredientsRepository().add_ingredient(ingredient_obj)


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
        if self.navigate_callback:
            self.navigate_callback(2)