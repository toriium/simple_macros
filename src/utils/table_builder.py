class TableBuilder:
    def __init__(self, table: any, data_list: list) -> None:
        self.table = table
        self.data_list = data_list
        self.columns: list[str] = None
        self.data_table: list = []

        self.build()

    def build(self):
        self.columns = [key for key in self.table().columns()]

        data_table: list[list] = []
        for data in self.data_list:
            row = [getattr(data, key) for key in self.columns]
            tuple_data = (data, row)
            data_table.append(tuple_data)
        self.data_table = data_table
