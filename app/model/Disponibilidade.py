class Disponibilidade:
    def __init__(self, veterinario_id, data, hora, status='livre', id=None):
        self.id = id
        self.veterinario_id = veterinario_id
        self.data = data
        self.hora = hora
        self.status = status # 'livre' ou 'ocupado'