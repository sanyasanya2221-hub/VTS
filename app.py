from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    hire_date = db.Column(db.Date)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    
    employee = db.relationship('Employee', backref='attendances')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'test' and password == 'test':
        return redirect(url_for('dashboard'))
    else:
        flash('Логин или пароль введен неверно')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    employees = Employee.query.all()
    attendances = Attendance.query.order_by(Attendance.date.desc(), Attendance.check_in.desc()).all()
    return render_template('dashboard.html', employees=employees, attendances=attendances)

@app.route('/check_in', methods=['POST'])
def check_in():
    try:
        emp_id = request.form['employee_id']
        today = datetime.now().date()
        
        existing = Attendance.query.filter_by(
            employee_id=emp_id, 
            date=today,
            check_out=None
        ).first()
        
        if not existing:
            new_att = Attendance(
                employee_id=emp_id, 
                date=today, 
                check_in=datetime.now()
            )
            db.session.add(new_att)
            db.session.commit()
            flash(f'Приход отмечен для сотрудника ID {emp_id}')
        else:
            flash('Сотрудник уже отметил приход сегодня')
            
    except Exception as e:
        flash(f'Ошибка: {str(e)}')
        
    return redirect(url_for('dashboard'))

@app.route('/check_out', methods=['POST'])
def check_out():
    try:
        emp_id = request.form['employee_id']
        today = datetime.now().date()
        
        att = Attendance.query.filter_by(
            employee_id=emp_id, 
            date=today,
            check_out=None
        ).first()
        
        if att:
            att.check_out = datetime.now()
            db.session.commit()
            flash(f'Уход отмечен для сотрудника ID {emp_id}')
        else:
            flash('Не найдена активная отметка о приходе')
            
    except Exception as e:
        flash(f'Ошибка: {str(e)}')
        
    return redirect(url_for('dashboard'))

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        
        if name:
            new_emp = Employee(
                name=name, 
                position=position if position else 'Сотрудник',
                hire_date=datetime.now().date()
            )
            db.session.add(new_emp)
            db.session.commit()
            flash(f'Сотрудник "{name}" успешно добавлен')
            return redirect(url_for('dashboard'))
        else:
            flash('Введите ФИО сотрудника')
            
    return render_template('add_employee.html')

@app.route('/init_db')
def init_db():
    """Инициализация базы данных"""
    with app.app_context():
        db.create_all()
        flash('База данных инициализирована')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if Employee.query.count() == 0:
            test_emp1 = Employee(name="Иванов Иван Иванович", position="Менеджер", hire_date=datetime.now().date())
            test_emp2 = Employee(name="Петрова Анна Сергеевна", position="Разработчик", hire_date=datetime.now().date())
            db.session.add(test_emp1)
            db.session.add(test_emp2)
            db.session.commit()
            print("Добавлены тестовые сотрудники")
    
    app.run(host='0.0.0.0', port=5000, debug=True)