import sqlite3
import os
from app.model.Consulta import Consulta

class ConsultaDAO:
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
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                hora TEXT,
                veterinario_id INTEGER,
                pet_id INTEGER,
                motivo TEXT,
                FOREIGN KEY(veterinario_id) REFERENCES veterinarios(id),
                FOREIGN KEY(pet_id) REFERENCES pets(id)
            );
        """)
        conn.commit()
        conn.close()

    def agendar(self, consulta: Consulta):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultas (data, hora, veterinario_id, pet_id, motivo)
            VALUES (?, ?, ?, ?, ?)
        """, (consulta.data, consulta.hora, consulta.veterinario_id, consulta.pet_id, consulta.motivo))
        consulta.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return consulta

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultas")
        result = cursor.fetchall()
        conn.close()
        lista = []
        for row in result:
            lista.append(Consulta(row[1], row[2], row[3], row[4], row[5], id=row[0]).to_dict())
        return lista