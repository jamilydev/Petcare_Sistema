class Consulta:
    def __init__(self, data, hora, veterinario_id, pet_id, motivo, id=None):
        self.id = id
        self.data = data
        self.hora = hora
        self.veterinario_id = veterinario_id
        self.pet_id = pet_id
        self.motivo = motivo

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "hora": self.hora,
            "veterinario_id": self.veterinario_id,
            "pet_id": self.pet_id,
            "motivo": self.motivo
        }