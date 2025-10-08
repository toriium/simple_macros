from contextlib import contextmanager
from copy import copy
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.data.db_orm.connection import ReadingSession, WritingSession
from src.data.errors.sql_error import SQLError


def dict_diff(old_data: dict, new_data: dict, keep_old_if_none: bool = False) -> dict:
    """
    keep_old_if_none: If the new data field is None will not show the difference, will keep the old value
    """

    # Create a dictionary to hold only the fields that differ
    differences = {}

    # Compare the old and new data
    for key in new_data:
        new_data_value = new_data[key]
        if new_data_value is None and keep_old_if_none is True:
            continue

        if key not in old_data or old_data[key] != new_data_value:
            differences[key] = new_data[key]

    if differences == {}:
        return None
    return differences


def create_obj_from_diff(old_obj, new_obj, keep_old_if_none: bool = False):
    diff_obj = old_obj

    old_dict = old_obj.model_to_dict()
    new_dict = new_obj.model_to_dict()

    diff_data = dict_diff(old_data=old_dict, new_data=new_dict, keep_old_if_none=keep_old_if_none)
    if diff_data is None:
        return diff_obj

    for k, v in diff_data.items():
        setattr(diff_obj, k, v)

    return diff_obj


@contextmanager
def create_reading_session() -> Session:
    """Way - 1
    with create_session() as session:
        var = session.query(User).filter_by(id=2).first()
        print(var.name)
    ----------------------------------------------------
    Way - 2
    with create_session() as session:
        results = session.query(User).all()
        for row in results:
            print(row.name).
    """
    session = ReadingSession()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def create_writing_session() -> Session:
    """Way - 1
        with create_writing_session() as session:
            session.add(obj)
            session.commit()
    """
    session = WritingSession()
    try:
        yield session
    finally:
        session.close()


def select_first_obj(obj_table, where_clauses: list = None) -> Any | None:
    """Way - 1
    result = select_first_obj(obj_table=User, where_clauses=[User.id==2])
    """
    where_clauses = where_clauses if where_clauses else []

    with create_reading_session() as session:
        stmt = select(obj_table).where(*where_clauses)
        result = session.scalar(statement=stmt)
        result = result

    return result if result else None


def select_all_obj(obj_table, where_clauses: list = None) -> list:
    """Way - 1
    result = select_all_obj(obj_table=User, where_clauses=[User.id == 1, User.id != 2])
    for var in result:
        print(var).
    """
    where_clauses = where_clauses if where_clauses else []

    with create_reading_session() as session:
        stmt = select(obj_table).where(*where_clauses)
        result = session.execute(statement=stmt)
        result = result.all()

    return result if result else []


def insert_obj(obj) -> tuple[Any, SQLError | None]:
    """Way - 1
    obj_user = User(name='nietzsche', age=55)
    result, err = insert_obj(obj=obj_user)
    ----------------------------------------------------
    Way - 2
    obj_user = User()
    obj_user.name = 'platao'
    obj_user.age = 65
    result, err = insert_obj(obj=obj_user)
    print(result.name)
    """
    try:
        with create_writing_session() as session:
            session.add(obj)
            session.flush()
            updated_obj_data = copy(obj)
            session.commit()
    except IntegrityError as error:
        duplicate_entry_errors = [
            'duplicate key value violates unique constraint',  # PostgresSQL
            "1062 (23000): Duplicate entry",  # MySQL
        ]
        is_duplicate_entry = False
        for e in duplicate_entry_errors:
            if e in str(error.orig):
                is_duplicate_entry = True

        unique_constraint_errors = [
            'UNIQUE constraint failed',  # SQLite
        ]
        is_unique_constraint = False
        for e in unique_constraint_errors:
            if e in str(error.orig):
                is_unique_constraint = True

        # Return specific error
        if is_duplicate_entry:
            return None, SQLError.duplicate_entry
        elif is_unique_constraint:
            return None, SQLError.unique_constraint
        else:
            raise error

    return updated_obj_data, None


def insert_all_obj(objs: list):
    """Way - 1
    obj_user1 = User(name='zenao', age=55)
    obj_user2 = User(name='diogenes', age=55)
    insert_all_obj(objs=[obj_user1, obj_user2]).
    """
    with create_writing_session() as session:
        session.add_all(objs)
        session.flush()
        updated_obj_data = copy(objs)
        session.commit()

    return updated_obj_data


def update_obj(obj_table, update_values: dict, where_clauses: list = None) -> tuple[Any, SQLError | None]:
    """
    # Way - 1
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("before:", result)
    #
    # updated, err = update_obj(obj_table=User, update_values=dict(name="54545"), where_clauses=[User.id == 1])
    # print("updated", updated)
    #
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("after:", result)
    """
    where_clauses = where_clauses if where_clauses else []

    with create_writing_session() as session:
        stmt = update(obj_table).where(*where_clauses).values(**update_values)
        result = session.execute(statement=stmt)

        session.flush()
        updated_obj_data = copy(update_values)
        rowcount = result.rowcount
        session.commit()

    if rowcount >= 1:
        return updated_obj_data, None
    else:
        return updated_obj_data, SQLError.not_found


def patch_obj(updated_obj) -> tuple[Any, SQLError | None]:
    """
    For cases when you queried an object, updated a value and want to update in the DB

    # Way - 1
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("before:", result)
    #
    # result.name = "zezim"
    # updated, err = update_obj(updated_obj=result)
    # print("updated", updated)
    #
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("after:", result)
    """

    with create_writing_session() as session:
        session.add(updated_obj)
        session.flush()
        updated_obj_data = copy(updated_obj)

        session.commit()

    return updated_obj_data, None


def delete_obj(obj_table, where_clauses: list = None) -> SQLError | None:
    """Way - 1
    err = delete_obj(obj_table=User, where_clauses=[User.id != 1])
    """
    where_clauses = where_clauses if where_clauses else []

    with create_writing_session() as session:
        stmt = delete(obj_table).where(*where_clauses)
        result = session.execute(statement=stmt)
        session.commit()

    if result.rowcount >= 1:
        return None
    else:
        return SQLError.not_found


if __name__ == '__main__':
    ...

    # ------------------------------------- use of create_session -------------------------------------
    # Form - 1
    # with create_session() as session:
    #     var = session.query(User).filter_by(id=2).first()
    #     print(var.name)

    # Form - 2
    # with create_session() as session:
    #     results = session.query(User).all()
    #     for row in results:
    #         print(row.name)

    # ------------------------------------- use of select_obj -------------------------------------
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 2])
    # print(result)

    # ------------------------------------- use of select_all_obj -------------------------------------
    # result = select_all_obj(obj_table=User, where_clauses=[User.id == 1, User.id != 2])
    # print(result)

    # ------------------------------------- use of update_obj -------------------------------------
    # Way - 1
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("before:", result)
    #
    # result.name = "zezim"
    # updated, err = update_obj(updated_obj=result)
    # print("updated", updated)
    #
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("after:", result)

    # Way - 2
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("before:", result)
    #
    # updated, err = update_obj(obj_table=User, update_values=dict(name="54545"), where_clauses=[User.id == 1])
    # print("updated", updated)
    #
    # result = select_first_obj(obj_table=User, where_clauses=[User.id == 1])
    # print("after:", result)

    # ------------------------------------- use of insert_obj -------------------------------------
    # Way - 1
    # user = User(name="jere")
    # insert_obj(user)
    # ----------------------------------------------------
    # Way - 2
    # obj_user = User()
    # obj_user.name = 'platao'
    # obj_user.age = 65
    # result, err = insert_obj(obj=obj_user)
    # print(result.name)

    # ------------------------------------- use of insert_all_obj -------------------------------------
    # Form - 1
    # obj_user1 = User(name='zenao', age=55)
    # obj_user2 = User(name='diogenes', age=55)
    # insert_all_obj(objs=[obj_user1, obj_user2])

    # ------------------------------------- use of delete_obj -------------------------------------
    # err = delete_obj(obj_table=User, where_clauses=[User.id != 1])
    # print(err)
