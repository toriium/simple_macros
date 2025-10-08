from src.data.db_orm.query_obj import select_all_obj
from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from utils.table_builder import TableBuilder


class IngredientsRepository:
    def get_all_ingredients(self) -> list[TblIngredients]:
        return select_all_obj(obj_table=TblIngredients)





if __name__ == "__main__":
    ingredients = IngredientsRepository().get_all_ingredients()

    for ingredient in ingredients:
        print(ingredient)
