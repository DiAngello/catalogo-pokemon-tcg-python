class Fichario:
    def __init__(
        self,
        id_fichario: str,
        nome: str,
        is_custom: int = 0
    ):
        self.id_fichario = id_fichario
        self.nome = nome
        self.is_custom = is_custom

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    def to_tuple(self):
        return (
            self.id_fichario,
            self.nome,
            self.is_custom
        )