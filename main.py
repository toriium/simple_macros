import flet as ft


class Ingredient(ft.Column):
    def __init__(self, name:str, fat:float = 0, carbs:float = 0, protein:float = 0, kcal:int = 0):
        super().__init__()
        self.name = name
        self.fat = float(fat)
        self.carbs = float(carbs)
        self.protein = float(protein)
        self.kcal = int(kcal)

        self.txt_name = ft.TextField(label="Name", value=self.name, on_change=self.update_values, text_align=ft.TextAlign.LEFT)
        self.txt_fat = ft.TextField(label="Fat", value=str(self.fat), on_change=self.update_values, text_align=ft.TextAlign.LEFT)
        self.txt_carbs = ft.TextField(label="Carbs", value=str(self.carbs), on_change=self.update_values, text_align=ft.TextAlign.LEFT)
        self.txt_protein = ft.TextField(label="Protein", value=str(self.protein), on_change=self.update_values, text_align=ft.TextAlign.LEFT)
        self.txt_kcal = ft.TextField(label="Kcal", value=str(self.kcal), on_change=self.update_values, text_align=ft.TextAlign.LEFT)

        row_macros = ft.Row(controls=[self.txt_name, self.txt_fat, self.txt_carbs, self.txt_protein, self.txt_kcal])

        self.controls = [
            row_macros
        ]

    def update_values(self, e):
        self.name = self.txt_name.value
        self.fat = float(self.txt_fat.value)
        self.carbs = float(self.txt_carbs.value)
        self.protein = float(self.txt_protein.value)
        self.kcal = int(self.txt_kcal.value)


class SimpleMacrosApp(ft.Column):
    # application's root control is a Column containing all other controls
    def __init__(self):
        super().__init__()

        self.ingredients = ft.Column()

        self.form_ingredient = Ingredient(name="NAMMMA", fat=0, carbs=0, protein=0, kcal=0)

        row_macros = ft.Row(controls=[self.form_ingredient])

        btn_add = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)
        btn_calculate = ft.FloatingActionButton(icon=ft.Icons.CALCULATE, on_click=self.calculate_click)

        self.txt_sum_of_macros = ft.TextField(label="Total", value="0", text_align=ft.TextAlign.JUSTIFY)
        
        self.controls = [
            ft.Row(controls=[row_macros]),
            ft.Row(controls=[btn_add, btn_calculate]),
            ft.Column(
                spacing=25,
                controls=[
                    self.ingredients,
                ],
            ),
            self.txt_sum_of_macros,
        ]

    def add_clicked(self, e):
        # self.form_ingredient.update_value()
        ingredient = Ingredient(name=self.form_ingredient.name,
                                fat=self.form_ingredient.fat,
                                carbs=self.form_ingredient.carbs,
                                protein=self.form_ingredient.protein,
                                kcal=self.form_ingredient.kcal)
        self.ingredients.controls.append(ingredient)
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

    # create application instance
    app = SimpleMacrosApp()

    # add application's root control to the page
    page.add(app)


ft.app(target=main)