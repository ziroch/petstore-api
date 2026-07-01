from app.database import get_connection

def create_pet(name: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pets (name, status) VALUES (?, ?)",
        (name, status)
    )
    conn.commit()
    pet_id = cursor.lastrowid
    conn.close()
    return pet_id

def get_pet(pet_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets WHERE id = ?", (pet_id,))
    pet = cursor.fetchone()
    conn.close()
    return pet

def list_pets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()
    return pets
