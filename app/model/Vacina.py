class Vacina:
    def __init__(self, nome, dataAplicacao, validade, pet_id, id=None):
        self.id = id
        self.nome = nome
        self.dataAplicacao = dataAplicacao
        self.validade = validade
        self.pet_id = pet_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "dataAplicacao": self.dataAplicacao,
            "validade": self.validade,
            "pet_id": self.pet_id
        }