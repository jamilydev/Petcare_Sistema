import sqlite3
import os
from app.model.Pet import Pet

class PetDAO:
    def __init__(self):
        # Configuração do caminho do banco (igual ao DonoDAO)
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
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dono_id INTEGER NOT NULL,
                especie TEXT,
                raca TEXT,
                idade INTEGER,
                peso REAL,
                FOREIGN KEY(dono_id) REFERENCES donos(id)
            );
        """)
        conn.commit()
        conn.close()

    def salvar(self, pet: Pet):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pets (nome, dono_id, especie, raca, idade, peso)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pet.nome, pet.dono_id, pet.especie, pet.raca, pet.idade, pet.peso))
        pet.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pet

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets")
        result = cursor.fetchall()
        conn.close()
        
        pets = []
        for row in result:
            # row ordem: id, nome, dono_id, especie, raca, idade, peso
            pet = Pet(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0])
            pets.append(pet.to_dict())
        return pets
    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donos WHERE id = ?", (id,))
        conn.commit()
        conn.close()