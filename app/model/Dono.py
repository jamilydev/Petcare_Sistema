class Dono:
    def __init__(self, nome, email, telefone, id=None):
        self.id = id
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._listaPets = []

    # Seus Getters e Setters originais aqui...
    # [cite: 218-233]

    # Método essencial para API: Transforma o objeto em Dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self._nome,
            "email": self._email,
            "telefone": self._telefone
        }