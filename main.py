import flet as ft


class Ingredient(ft.Column):
    def __init__(
        self,
        name: str,
        fat: float = 0,
        carbs: float = 0,
        protein: float = 0,
        kcal: int = 0,
        on_delete=None,
    ):
        super().__init__()
        self.name = name
        self.fat = float(fat)
        self.carbs = float(carbs)
        self.protein = float(protein)
        self.kcal = int(kcal)

        self.on_delete = on_delete

        self.txt_name = ft.TextField(
            label="Name",
            value=self.name,
            on_change=self.update_values,
            text_align=ft.TextAlign.LEFT,
        )
        self.txt_fat = ft.TextField(
            label="Fat",
            value=str(self.fat),
            on_change=self.update_values,
            text_align=ft.TextAlign.LEFT,
        )
        self.txt_carbs = ft.TextField(
            label="Carbs",
            value=str(self.carbs),
            on_change=self.update_values,
            text_align=ft.TextAlign.LEFT,
        )
        self.txt_protein = ft.TextField(
            label="Protein",
            value=str(self.protein),
            on_change=self.update_values,
            text_align=ft.TextAlign.LEFT,
        )
        self.txt_kcal = ft.TextField(
            label="Kcal",
            value=str(self.kcal),
            on_change=self.update_values,
            text_align=ft.TextAlign.LEFT,
        )
        
        delete_btn = ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete_clicked)
        self.row = ft.Row(
            controls=[
                self.txt_name,
                self.txt_fat,
                self.txt_carbs,
                self.txt_protein,
                self.txt_kcal,
            ]
        )

        if self.on_delete is not None:
            self.row.controls.append(delete_btn)

        self.controls = [self.row]

    def delete_clicked(self, e):
        if self.on_delete:
            self.on_delete(self)

    def update_values(self, e):
        self.name = self.txt_name.value
        self.fat = float(self.txt_fat.value)
        self.carbs = float(self.txt_carbs.value)
        self.protein = float(self.txt_protein.value)
        self.kcal = int(self.txt_kcal.value)


class IngredientList(ft.Column):
    def __init__(self):
        super().__init__()
        self.ingredients: list[Ingredient] = []

    def add(self, ingredient: Ingredient):
        # Adiciona o callback de deleção ao ingrediente
        ingredient.on_delete = self.remove
        self.ingredients.append(ingredient)
        self.controls.append(ingredient)
        self.update()

    def remove(self, ingredient: "Ingredient"):
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
        if ingredient in self.controls:
            self.controls.remove(ingredient)
        self.update()


class SimpleMacrosApp(ft.Column):
    # application's root control is a Column containing all other controls
    def __init__(self):
        super().__init__()

        self.ingredients = IngredientList()

        self.form_ingredient = Ingredient(
            name="Put a name", fat=0, carbs=0, protein=0, kcal=0
        )

        row_macros = ft.Row(controls=[self.form_ingredient])

        btn_add = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)
        btn_calculate = ft.FloatingActionButton(
            icon=ft.Icons.CALCULATE, on_click=self.calculate_click
        )

        self.txt_sum_of_macros = ft.TextField(
            label="Total", value="0", text_align=ft.TextAlign.JUSTIFY
        )

        self.controls = [
            ft.Row(controls=[row_macros, btn_add]),
            ft.Row(controls=[btn_calculate]),
            ft.Column(
                spacing=25,
                controls=[
                    self.ingredients,
                ],
            ),
            self.txt_sum_of_macros,
        ]

    def add_clicked(self, e):
        ingredient = Ingredient(
            name=self.form_ingredient.name,
            fat=self.form_ingredient.fat,
            carbs=self.form_ingredient.carbs,
            protein=self.form_ingredient.protein,
            kcal=self.form_ingredient.kcal,
            on_delete=self.ingredients.remove,
        )
        self.ingredients.add(ingredient)
        self.update()

    def calculate_click(self, e):
        value = 0
        for ingredient in self.ingredients.controls:
            protein = float(ingredient.txt_protein.value)
            carbs = float(ingredient.txt_carbs.value)
            fat = float(ingredient.txt_fat.value)
            kcal = int(ingredient.txt_kcal.value)
            value += protein + carbs + fat + kcal
        self.txt_sum_of_macros.value = str(value)
        self.update()


def main(page: ft.Page):
    page.title = "Simple Macros"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.update()

    app = SimpleMacrosApp()

    page.add(app)


ft.app(target=main)
