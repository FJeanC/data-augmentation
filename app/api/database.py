import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('operation_registers.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registers 
                                (id INTEGER PRIMARY KEY, operation_type TEXT, status TEXT, ope_start_time TEXT, ope_end_time TEXT)''')
        self.connection.commit()
    
    def insert_register(self, operation_type, status, ope_start_time, ope_end_time):
        self.cursor.execute("INSERT INTO registers (operation_type, status, ope_start_time, ope_end_time) VALUES (?, ?, ?, ?)", 
                (operation_type, status, ope_start_time, ope_end_time))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_registers(self, status=None):
        if status is None:
            self.cursor.execute("SELECT * FROM registers")
        else:
            self.cursor.execute("SELECT * FROM registers WHERE status = ?", (status))
        rows = self.cursor.fetchall()
        return [{"id": row[0], "operation_type": row[1], "status": row[2], "ope_start_time": row[3], "ope_end_time": row[4]} for row in rows]
    
    def update_register(self, id, operation_type, status, ope_start_time, ope_end_time):
        self.cursor.execute("UPDATE registers SET operation_type = ?, status = ?,  ope_start_time = ?, ope_end_time = ? WHERE id = ?", 
                (operation_type, status, ope_start_time, ope_end_time, id))
        self.connection.commit()
        return self.cursor.rowcount
    
    def delete_register(self, id):
        self.cursor.execute("DELETE FROM registers WHERE id = ?", (id,))
        self.connection.commit()
        return self.cursor.rowcount
