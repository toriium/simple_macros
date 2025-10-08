import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.utils.table_builder import TableBuilder


class IngredientsPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.columns = []

        columns = [ft.DataColumn(ft.Text(col)) for col in TblIngredients().columns()]
        columns.append(ft.DataColumn(ft.Text("Actions")))

        self.data_table = ft.DataTable(columns=columns, rows=[])
        self.update_table()
        
        text = ft.Text("Ingredients Page", size=30)
        self.controls = [text, self.data_table]

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

    def delete_ingredient(self, ingredient: TblIngredients):
        # IngredientsRepository().delete_ingredient(ingredient.id)
        IngredientsRepository().delete_ingredient(ingredient[0])
        self.update_table()
        self.update()
