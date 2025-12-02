import sqlite3
import os
from app.model.Veterinario import Veterinario

class VeterinarioDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, '../database')
        self.db_path = os.path.join(db_dir, 'petcare.db')
        
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _criar_tabela(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS veterinarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                crmv TEXT NOT NULL UNIQUE,
                especialidade TEXT,
                telefone TEXT,
                email TEXT,
                senha TEXT NOT NULL
            );
        """)
        
        # Migração: Adiciona a coluna 'senha' se a tabela já existir sem ela
        try:
            cursor.execute("PRAGMA table_info(veterinarios)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'senha' not in colunas:
                cursor.execute("ALTER TABLE veterinarios ADD COLUMN senha TEXT DEFAULT '123456'")
        except Exception as e:
            pass
        
        conn.commit()
        conn.close()

    def salvar(self, vet: Veterinario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO veterinarios (nome, crmv, especialidade, telefone, email, senha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vet.nome, vet.crmv, vet.especialidade, vet.telefone, vet.email, vet.senha))
        vet.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vet

    def autenticar(self, email, senha):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM veterinarios WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Retorna o objeto Veterinario
            return Veterinario(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0])
        return None

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM veterinarios")
        result = cursor.fetchall()
        conn.close()
        
        lista_vets = []
        for row in result:
            try:
                vet = Veterinario(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0])
            except IndexError:
                vet = Veterinario(row[1], row[2], row[3], row[4], row[5], "123456", id=row[0])
            lista_vets.append(vet.to_dict())
        return lista_vets

    # --- A FUNÇÃO QUE FALTAVA ---
    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        
        # 1. Apaga as disponibilidades desse vet (Limpeza)
        try:
            cursor.execute("DELETE FROM disponibilidades WHERE veterinario_id = ?", (id,))
        except:
            pass 

        # 2. Apaga o Veterinário
        cursor.execute("DELETE FROM veterinarios WHERE id = ?", (id,))
        conn.commit()
        conn.close()