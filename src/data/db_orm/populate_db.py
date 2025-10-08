from src.data.db_orm.query_obj import insert_obj
from src.data.db_orm.tables.tbl_ingredients import TblIngredients
from src.data.errors.sql_error import SQLError


def add_tbl_ingredients() -> list:
    ingredient1 = TblIngredients(
        name="Chicken Breast", 
        quantity=100.0, 
        fat=3.6, 
        carbohydrates=0.0, 
        protein=31.0, 
        fiber=0.0, 
        kcal=165.0)

    commands = [
        ingredient1,
    ]
    return commands


def populate_db():
    objs = []

    objs.extend(add_tbl_ingredients())

    for obj in objs:
        updated, err = insert_obj(obj)
        if err:
            if err in [SQLError.duplicate_entry, SQLError.unique_constraint]:
                continue
            else:
                raise err
