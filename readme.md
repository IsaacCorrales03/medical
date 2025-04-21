# Sistema de Gestión de Medicamentos con Flask

Este proyecto consiste en una aplicación web desarrollada con Flask que permite la gestión de medicamentos, interacciones entre ellos, y alarmas para recordatorios de toma de medicación.

![Estructura del Proyecto](https://placehold.co/600x400?text=Estructura+del+Proyecto)

## Estructura del Proyecto

El proyecto está organizado en carpetas para separar el código del servidor, la base de datos, y los recursos estáticos:

- `app.py`: Archivo principal de Flask
- `database.py`: Gestor de base de datos
- `database.db`: Base de datos SQLite
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `templates/`: Plantillas HTML con Jinja2

## Explicación del Código

### Archivo Principal (app.py)

```python
from flask import * 
from database import DataBaseManager
app = Flask("__main__")
app.static_folder = 'static'

my_db = DataBaseManager()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        pass
        # lógica para el inicio de sesión 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        pass
        # lógica de registro

app.run(port=1010, debug=True)
```

Este archivo es el punto de entrada de la aplicación Flask. Define tres rutas principales:

- **/** - La página de inicio que renderiza `index.html`
- **/login** - Maneja tanto la visualización del formulario de inicio de sesión (GET) como el procesamiento del formulario enviado (POST)
- **/register** - Similar a login, maneja la visualización y procesamiento del formulario de registro

El servidor se ejecuta en el puerto 1010 con el modo de depuración activado.

### Gestor de Base de Datos (database.py)

```python
import sqlite3

class DataBaseManager:
    def __init__(self):
        print("Iniciando base de datos...")
        self.my_connection = sqlite3.connect('database.db')
        self.my_cursor = self.my_connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        users_table = """CREATE TABLE IF NOT EXISTS Usuarios(Id INTEGER PRIMARY KEY AUTOINCREMENT,  Username VARCHAR(25) NOT NULL, Email VARCHAR(100) NOT NULL, Password VARCHAR(255) NOT NULL)"""
        self.my_cursor.execute(users_table)
        self.my_connection.commit()
        print("Tablas creadas...")
    
    def create_user(self, username, email, password):
        self.my_cursor.execute("INSERT INTO Usuarios(Username, Email, Password) VALUES(?, ?, ?)", (username, email, password))
        self.my_connection.commit()
        print("Usuario creado...")
```

Esta clase maneja las interacciones con la base de datos SQLite. Incluye:

- **Inicialización**: Establece la conexión a la base de datos y crea las tablas necesarias si no existen.
- **create_tables()**: Crea la tabla de Usuarios con campos para ID, nombre de usuario, email y contraseña.
- **create_user()**: Método para insertar un nuevo usuario en la base de datos.

## Front-end con Tailwind CSS

El proyecto utiliza Tailwind CSS como framework de diseño, lo que permite un desarrollo rápido y responsivo con clases de utilidad predefinidas. Esto facilita mantener un diseño coherente en toda la aplicación sin necesidad de escribir CSS personalizado extenso.

Los archivos de estilo se encuentran en la carpeta `static/styles/`, y se vinculan a las plantillas HTML.

## Plantillas con Jinja2

Las plantillas HTML utilizan el motor de plantillas Jinja2, que viene integrado con Flask. Esto permite:

- Extender plantillas base (layouts)
- Pasar datos desde Flask a las plantillas
- Uso de condicionales y bucles en el HTML
- Reutilización de componentes

## Métodos HTTP: GET y POST

- **GET**: Utilizado cuando el usuario accede a una página para visualizar información. Por ejemplo, al cargar el formulario de inicio de sesión o registro.
- **POST**: Utilizado cuando el usuario envía datos al servidor. Por ejemplo, al enviar credenciales de inicio de sesión o datos de registro.

En el código actual, la lógica para procesar los datos POST está pendiente de implementar.

## Base de Datos

Actualmente, el proyecto utiliza SQLite como sistema de gestión de base de datos, ideal para desarrollo y aplicaciones pequeñas a medianas. Hay planes de migrar a PostgreSQL en el futuro para mayor escalabilidad y funcionalidades avanzadas.

## Estado Actual del Proyecto

### Páginas Completadas (Diseño):
- ✅ Página de inicio
- ✅ Inicio de sesión
- ✅ Registro

### Páginas Pendientes:
- ⏳ **Medicamentos**: Gestión y visualización de medicamentos
- ⏳ **Interacciones**: Análisis de interacciones entre medicamentos
- ⏳ **Blog**: Artículos informativos sobre salud y medicamentos
- ⏳ **Cuenta**: Perfil de usuario y configuraciones
- ⏳ **Categorías**: Clasificación de medicamentos
- ⏳ **Añadir alarma**: Sistema de recordatorios para toma de medicamentos

## Enfoque del Proyecto

El proyecto ha priorizado el diseño y la experiencia de usuario, utilizando Tailwind CSS para lograr una interfaz atractiva y responsiva. 

El desarrollo del backend está en sus etapas iniciales, con la implementación básica de rutas y la estructura de la base de datos, pero con varios aspectos pendientes de completar como la autenticación de usuarios y la lógica de negocio para la gestión de medicamentos e interacciones.

La migración planeada de SQLite a PostgreSQL representa un paso hacia una aplicación más robusta y escalable, indicando la intención de evolucionar el proyecto hacia un sistema más completo y profesional.

## Como instalar
