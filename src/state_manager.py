class StateManager:
    current_page = None
    base_layout = None

    @staticmethod
    def pages():
        from pages.add_edit_ingredient import AddEditIngredientsPage
        from pages.ingredients import IngredientsPage

        class Pages:
            ADD_EDIT = AddEditIngredientsPage
            INGREDIENTS = IngredientsPage

        return Pages
    
    @classmethod
    def change_page(cls, page_class, **kwargs):
        page = page_class(**kwargs)
        cls.current_page = page
        cls.base_layout.change_page(page)

# StateManager = StateManager1()