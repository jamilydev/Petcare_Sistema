import sqlite3
import os
from app.model.Disponibilidade import Disponibilidade

class DisponibilidadeDAO:
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
            CREATE TABLE IF NOT EXISTS disponibilidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                veterinario_id INTEGER,
                data TEXT,
                hora TEXT,
                status TEXT,
                FOREIGN KEY(veterinario_id) REFERENCES veterinarios(id)
            );
        """)
        conn.commit()
        conn.close()

    def criar(self, disp):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO disponibilidades (veterinario_id, data, hora, status) VALUES (?, ?, ?, ?)",
                       (disp.veterinario_id, disp.data, disp.hora, disp.status))
        conn.commit()
        conn.close()

    def listar_por_vet(self, vet_id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM disponibilidades WHERE veterinario_id = ? ORDER BY data, hora", (vet_id,))
        result = cursor.fetchall()
        conn.close()
        return [Disponibilidade(row[1], row[2], row[3], row[4], id=row[0]) for row in result]

    def listar_livres(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM disponibilidades WHERE status = 'livre' ORDER BY data, hora")
        result = cursor.fetchall()
        conn.close()
        return [Disponibilidade(row[1], row[2], row[3], row[4], id=row[0]) for row in result]

    def ocupar_vaga(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE disponibilidades SET status = 'ocupado' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM disponibilidades WHERE id = ?", (id,))
        conn.commit()
        conn.close()