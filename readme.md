# Sistema de Gestión de Medicamentos con Flask

Este proyecto consiste en una aplicación web desarrollada con Flask que permite la gestión de medicamentos, interacciones entre ellos, y alarmas para recordatorios de toma de medicación.

![Estructura del Proyecto](https://raw.githubusercontent.com/IsaacCorrales03/medical/refs/heads/main/estructura.jpg)

## Estructura del Proyecto

El proyecto está organizado en carpetas para separar el código del servidor, la base de datos, y los recursos estáticos:

- `app.py`: Archivo principal de Flask
- `database.py`: Gestor de base de datos
- `database.db`: Base de datos SQLite
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `templates/`: Plantillas HTML con Jinja2

## Explicación del Código
## Archivo Principal (app.py)

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

@app.route('/medicamentos', methods=['GET'])
def medicamentos():
    if request.args:
        name = request.args.get('name')
        medicamentos = my_db.get_medicamento_by_name(name)
    else:
        medicamentos = my_db.get_all_medicamentos()
    return render_template('medicamentos.html', medicamentos=medicamentos)

app.run(port=1010, debug=True)
```

Este archivo es el punto de entrada de la aplicación Flask. Define cuatro rutas principales:

- **/** - La página de inicio que renderiza `index.html`
- **/login** - Maneja tanto la visualización del formulario de inicio de sesión (GET) como el procesamiento del formulario enviado (POST)
- **/register** - Similar a login, maneja la visualización y procesamiento del formulario de registro
- **/medicamentos** - Muestra todos los medicamentos o permite filtrar por nombre mediante un parámetro de consulta

El servidor se ejecuta en el puerto 1010 con el modo de depuración activado.

# Gestor de Base de Datos (database.py)

## Descripción General

El archivo `database.py` implementa un gestor de base de datos SQLite utilizando el patrón Singleton con seguridad para múltiples hilos. Esta implementación garantiza que las conexiones a la base de datos se manejen correctamente en entornos multi-hilo, evitando problemas de concurrencia.

## Características Principales

### Patrón Singleton Thread-Safe
- Mantiene una única instancia de la clase a nivel de aplicación
- Proporciona conexiones independientes para cada hilo
- Utiliza bloqueos para evitar condiciones de carrera durante la inicialización

### Gestión de Conexiones
- Inicialización perezosa: las conexiones se crean solo cuando son necesarias
- Cada hilo obtiene su propia conexión aislada
- Cierre explícito de conexiones para liberar recursos

### Estructura de la Base de Datos
La clase gestiona dos tablas principales:

1. **Usuarios**:
   - `Id`: Identificador único autoincremental
   - `Username`: Nombre de usuario (limitado a 25 caracteres)
   - `Email`: Correo electrónico (limitado a 100 caracteres)
   - `Password`: Contraseña almacenada (hasta 255 caracteres)

2. **Medicamentos**:
   - `Id`: Identificador único autoincremental
   - `Nombre`: Nombre del medicamento
   - `Uso`: Descripción del uso terapéutico
   - `Dosis`: Información sobre la posología
   - `Efectos_Secundarios`: Posibles efectos adversos
   - `Recomendaciones_Alimenticias`: Consejos sobre alimentación relacionados con el medicamento

## Métodos Disponibles

### Gestión de Usuarios
- `create_user(username, email, password)`: Registra un nuevo usuario en la base de datos

### Gestión de Medicamentos
- `add_medicamento(nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias)`: Añade un nuevo medicamento
- `get_medicamento_by_name(nombre)`: Busca medicamentos que coincidan parcialmente con el nombre proporcionado
- `get_all_medicamentos()`: Obtiene todos los medicamentos almacenados
- `update_medicamento(id, nombre, uso, dosis, efectos_secundarios, recomendaciones_alimenticias)`: Actualiza la información de un medicamento existente
- `delete_medicamento(id)`: Elimina un medicamento de la base de datos

### Utilidades
- `create_tables()`: Crea las tablas necesarias si no existen
- `close_connection()`: Cierra la conexión del hilo actual a la base de datos

## Ejemplo de Uso

```python
# Inicializar el gestor de base de datos
db = DataBaseManager()
db.create_tables()

# Añadir un medicamento
db.add_medicamento(
    nombre="Paracetamol",
    uso="Alivio del dolor y reducción de la fiebre.",
    dosis="500 mg cada 6 horas, no exceder 4 g al día.",
    efectos_secundarios="Raras veces, daño hepático en dosis altas.",
    recomendaciones_alimenticias="Puede tomarse con o sin alimentos."
)

# Buscar medicamentos por nombre
resultados = db.get_medicamento_by_name("Para")

# Cerrar la conexión cuando termine
db.close_connection()
```

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
```bash
git clone "https://github.com/IsaacCorrales03/medical.git"
pip install -r requirements.txt
python server.py
```