from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.db_orm.tables.base import Base


class TblRecipeIngredients(Base):
    __tablename__ = 'tbl_recipe_ingredients'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('tbl_recipes.id', ondelete="CASCADE"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('tbl_ingredients.id', ondelete="CASCADE"))
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)

    # relações
    recipe: Mapped["TblRecipes"] = relationship(back_populates="ingredients")
    ingredient: Mapped["TblIngredients"] = relationship(back_populates="recipes")

    def __repr__(self):
        return str(self.model_to_dict())

    def __str__(self):
        return str(self.columns())
