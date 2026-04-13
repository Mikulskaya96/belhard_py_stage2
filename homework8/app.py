from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, static_folder='../homework4/static')

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- МОДЕЛИ (Models) ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    user = db.relationship('User', backref='results')
    quiz = db.relationship('Quiz', backref='results')

# --- МАРШРУТЫ (Routes) ---

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# User CRUD Routes
@app.route('/users/')
def users():
    all_users = User.query.all()
    return render_template('users/list.html', users=all_users)

@app.route('/user/create/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('users/create.html')

@app.route('/user/<int:id>/update/', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('users/update.html', user=user)

@app.route('/user/<int:id>/delete/', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

# Quiz CRUD Routes
@app.route('/quizzes/')
def quizzes():
    all_quizzes = Quiz.query.all()
    return render_template('quizzes/list.html', quizzes=all_quizzes)

@app.route('/quiz/add/', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        title = request.form['title']
        db.session.add(Quiz(title=title))
        db.session.commit()
        return redirect(url_for('quizzes'))
    return render_template('quizzes/add.html')

@app.route('/quiz/edit/<int:id>/', methods=['GET', 'POST'])
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        quiz.title = request.form['title']
        db.session.commit()
        return redirect(url_for('quizzes'))
    return render_template('quizzes/edit.html', quiz=quiz)

@app.route('/quiz/delete/<int:id>/')
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('quizzes'))

# Question CRUD Routes
@app.route('/questions/')
def questions():
    all_questions = Question.query.all()
    return render_template('questions/list.html', questions=all_questions)

@app.route('/question/add/', methods=['GET', 'POST'])
def add_question():
    quizzes_list = Quiz.query.all()
    if request.method == 'POST':
        text = request.form['text']
        answer = request.form['answer']
        quiz_id = request.form['quiz_id']
        new_question = Question(text=text, answer=answer, quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('questions'))
    return render_template('questions/add.html', quizzes=quizzes_list)

@app.route('/question/edit/<int:id>/', methods=['GET', 'POST'])
def edit_question(id):
    question = Question.query.get_or_404(id)
    quizzes_list = Quiz.query.all()
    if request.method == 'POST':
        question.text = request.form['text']
        question.quiz_id = request.form['quiz_id']
        db.session.commit()
        return redirect(url_for('questions'))
    return render_template('questions/edit.html', question=question, quizzes=quizzes_list)

@app.route('/question/delete/<int:id>/')
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('questions'))

# Игра
@app.route('/quiz/<int:quiz_id>/play/')
def play_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions_list = Question.query.filter_by(quiz_id=quiz_id).all()
    all_users = User.query.all()
    return render_template(
        'quizzes/play.html',
        quiz=quiz,
        questions=questions_list,
        users=all_users,
    )

# Финиш
@app.route('/save_result/', methods=['POST'])
def save_result():
    user_id = request.form.get('user_id')
    quiz_id = request.form.get('quiz_id')
    score = request.form.get('score')

    if user_id and quiz_id:
        new_result = Result(user_id=user_id, quiz_id=quiz_id, score=score)
        db.session.add(new_result)
        db.session.commit()

    return redirect(url_for('leaderboard'))

@app.route('/leaderboard/')
def leaderboard():
    results = Result.query.order_by(Result.score.desc()).all()
    return render_template('leaderboard.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
    
    # тестовый комментарий 