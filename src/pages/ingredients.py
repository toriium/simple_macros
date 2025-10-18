import flet as ft

from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.repository.ingredients import IngredientsRepository
from src.utils.table_builder import TableBuilder
from src.state_manager import StateManager


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
        
        for ingredient, fields in table.data_table:
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
            row_cells = [ft.DataCell(ft.Text(str(item))) for item in fields]
            row_cells.append(ft.DataCell(delete_btn))
            row_cells.append(ft.DataCell(edit_btn))
            self.data_table.rows.append(ft.DataRow(cells=row_cells))
        
        self.update()


    def delete_ingredient(self, ingredient: TblIngredients):
        IngredientsRepository.delete_ingredient(ingredient_id=ingredient.id)
        self.update_table()

    def edit_ingredient(self, ingredient: TblIngredients):
        page = StateManager.pages().ADD_EDIT
        StateManager.change_page(page, mode="edit", ingredient_id=ingredient.id)

class AddIngredientsRow(ft.Row):
    def __init__(self):
        super().__init__()
        self.expand = True
        
        add_btn = ft.ElevatedButton("Add Ingredient", on_click=self.go_to_add_edit)

        self.controls = [add_btn]
    
    def go_to_add_edit(self, e):
        # add_edit_page = AddEditIngredientsPage(change_page_callback=self.change_page_callback)
        StateManager.change_page(StateManager.pages().ADD_EDIT)
        # self.change_page_callback(page=add_edit_page)

class IngredientsPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        
        self.ingredients_table = IngredientsTable()
        self.add_ingredients_row = AddIngredientsRow()

        self.controls = [self.add_ingredients_row, self.ingredients_table]
