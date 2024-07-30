from flask import Flask, render_template, request
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/next')
def next_page():
    return "Привет, Вася!"

@app.route('/load_image', methods=['GET', 'POST'])
def load_image():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'Lesson_2/uploads', file_name))
        return f"Файл {file_name} загружен на сервер"
    
    context = {'task': 'задание_2'}

    return render_template('page_1.html', **context)

@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    login = {
        'auth_email': '1@mail.ru',
        'auth_pass': '123'
    }
    if request.method == 'POST':
        auth_email = request.form.get('auth_email')
        auth_pass = request.form.get('auth_pass')
        if auth_email == login['auth_email'] and auth_pass == login['auth_pass']:
            return f"Вход с почты: {escape(auth_email)} выполнен"
        else:
            return 'Ошибка'
    
    context = {'task': 'задание_3'}

    return render_template('authorization.html', **context)
    
@app.route('/counter', methods=['GET', 'POST'])
def counter():
    if request.method == 'POST':
        text = request.form.get('text')
        return f"Количество слов: {len(text.split())}"
    
    context = {'task': 'задание_4'}

    return render_template('counter.html', **context)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        number_1 = request.form.get('number_1')
        number_2 = request.form.get('number_2')
        operation = request.form.get('operation')

        match operation:
            case 'add':
                return str(int(number_1) + int(number_2))
            case 'subtract':
                return str(int(number_1) - int(number_2))
            case 'multiply':
                return str(int(number_1) * int(number_2))
            case 'divide':
                return str(int(number_1) / int(number_2))
    
    context = {'task': 'задание_5'}

    return render_template('calculator.html', **context)


if __name__ == '__main__':
    app.run()
