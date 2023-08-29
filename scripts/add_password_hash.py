"""Script to add password hashes"""

import sqlite3
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash

BYTES_KEY = bytes("FERNET_KEY", encoding="utf-8")
fernet = Fernet(BYTES_KEY)

conn = sqlite3.connect("instance/prod.sqlite3")
cursor = conn.cursor()


def decrypt(encrypted_string: bytes) -> str:
    """Decrypt bytes string.

    Args:
        encrypted_string (bytes): Encrypted string

    Returns:
        str: Decrypted string
    """
    return fernet.decrypt(encrypted_string).decode()


cursor.execute("SELECT eid, password FROM employees")

for eid, password in cursor.fetchall():
    cursor.execute(
        f"UPDATE employees SET password_hash='{generate_password_hash(decrypt(password))}' WHERE eid='{eid}'"
    )

conn.commit()
conn.close()
