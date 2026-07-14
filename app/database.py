import sqlite3
from typing import List, Optional, Dict, Any


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()

        # Tabla Pets
        cursor.execute("""
            CREATE TABLE pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                photoUrls TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                status TEXT
            )
        """)

        # Tabla Orders
        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                petId INTEGER,
                quantity INTEGER,
                shipDate TEXT,
                status TEXT,
                complete INTEGER DEFAULT 0
            )
        """)

        # Tabla Users
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                firstName TEXT,
                lastName TEXT,
                email TEXT,
                password TEXT,
                phone TEXT,
                userStatus INTEGER
            )
        """)
        self.conn.commit()

    # ─── PET CRUD ─────────────────────────────────
    def create_pet(self, pet_data: Dict[str, Any]) -> int:
        import json
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO pets (name, photoUrls, category, tags, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            pet_data["name"],
            json.dumps(pet_data.get("photoUrls", [])),
            json.dumps(pet_data.get("category")) if pet_data.get("category") else None,
            json.dumps(pet_data.get("tags", [])) if pet_data.get("tags") else None,
            pet_data.get("status")
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_pet(self, pet_id: int) -> Optional[Dict]:
        import json
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pets WHERE id = ?", (pet_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "name": row["name"],
            "photoUrls": json.loads(row["photoUrls"]) if row["photoUrls"] else [],
            "category": json.loads(row["category"]) if row["category"] else None,
            "tags": json.loads(row["tags"]) if row["tags"] else [],
            "status": row["status"]
        }

    def update_pet(self, pet_id: int, pet_data: Dict[str, Any]) -> bool:
        import json
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE pets SET name=?, photoUrls=?, category=?, tags=?, status=?
            WHERE id=?
        """, (
            pet_data["name"],
            json.dumps(pet_data.get("photoUrls", [])),
            json.dumps(pet_data.get("category")) if pet_data.get("category") else None,
            json.dumps(pet_data.get("tags", [])) if pet_data.get("tags") else None,
            pet_data.get("status"),
            pet_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_pet(self, pet_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def find_pets_by_status(self, status_list: List[str]) -> List[Dict]:
        import json
        cursor = self.conn.cursor()
        placeholders = ",".join("?" * len(status_list))
        cursor.execute(f"SELECT * FROM pets WHERE status IN ({placeholders})", status_list)
        rows = cursor.fetchall()
        return [{
            "id": r["id"],
            "name": r["name"],
            "photoUrls": json.loads(r["photoUrls"]) if r["photoUrls"] else [],
            "category": json.loads(r["category"]) if r["category"] else None,
            "tags": json.loads(r["tags"]) if r["tags"] else [],
            "status": r["status"]
        } for r in rows]

    def find_pets_by_tags(self, tag_names: List[str]) -> List[Dict]:
        import json
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pets")
        rows = cursor.fetchall()
        result = []
        for r in rows:
            tags = json.loads(r["tags"]) if r["tags"] else []
            if any(t.get("name") in tag_names for t in tags if isinstance(t, dict)):
                result.append({
                    "id": r["id"],
                    "name": r["name"],
                    "photoUrls": json.loads(r["photoUrls"]) if r["photoUrls"] else [],
                    "category": json.loads(r["category"]) if r["category"] else None,
                    "tags": tags,
                    "status": r["status"]
                })
        return result

    def get_all_pets(self) -> List[Dict]:
        import json
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pets")
        rows = cursor.fetchall()
        return [{
            "id": r["id"],
            "name": r["name"],
            "photoUrls": json.loads(r["photoUrls"]) if r["photoUrls"] else [],
            "category": json.loads(r["category"]) if r["category"] else None,
            "tags": json.loads(r["tags"]) if r["tags"] else [],
            "status": r["status"]
        } for r in rows]

    # ─── ORDER CRUD ───────────────────────────────
    def create_order(self, order_data: Dict[str, Any]) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO orders (petId, quantity, shipDate, status, complete)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_data.get("petId"),
            order_data.get("quantity"),
            order_data.get("shipDate"),
            order_data.get("status"),
            1 if order_data.get("complete") else 0
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_order(self, order_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "petId": row["petId"],
            "quantity": row["quantity"],
            "shipDate": row["shipDate"],
            "status": row["status"],
            "complete": bool(row["complete"])
        }

    def delete_order(self, order_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_inventory(self) -> Dict[str, int]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM pets GROUP BY status")
        rows = cursor.fetchall()
        return {r["status"] or "unknown": r["count"] for r in rows}

    # ─── USER CRUD ────────────────────────────────
    def create_user(self, user_data: Dict[str, Any]) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, firstName, lastName, email, password, phone, userStatus)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data.get("username"),
            user_data.get("firstName"),
            user_data.get("lastName"),
            user_data.get("email"),
            user_data.get("password"),
            user_data.get("phone"),
            user_data.get("userStatus")
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
        return dict(row)

    def update_user(self, username: str, user_data: Dict[str, Any]) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE users SET firstName=?, lastName=?, email=?, password=?, phone=?, userStatus=?
            WHERE username=?
        """, (
            user_data.get("firstName"),
            user_data.get("lastName"),
            user_data.get("email"),
            user_data.get("password"),
            user_data.get("phone"),
            user_data.get("userStatus"),
            username
        ))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_user(self, username: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


db = Database()
