import sqlite3
import threading

class DataBaseManager:
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataBaseManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Inicializando clase DataBaseManager...")
            self._initialized = True
            # No inicializamos la conexión aquí, solo cuando se necesite
    
    def _get_connection(self):
        # Crear conexión por hilo si no existe
        if not hasattr(self._local, 'connection'):
            print(f"Creando conexión para hilo: {threading.current_thread().ident}")
            self._local.connection = sqlite3.connect('database.db')
        return self._local.connection
    
    def _get_cursor(self):
        return self._get_connection().cursor()
    
    def create_tables(self):
        cursor = self._get_cursor()
        users_table = """CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(25) NOT NULL, 
            Email VARCHAR(100) NOT NULL, 
            Number VARCHAR(100) NOT NULL,
            Type VARCHAR(100) NOT NULL,
            Password VARCHAR(255) NOT NULL

        );"""
        
        medicamentos_table = """CREATE TABLE IF NOT EXISTS Medicamentos(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(100) NOT NULL,
            Uso TEXT,
            Dosis TEXT,
            Efectos_Secundarios TEXT,
            Recomendaciones_Alimenticias TEXT
        )"""

        medicamentos_usuario_table = """
            CREATE TABLE IF NOT EXISTS Medicamentos_Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                dia TEXT NOT NULL,          
                hora TEXT NOT NULL,        
                ciclo TEXT NOT NULL,  
                FOREIGN KEY(paciente_id) REFERENCES Usuarios(id)
            );"""
        
        cursor.execute(users_table)
        cursor.execute(medicamentos_table)
        cursor.execute(medicamentos_usuario_table)

        self._get_connection().commit()
        print("Tablas creadas...")

    def create_user(self, username, email, password, number, type):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Usuarios(Username, Email, Password, Number, Type) VALUES (?, ?, ?, ?, ?)", 
                    (username, email, password, number, type))
        self._get_connection().commit()
        cursor.execute("SELECT * FROM Usuarios WHERE Email=? AND Password=?", (email, password))
        return cursor.fetchone()
    
    def add_medicamento(self, nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias):
        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO Medicamentos(
                Nombre, 
                Uso, 
                Dosis, 
                Efectos_Secundarios, 
                Recomendaciones_Alimenticias
            ) VALUES(?, ?, ?, ?, ?)
        """, (nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias))
        self._get_connection().commit()
        print(f"Medicamento '{nombre}' añadido correctamente...")
    
    def get_medicamento_by_name(self, nombre):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        return cursor.fetchall()
    
    def login_user(self, email, password):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE Email=? AND Password=?", (email, password))
        return cursor.fetchone()


    def get_all_medicamentos(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos")
        return cursor.fetchall()
    
    def update_medicamento(self, id, nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias):
        cursor = self._get_cursor()
        cursor.execute("""
            UPDATE Medicamentos 
            SET Nombre=?, Uso=?, Dosis=?, Efectos_Secundarios=?, Recomendaciones_Alimenticias=?
            WHERE Id=?
        """, (nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias, id))
        self._get_connection().commit()
        print(f"Medicamento ID {id} actualizado correctamente...")
    
    def delete_medicamento(self, id):
        cursor = self._get_cursor()
        cursor.execute("DELETE FROM Medicamentos WHERE Id=?", (id,))
        self._get_connection().commit()
        print(f"Medicamento ID {id} eliminado correctamente...")
    
    def close_connection(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
            print("Conexión a la base de datos cerrada...")

    def get_usuario(self, usuario_id):
        cursor = self._get_cursor()

        # Obtener info del usuario
        cursor.execute("SELECT * FROM Usuarios WHERE Id=?", (usuario_id,))
        usuario_data = cursor.fetchone()
        if not usuario_data:
            return None

        # Crear diccionario de usuario 
        usuario = {
            "id": usuario_data[0],
            "nombre": usuario_data[1],
            "email": usuario_data[2],
            "telefono": usuario_data[5],  # Asumiendo que el teléfono está en la posición 4
            "tipo": usuario_data[4]       # Asumiendo que el tipo está en la posición 5
        }

        # Obtener medicamentos asociados
        cursor.execute("""
            SELECT nombre, dia, hora
            FROM Medicamentos_Usuarios
            WHERE paciente_id=?
        """, (usuario_id,))
        medicamentos = cursor.fetchall()

        # Convertir medicamentos a lista de diccionarios
        medicamentos_info = [
            {"Medicamento": nombre, "Día": dia, "Hora del día": hora}
            for nombre, dia, hora in medicamentos
        ]

        # Agregar medicamentos al diccionario del usuario
        usuario["medicamentos"] = medicamentos_info

        return usuario


    def add_medicamento_usuario(self, paciente_id, nombre, dia, hora,ciclo):
        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO Medicamentos_Usuarios(paciente_id, nombre, dia, hora,ciclo)
            VALUES (?, ?, ?, ?,?)
        """, (paciente_id, nombre, dia, hora, ciclo))
        self._get_connection().commit()
        print(f"Medicamento '{nombre}' asignado al paciente ID {paciente_id}")
        return 1
    def get_medicamento_usuario(self, paciente_id):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM Medicamentos_Usuarios WHERE paciente_id = ?", (paciente_id,))
        return cursor.fetchall()
if __name__ == '__main__':
    db = DataBaseManager()
    db.create_tables()