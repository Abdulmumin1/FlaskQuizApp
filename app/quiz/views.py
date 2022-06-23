from . import main
from flask import session, redirect, url_for, request, render_template
import json
from app.models import Question, Answers


@main.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get('namefield', '')
        if username:
            session['username'] = username
            data = {'id': 1, 'scored': 0, 'failed': 0}
            data = json.dumps(data)
            session['current'] = data
            return redirect(url_for('main.questions'))

    username = session.get('username')
    if username:
        return redirect(url_for('main.questions'))
    return render_template('home.html')


@main.route('/quiz', methods=["GET", "POST"])
def questions():
    data = session.get('current')
    data = json.loads(data)
    id_ = data['id']
    qs = Question.query.get(id_)
    ans = Answers.query.get(id_)

    score = data['scored']
    failed = data['failed']

    if request.method == 'POST':
        answer = request.form.get('a')
        if answer == qs.answer:
            score += 1

        else:
            failed += 1

        id_ += 1
        qs = Question.query.get(id_)
        ans = Answers.query.get(id_)

        data = {'id': id_, 'scored': score, 'failed': failed}
        session['current'] = json.dumps(data)

        if not (qs and ans):
            return redirect(url_for('main.dashboard'))
    ans = [ans.a, ans.b, ans.c, ans.d]

    return render_template('quiz.html', qs=qs, ans=ans, username=session.get('username'))


@main.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    data = session.get('current')
    #data = json.loads(data)
    session['current'] = json.dumps({'id': 1, 'scored': 0, 'failed': 0})

    if request.method == 'POST':
        quest = request.form.get('quit')

        if not quest:
            return redirect(url_for('main.questions'))
        else:
            session.pop('username')
            return redirect(url_for('main.index'))
    data = json.loads(data)
    username = session.get('username')

    score = data['scored']
    failed = data['failed']

    if not username:

        return redirect(url_for('main.index'))

    return render_template('dashboard.html', score=score, failed=failed)
