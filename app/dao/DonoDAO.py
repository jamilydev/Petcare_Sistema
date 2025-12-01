import sqlite3
import os
from app.model.Dono import Dono

class DonoDAO:
    def __init__(self):
        # --- Bloco para resolver o problema de caminho do banco ---
        # Pega o diretório onde este arquivo (DonoDAO.py) está
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        # Sobe um nível e entra na pasta database
        db_dir = os.path.join(base_dir, '../database')        
        # Define o arquivo final
        self.db_path = os.path.join(db_dir, 'petcare.db')     
        
        # Garante que a pasta existe
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        # ---------------------------------------------------------

        # Chama a função para criar a tabela (O erro estava aqui porque esta função abaixo não existia)
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _criar_tabela(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT
            );
        """)
        conn.commit()
        conn.close()

    def salvar(self, dono: Dono):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO donos (nome, email, telefone) VALUES (?, ?, ?)",
                       (dono._nome, dono._email, dono._telefone)) # <-- CORRIGIDO AQUI
        dono.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return dono

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donos")
        result = cursor.fetchall()
        conn.close()
        
        donos = []
        for row in result:
            # row[0]=id, row[1]=nome, row[2]=email, row[3]=telefone
            obj = Dono(row[1], row[2], row[3], id=row[0])
            donos.append(obj.to_dict())
        return donos

    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pets WHERE id = ?", (id,))
        conn.commit()
        conn.close()
