import sqlite3
import os
from app.model.Pet import Pet

class PetDAO:
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
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dono_id INTEGER NOT NULL,
                especie TEXT,
                raca TEXT,
                idade INTEGER,
                peso REAL,
                data_nascimento TEXT,
                FOREIGN KEY(dono_id) REFERENCES donos(id)
            );
        """)
        
        # Migração: Adiciona a coluna 'data_nascimento' se a tabela já existir sem ela
        try:
            cursor.execute("PRAGMA table_info(pets)")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            
            if 'data_nascimento' not in colunas:
                cursor.execute("ALTER TABLE pets ADD COLUMN data_nascimento TEXT DEFAULT ''")
        except Exception as e:
            pass
        
        conn.commit()
        conn.close()

    def salvar(self, pet: Pet):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pets (nome, dono_id, especie, raca, idade, peso, data_nascimento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pet.nome, pet.dono_id, pet.especie, pet.raca, pet.idade, pet.peso, pet.data_nascimento))
        pet.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pet

    # --- NOVO: Método para Atualizar ---
    def atualizar(self, pet: Pet):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pets 
            SET nome=?, especie=?, raca=?, idade=?, peso=?, data_nascimento=?
            WHERE id=?
        """, (pet.nome, pet.especie, pet.raca, pet.idade, pet.peso, pet.data_nascimento, pet.id))
        conn.commit()
        conn.close()

    # --- NOVO: Buscar apenas 1 pet para preencher o formulário ---
    def buscar_por_id(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # row: id, nome, dono_id, especie, raca, idade, peso, data_nascimento
            return Pet(row[1], row[2], row[3], row[4], row[5], row[6], row[7], id=row[0])
        return None

    def listar(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets")
        result = cursor.fetchall()
        conn.close()
        
        pets = []
        for row in result:
            # Fallback para caso o banco antigo ainda esteja lá sem a coluna data (evita erro)
            try:
                data_nasc = row[7]
            except IndexError:
                data_nasc = ""

            pet = Pet(row[1], row[2], row[3], row[4], row[5], row[6], data_nasc, id=row[0])
            pets.append(pet.to_dict())
        return pets

    def excluir(self, id):
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM vacinas WHERE pet_id = ?", (id,))
        except: pass
        try:
            cursor.execute("DELETE FROM consultas WHERE pet_id = ?", (id,))
        except: pass
        
        cursor.execute("DELETE FROM pets WHERE id = ?", (id,))
        conn.commit()
        conn.close()