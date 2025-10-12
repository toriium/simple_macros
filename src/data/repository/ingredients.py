from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.db_orm.query_obj import delete_obj, insert_obj, select_all_obj, select_first_obj, update_obj



class IngredientsRepository:
    @classmethod
    def get_all_ingredients(cls) -> list[TblIngredients]:
        return select_all_obj(obj_table=TblIngredients)
    
    @classmethod
    def get_ingredient(cls, ingredient_id: int) -> TblIngredients:
        return select_first_obj(obj_table=TblIngredients, where_clauses=[TblIngredients.id == ingredient_id])

    @classmethod
    def add_ingredient(cls, ingredient: TblIngredients) -> None:
        _, err = insert_obj(obj=ingredient)
        if err:
            print(f"Error adding ingredient: {err}")

    @classmethod
    def update_ingredient(cls, values: dict, ingredient_id: int) -> None:
        updated, err = update_obj(obj_table=TblIngredients, update_values=values, where_clauses=[TblIngredients.id == ingredient_id])
        if err:
            print(f"Error updating ingredient: {err}")

    @classmethod
    def delete_ingredient(cls, ingredient_id: int) -> None:
        err = delete_obj(obj_table=TblIngredients, where_clauses=[TblIngredients.id == ingredient_id])
        if err:
            print(f"Error deleting ingredient with id {ingredient_id}: {err}")




if __name__ == "__main__":
    ingredients = IngredientsRepository.get_all_ingredients()

    for ingredient in ingredients:
        print(ingredient)
