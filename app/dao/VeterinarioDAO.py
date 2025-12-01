import sqlite3
import os
from app.model.Veterinario import Veterinario

class VeterinarioDAO:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(base_dir, '../database')
        self.db_path = os.path.join(db_dir, 'petcare.db')
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
                email TEXT
            );
        """)
        conn.commit()
        conn.close()

    def salvar(self, vet: Veterinario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO veterinarios (nome, crmv, especialidade, telefone, email)
            VALUES (?, ?, ?, ?, ?)
        """, (vet.nome, vet.crmv, vet.especialidade, vet.telefone, vet.email))
        vet.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vet

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM veterinarios")
        result = cursor.fetchall()
        conn.close()
        lista = []
        for row in result:
            lista.append(Veterinario(row[1], row[2], row[3], row[4], row[5], id=row[0]).to_dict())
        return lista