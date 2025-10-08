import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.utils.table_builder import TableBuilder


class IngredientsPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        ingredients = IngredientsRepository().get_all_ingredients()
        table = TableBuilder(table=TblIngredients, data_list=ingredients)

        columns = [ft.DataColumn(ft.Text(col)) for col in table.columns]

        self.data_table = ft.DataTable(
            columns=columns,
            rows=[])
        
        for ingredient in table.data_table:
            self.data_table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(item))) for item in ingredient])
            )

        text = ft.Text("Ingredients Page", size=30)
        self.controls = [text, self.data_table]


    # def did_mount(self):
    #     # Called after the control is added to the page
    #     print("BaseLayout mounted")
