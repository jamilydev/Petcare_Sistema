class Recompensa:
    # Atributo de classe mencionado no seu PDF
    taxaBonus = 1.2 

    def __init__(self, pontos, nivel, dono_id, id=None):
        self.id = id
        self.pontos = pontos
        self.nivel = nivel
        self.dono_id = dono_id

    def to_dict(self):
        return {
            "id": self.id,
            "pontos": self.pontos,
            "nivel": self.nivel,
            "dono_id": self.dono_id,
            "taxaBonus": self.taxaBonus
        }