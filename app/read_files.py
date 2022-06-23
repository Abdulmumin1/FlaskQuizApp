import json
import sqlite3


def add_questions():
    i = None
    while True:
        # diction = {}

        # json_file = json.load(open('questions.json', 'r'))
        # for key in json_file.keys():
        #     diction[key] = json_file[key]
        # i = int(key)
        # i += 1

        question = input('Enter question: ').capitalize()
        answer = input('Enter answer: ').title()
        options = map(lambda x: x.title(),
                      input('Enter option: ').split(','))
        options = list(options)
        options.append(answer)

        if len(options) < 4:
            dif = 4 - len(options)
            for i in range(dif):
                options.append(' ')

        # diction[i] = {'question': question,
        #               'answer': answer, 'options': options}

        insert_data(question, answer, options)

        # json_file = json.dump(diction, open('questions.json', 'w'))


def insert_data(question, answer, options):
    db = sqlite3.connect('questions.db')
    cur = db.cursor()

    statement = "insert into questions (question, answer) values(?,?)"
    cur.execute(statement, (question, answer))

    select = "select id from questions where question = ?"
    question_id = [i[0] for i in cur.execute(select, (question,))]
    question_id = question_id[0]

    statement2 = "insert into answers (a,b,c,d,q_id) values(?,?,?,?,?)"
    cur.execute(statement2, (*options, question_id))
    db.commit()
    db.close()


def register_questions():
    datas = json.load(open('new.json'))
    for question in datas.values():
        q = question['question']
        ans = question['answer']
        option = question['options']
        # print(len(option))

        insert_data(q, ans, option)

add_questions()
