from flask import Flask, render_template, session, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'o9rew908qre3qr3$TEw3qejrewqopreREWQr'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Question(db.Model):
	__tablename__ = 'questions'
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String, nullable=False)
	answer = db.Column(db.String(20))
	

class Answers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	a = db.Column(db.String(20), nullable=False)
	b = db.Column(db.String(20), nullable=False)
	c = db.Column(db.String(20), nullable=False)
	d = db.Column(db.String(20), nullable=False)
	q_id = db.Column(db.Integer, db.ForeignKey('questions.id'))


@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		username = request.form.get('namefield', '')
		if username:
			session['username'] = username
			session['current'] = 1
			return redirect(url_for('questions'))

	username = session.get('username')
	if username:
		return redirect(url_for('questions'))
	return render_template('home.html')

@app.route('/quiz', methods=["GET", "POST"])
def questions():
	id = session.get('current')
	qs = Question.query.get(id)
	ans = Answers.query.get(id)

	score  = session.get('score', 'non')
	failed = session.get('failed', 'non')
	if not (failed and score) != 'non':
		session['score'] = 0
		
		session['failed'] = 0
		

	if request.method == 'POST':
		answer = request.form.get('a')
		if answer == qs.answer:
			score += 1
			session['score'] = score
		else:
			failed += 1
			session['failed'] = failed

		id += 1
		qs = Question.query.get(id)
		ans = Answers.query.get(id)
		session['current'] = id

		if not (qs and ans):
			return redirect(url_for('dashboard'))
			
	return render_template('quiz.html', qs=qs,ans=ans,username=session.get('username'))

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
	
	if request.method == 'POST':
		quest = request.form.get('quit')
		
		if not quest:
			session['current'] = 1
			return redirect(url_for('questions'))
		else:
			session.pop('username')
			return redirect(url_for('index'))
	
	session['current'] = 1
	username = session.get('username')
	score = session.get("score")
	failed = session.get("failed")
	
	try:
		session.pop('score')
		session.pop('failed')
	except:

		return redirect(url_for('questions'))

	if not username:

		return redirect(url_for('index'))

	return render_template('dashboard.html', score=score, failed=failed)