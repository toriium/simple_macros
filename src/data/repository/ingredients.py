from src.data.db_orm.query_obj import select_all_obj
from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.db_orm.query_obj import delete_obj, insert_obj



class IngredientsRepository:
    def get_all_ingredients(self) -> list[TblIngredients]:
        return select_all_obj(obj_table=TblIngredients)

    def add_ingredient(self, ingredient: TblIngredients) -> None:
        _, err = insert_obj(obj=ingredient)
        if err:
            print(f"Error adding ingredient: {err}")

    def delete_ingredient(self, ingredient_id: int) -> None:
        err = delete_obj(obj_table=TblIngredients, where_clauses=[TblIngredients.id == ingredient_id])
        if err:
            print(f"Error deleting ingredient with id {ingredient_id}: {err}")




if __name__ == "__main__":
    ingredients = IngredientsRepository().get_all_ingredients()

    for ingredient in ingredients:
        print(ingredient)
