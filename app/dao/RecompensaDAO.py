import sqlite3
import os
from app.model.Recompensa import Recompensa
class RecompensaDAO:
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
            CREATE TABLE IF NOT EXISTS recompensas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pontos INTEGER,
                nivel INTEGER,
                dono_id INTEGER UNIQUE,
                FOREIGN KEY(dono_id) REFERENCES donos(id)
            );
        """)
        conn.commit()
        conn.close()

    def salvar_ou_atualizar(self, recompensa: Recompensa):
        # Verifica se o dono já tem pontuação
        conn = self._conectar()
        cursor = conn.cursor()
        
        # Tenta atualizar primeiro
        cursor.execute("""
            UPDATE recompensas SET pontos = ?, nivel = ? WHERE dono_id = ?
        """, (recompensa.pontos, recompensa.nivel, recompensa.dono_id))
        
        if cursor.rowcount == 0:
            # Se não atualizou nada, é porque não existe, então insere
            cursor.execute("""
                INSERT INTO recompensas (pontos, nivel, dono_id) VALUES (?, ?, ?)
            """, (recompensa.pontos, recompensa.nivel, recompensa.dono_id))
            recompensa.id = cursor.lastrowid
            
        conn.commit()
        conn.close()
        return recompensa

    def buscar_por_dono(self, dono_id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recompensas WHERE dono_id = ?", (dono_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Recompensa(row[1], row[2], row[3], id=row[0]).to_dict()
        return None
    def excluir_por_dono(self, dono_id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recompensas WHERE dono_id = ?", (dono_id,))
        conn.commit()
        conn.close()