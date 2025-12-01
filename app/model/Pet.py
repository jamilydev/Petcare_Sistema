class Pet:
    def __init__(self, nome, dono_id, especie, raca, idade, peso, id=None):
        self.id = id
        self.nome = nome
        self.dono_id = dono_id  # ID do dono no banco de dados
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.peso = peso

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "dono_id": self.dono_id,
            "especie": self.especie,
            "raca": self.raca,
            "idade": self.idade,
            "peso": self.peso
        }