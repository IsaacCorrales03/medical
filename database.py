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
            Password VARCHAR(255) NOT NULL
        )"""
        
        medicamentos_table = """CREATE TABLE IF NOT EXISTS Medicamentos(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre VARCHAR(100) NOT NULL,
            Uso TEXT,
            Dosis TEXT,
            Efectos_Secundarios TEXT,
            Recomendaciones_Alimenticias TEXT
        )"""
        
        cursor.execute(users_table)
        cursor.execute(medicamentos_table)
        self._get_connection().commit()
        print("Tablas creadas...")

    def create_user(self, username, email, password):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO Usuarios(Username, Email, Password) VALUES(?, ?, ?)", 
                      (username, email, password))
        self._get_connection().commit()
        print("Usuario creado...")
    
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