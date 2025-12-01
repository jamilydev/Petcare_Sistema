class Veterinario:
    def __init__(self, nome, crmv, especialidade, telefone, email, id=None):
        self.id = id
        self.nome = nome
        self.crmv = crmv
        self.especialidade = especialidade
        self.telefone = telefone
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "crmv": self.crmv,
            "especialidade": self.especialidade,
            "telefone": self.telefone,
            "email": self.email
        }