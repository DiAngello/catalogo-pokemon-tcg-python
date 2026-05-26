class Inventario:
    def __init__(
        self,
        id_inventario: int,
        id_carta: str,
        id_fichario: str,
        quantidade: int = 1,
        extras: str = "Normal",
        data_aquisicao=None
    ):
        self.id_inventario = id_inventario
        self.id_carta = id_carta
        self.id_fichario = id_fichario
        self.quantidade = quantidade
        self.extras = extras
        self.data_aquisicao = data_aquisicao

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    def to_tuple(self):
        return (
            self.id_inventario,
            self.id_carta,
            self.id_fichario,
            self.quantidade,
            self.extras,
            self.data_aquisicao
        )