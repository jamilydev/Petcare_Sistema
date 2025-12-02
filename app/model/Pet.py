class Pet:
    def __init__(self, nome, dono_id, especie, raca, idade, peso, data_nascimento, id=None):
        self.id = id
        self.nome = nome
        self.dono_id = dono_id
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.peso = peso
        self.data_nascimento = data_nascimento # <--- Novo Campo

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "dono_id": self.dono_id,
            "especie": self.especie,
            "raca": self.raca,
            "idade": self.idade,
            "peso": self.peso,
            "data_nascimento": self.data_nascimento
        }