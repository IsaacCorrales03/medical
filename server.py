from flask import * 
from database import DataBaseManager
from flask_mail import Message, Mail
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask("__main__")
app.static_folder = 'static'

# Configuración desde variables de entorno
app.secret_key = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT')) 
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

from flask import request, render_template
from flask_mail import Message

@app.route('/email')
def enviar_correo():
    tipo = request.args.get('tipo')  # novedades, suscripcion, medicamento
    correo_destinatario = request.args.get('correo')
    if tipo == 'novedades':
        if not correo_destinatario:
            return "Falta el parámetro 'correo' para novedades.", 400

        html_content = render_template('correo_novedades.html')
        asunto = '¡Novedades de Meditime!'

    elif tipo == 'suscripcion':
        if not correo_destinatario:
            return "Falta el parámetro 'correo' para aviso de suscripción.", 400

        html_content = render_template('correo_suscripcion.html')
        asunto = '¡Gracias por suscribirte a Meditime!'

    elif tipo == 'recordatorio':
        nombre = request.args.get('nombre')
        hora = request.args.get('hora')
        user_email = correo_destinatario
        nombre_usuario = my_db.get_username_by_email(user_email)[0]
        print(nombre_usuario)
        
        # Validar que todos los campos requeridos estén presentes
        if not nombre:
            return jsonify({'error': 'El campo nombre es requerido'}), 400
        
        if not hora:
            return jsonify({'error': 'El campo hora es requerido'}), 400
        
        if not user_email:
            return jsonify({'error': 'El campo user_email es requerido'}), 400

        html_content = render_template(
            'correo_recordatorio.html',
            hora= hora,
            nombre_usuario=nombre_usuario,
            medicamento=nombre
        )
        asunto = 'Recordatorio de Medicación'
    else:
        return "Tipo de correo no válido. Usa 'novedades', 'suscripcion' o 'medicamento'.", 400
    
    # Enviar correo
    msg = Message(asunto,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[correo_destinatario])
    msg.html = html_content
    mail.send(msg)

    return 'Correo enviado correctamente.'



my_db = DataBaseManager()
my_db.create_tables()
@app.route('/')
def index():
    categorias = my_db.get_all_categorias()
    return render_template("index.html", categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate required fields
        if not email or not password:
            flash('Por favor, complete todos los campos.', 'error')
            return render_template("login.html")
        
        # Attempt to login the user
        user = my_db.login_user(email, password)
        
        # Check if user exists
        if user:
            # Store user ID in session
            session['user_id'] = user[0]  # First index of the returned row
            
            # Redirect to dashboard or home page
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            flash('Correo electrónico o contraseña incorrectos.', 'error')
            return render_template("login.html")
    
    # If something unexpected happens
    return render_template("login.html")

@app.route('/logout')
def logout():
    session['user_id'] = None
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        # Obtener datos del formulario usando request.form en lugar de request.args
        username = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        number = request.form.get('telefono')
        tipo = request.form.get('type')

        # Validaciones simples
        if not username or not email or not password:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for('register'))

        try:
            user = my_db.create_user(username, email, password, number, tipo)
            session['user_id'] = user[0]  # Guardamos el ID del usuario en sesión
            flash("Registro exitoso", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error al registrar: {str(e)}", "error")
            return redirect(url_for('register'))
        
@app.route('/dashboard')
def dashboard():
    user = session.get('user_id')
    userdata = my_db.get_usuario(user)
    print(userdata)
    return render_template('dashboard.html', userdata=userdata)


@app.route('/add_medication', methods=['POST'])
def add_medication():
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No ha iniciado sesión'})
    
    try:
        # Get form data
        paciente_id = session['user_id']
        nombre = request.form.get('nombre_medicamento')
        hora = request.form.get('hora')
        ciclo = request.form.get('ciclo')
        
        # Set dia based on ciclo
        if ciclo == 'semanal':
            dia = request.form.get('dia')
        elif ciclo == 'mensual':
            # For monthly, dia is the day of the month (1-31)
            dia = request.form.get('dia', '1')  # Default to 1st day if not specified
        else:
            # For daily or multiple times, dia is not relevant
            dia = '0'
        
        # Add medication to database
        result = my_db.add_medicamento_usuario(
            paciente_id=paciente_id,
            nombre=nombre,
            dia=dia,
            hora=hora,
            ciclo=ciclo
        )
        
        if result:
            return jsonify({'success': True, 'message': 'Medicamento añadido correctamente'})
        else:
            return jsonify({'success': False, 'message': 'Error al añadir el medicamento'})
            
    except Exception as e:
        print(f"Error al añadir medicamento: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/get_medication')
def get_medication():
    medicamentos_raw = my_db.get_medicamento_usuario(session['user_id'])
    
    # Transform each medication entry to a dictionary with named keys
    medicamentos = []
    for med in medicamentos_raw:
        medicamento_dict = {
            "id": med[0],
            "user_id": med[1],
            "nombre": med[2],
            "dosis": med[3],
            "hora": med[4],
            "frecuencia": med[5]
        }
        medicamentos.append(medicamento_dict)
    
    return jsonify(medicamentos)

@app.route('/condiciones')
def condiciones():
    return render_template('condiciones.html')

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def devtools_json():
    return ('', 200)

@app.route('/add_recordatorio', methods=['POST'])
def add_recordatorio():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    dia = data.get('dia')
    hora = data.get('hora')
    nombre = data.get('nombre')
    user_email = data.get('user_email')

    my_db.add_recordatorio(paciente_id=paciente_id,dia=dia, hora=hora, nombre=nombre, user_email=user_email)
    return {'status': 'Ok'}

@app.route('/get_recordatorios', methods=['POST'])
def get_recordatios():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    recordatorios = my_db.get_recordatorio_by_id(paciente_id)
    return recordatorios

@app.route('/medicamentos', methods=['GET'])
def medicamentos():
    if request.args:
        name = request.args.get('name')
        categoria = request.args.get('categoria')
        if name:
            medicamentos = my_db.get_medicamento_by_name(name)
        if categoria:
            medicamentos = my_db.get_medicamento_by_categoria(categoria)
    else:
        medicamentos = my_db.get_all_medicamentos()
    return render_template('medicamentos.html', medicamentos=medicamentos)
pass
if __name__ == '__main__':
    app.run(debug=True, port=1010, )
