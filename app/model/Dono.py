class Dono:
    def __init__(self, nome, email, telefone, senha, id=None): # <--- Adicione senha
        self.id = id
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self.senha = senha 

    @property
    def nome(self): return self._nome
    # ... (outros getters se houver)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self._nome,
            "email": self._email,
            "telefone": self._telefone
            # Não retornamos a senha aqui por segurança
        }