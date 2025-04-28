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

