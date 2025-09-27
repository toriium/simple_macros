import flet as ft


class Ingredient(ft.Column):
    def __init__(self, name, fat, carbs, protein, kcal):
        super().__init__()
        self.name = name
        self.fat = float(fat)
        self.carbs = float(carbs)
        self.protein = float(protein)
        self.kcal = int(kcal)

        self.txt_name = ft.TextField(label="Name", value=self.name, text_align=ft.TextAlign.LEFT)
        self.txt_fat = ft.TextField(label="Fat", value=str(self.fat), text_align=ft.TextAlign.RIGHT)
        self.txt_carbs = ft.TextField(label="Carbs", value=str(self.carbs), text_align=ft.TextAlign.RIGHT)
        self.txt_protein = ft.TextField(label="Protein", value=str(self.protein), text_align=ft.TextAlign.RIGHT)
        self.txt_kcal = ft.TextField(label="Kcal", value=str(self.kcal), text_align=ft.TextAlign.RIGHT)

        row_macros = ft.Row(controls=[self.txt_name, self.txt_fat, self.txt_carbs, self.txt_protein, self.txt_kcal])

        self.controls = [
            row_macros
        ]


class SimpleMacrosApp(ft.Column):
    # application's root control is a Column containing all other controls
    def __init__(self):
        super().__init__()

        self.ingredients = ft.Column()


        self.txt_name = ft.TextField(label="Name", value="", text_align=ft.TextAlign.LEFT)
        self.txt_fat = ft.TextField(label="Fat", value="0", text_align=ft.TextAlign.RIGHT)
        self.txt_carbs = ft.TextField(label="Carbs", value="0", text_align=ft.TextAlign.RIGHT)
        self.txt_protein = ft.TextField(label="Protein", value="0", text_align=ft.TextAlign.RIGHT)
        self.txt_kcal = ft.TextField(label="Kcal", value="0", text_align=ft.TextAlign.RIGHT)



        row_macros = ft.Row(controls=[self.txt_name, self.txt_fat, self.txt_carbs, self.txt_protein, self.txt_kcal])

        self.txt_sum_of_macros = ft.TextField(label="Total", value="0", text_align=ft.TextAlign.JUSTIFY)

        btn_add = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)
        btn_calculate = ft.FloatingActionButton(icon=ft.Icons.CALCULATE, on_click=self.calculate_click)

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
        ingredient = Ingredient(self.txt_name.value, self.txt_fat.value, self.txt_carbs.value, self.txt_protein.value, self.txt_kcal.value)
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