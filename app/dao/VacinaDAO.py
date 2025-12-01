import sqlite3
import os
from app.model.Vacina import Vacina

class VacinaDAO:
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
            CREATE TABLE IF NOT EXISTS vacinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dataAplicacao TEXT,
                validade TEXT,
                pet_id INTEGER,
                FOREIGN KEY(pet_id) REFERENCES pets(id)
            );
        """)
        conn.commit()
        conn.close()

    def aplicar(self, vacina: Vacina):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vacinas (nome, dataAplicacao, validade, pet_id)
            VALUES (?, ?, ?, ?)
        """, (vacina.nome, vacina.dataAplicacao, vacina.validade, vacina.pet_id))
        vacina.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vacina

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vacinas")
        result = cursor.fetchall()
        conn.close()
        lista = []
        for row in result:
            lista.append(Vacina(row[1], row[2], row[3], row[4], id=row[0]).to_dict())
        return lista
        