from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.db_orm.tables.base import Base


class TblIngredients(Base):
    __tablename__ = 'tbl_ingredients'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    quantity: Mapped[float] = mapped_column(default=0.0, nullable=False)
    fat: Mapped[float] = mapped_column(default=0.0, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(default=0.0, nullable=False)
    protein: Mapped[float] = mapped_column(default=0.0, nullable=False)
    fiber: Mapped[float] = mapped_column(default=0.0, nullable=False)
    kcal: Mapped[float] = mapped_column(default=0.0, nullable=False)
    # unit: Mapped[str] = mapped_column(String(50), nullable=False)

    # relação reversa
    recipes: Mapped[list["TblRecipeIngredients"]] = relationship(back_populates="ingredient")
    def __repr__(self):
        return str(self.model_to_dict())

    def __str__(self):
        return str(self.columns())
