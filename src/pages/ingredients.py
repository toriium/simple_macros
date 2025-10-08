import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.utils.table_builder import TableBuilder


class IngredientsTable(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.columns = []

        columns = [ft.DataColumn(ft.Text(col)) for col in TblIngredients().columns()]
        columns.append(ft.DataColumn(ft.Text("Actions")))

        self.data_table = ft.DataTable(columns=columns, rows=[])
        # self.update_table()
        
        text = ft.Text("Ingredients Page", size=30)
        self.controls = [text, self.data_table]
    
    def did_mount(self):
        self.update_table()

    def update_table(self):
        ingredients = IngredientsRepository().get_all_ingredients()
        table = TableBuilder(table=TblIngredients, data_list=ingredients)

        self.data_table.rows.clear()
        
        for ingredient in table.data_table:
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Delete",
                on_click=lambda e, ing=ingredient: self.delete_ingredient(ing)
            )
            row_cells = [ft.DataCell(ft.Text(str(item))) for item in ingredient]
            row_cells.append(ft.DataCell(delete_btn))
            self.data_table.rows.append(ft.DataRow(cells=row_cells))
        
        self.update()


    def delete_ingredient(self, ingredient: TblIngredients):
        # IngredientsRepository().delete_ingredient(ingredient.id)
        IngredientsRepository().delete_ingredient(ingredient[0])
        self.update_table()



class AddIngredientsRow(ft.Row):
    def __init__(self, update_table_callback: callable):
        super().__init__()
        # self.expand = True

        self.update_table_callback = update_table_callback

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

        # Notify the parent to update the table
        self.update_table_callback()

class IngredientsPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        
        self.ingredients_table = IngredientsTable()
        self.add_ingredients_row = AddIngredientsRow(update_table_callback=self.ingredients_table.update_table)

        add_row_container = ft.Container(
            content=self.add_ingredients_row,
            height=60,  # ajuste conforme necessário
            padding=1
        )

        self.controls = [add_row_container, self.ingredients_table]
