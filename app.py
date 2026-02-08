from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'qadasi_secret_key'

# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mathoito.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    id_number = db.Column(db.String(20), unique=True)
    cell_no = db.Column(db.String(15))
    country = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10))

# Initialize Database
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            hashed_pw = generate_password_hash(request.form['password'])
            new_user = User(
                name=request.form.get('name'),
                surname=request.form.get('surname'),
                id_number=request.form.get('id_number'),
                cell_no=request.form.get('cell_no'),
                country=request.form.get('country'),
                email=request.form.get('email'),
                password=hashed_pw,
                gender=request.form.get('gender')
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Error: {e}. Ensure Email/ID is unique."
            
    return render_template('si.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        
        return "Login Failed. Invalid credentials."
    
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
