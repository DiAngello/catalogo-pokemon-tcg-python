class Carta:
    def __init__(
        self,
        id_carta: str,
        id_colecao: str,
        numero: str,
        nome: str,
        imagem_url: str,
        idioma: str
    ):
        self.id_carta = id_carta
        self.id_colecao = id_colecao
        self.numero = numero
        self.nome = nome
        self.imagem_url = imagem_url
        self.idioma = idioma

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    def to_tuple(self):
        return (
            self.id_carta,
            self.id_colecao,
            self.numero,
            self.nome,
            self.imagem_url,
            self.idioma
        )