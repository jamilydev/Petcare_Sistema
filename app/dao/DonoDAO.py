import sqlite3
import os
from app.model.Dono import Dono

class DonoDAO:
    def __init__(self):
        # Configuração do caminho do banco
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, '../database')
        self.db_path = os.path.join(db_dir, 'petcare.db')
        
        # Garante que a pasta existe
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

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
                telefone TEXT,
                senha TEXT NOT NULL
            );
        """)
        
        # Migração: Adiciona a coluna 'senha' se a tabela já existir sem ela
        try:
            # Verifica se a coluna senha existe
            cursor.execute("PRAGMA table_info(donos)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'senha' not in colunas:
                # Adiciona a coluna senha com valor padrão para registros existentes
                cursor.execute("ALTER TABLE donos ADD COLUMN senha TEXT DEFAULT '123456'")
        except Exception as e:
            # Se der erro, ignora (pode ser que a tabela não exista ainda)
            pass
        
        conn.commit()
        conn.close()

    def salvar(self, dono: Dono):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO donos (nome, email, telefone, senha) VALUES (?, ?, ?, ?)",
                       (dono.nome, dono._email, dono._telefone, dono.senha))
        dono.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return dono

    def autenticar(self, email, senha):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donos WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Retorna o objeto Dono se encontrou
            return Dono(row[1], row[2], row[3], row[4], id=row[0])
        return None

    def atualizar(self, dono):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE donos 
            SET nome = ?, email = ?, telefone = ?
            WHERE id = ?
        """, (dono.nome, dono._email, dono._telefone, dono.id))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donos")
        result = cursor.fetchall()
        conn.close()
        
        lista_donos = []
        for row in result:
            try:
                # Tenta criar com a senha (banco novo)
                dono = Dono(row[1], row[2], row[3], row[4], id=row[0])
            except IndexError:
                # Se der erro (banco antigo sem senha), usa senha padrão
                dono = Dono(row[1], row[2], row[3], "123456", id=row[0])
            
            lista_donos.append(dono.to_dict())
        return lista_donos

    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donos WHERE id = ?", (id,))
        conn.commit()
        conn.close()