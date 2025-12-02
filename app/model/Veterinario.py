class Veterinario:
    def __init__(self, nome, crmv, especialidade, telefone, email, senha, id=None): 
        self.id = id
        self.nome = nome
        self.crmv = crmv
        self.especialidade = especialidade
        self.telefone = telefone
        self.email = email
        self.senha = senha 

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "crmv": self.crmv,
            "especialidade": self.especialidade,
            "telefone": self.telefone,
            "email": self.email
        }

    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM veterinarios WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        