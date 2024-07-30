import logging
from flask import Flask, flash, render_template, request, abort, redirect, url_for
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename
from markupsafe import escape
import secrets
secrets.token_hex()



app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


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
                if number_2 == '0':
                    return "нельзя делить на ноль"
                return str(int(number_1) / int(number_2))
    
    context = {'task': 'задание_5'}

    return render_template('calculator.html', **context)

@app.route('/check_age', methods=['GET', 'POST'])
def check_age():
    MIN_AGE = 18
    age = '0'
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        if int(age) > MIN_AGE:
            return f'Вы вошли под именем {name}'
        else:
            abort(403)

            
    context = {'task': 'задание_5'}

    return render_template('check_age.html', **context)

@app.errorhandler(403)
def page_not_found(e):
    logger.warning(e)
    context = {
        'title': 'Доступ запрещён', 'url': request.base_url,
        }
    return render_template('403.html', **context), 403

@app.route('/quadro', methods=['GET', 'POST'])
def quadro():
    NUMBER = 5
    return redirect(url_for('quadro_result', number=int(NUMBER**2)))

@app.route('/quadro/<int:number>')
def quadro_result(number):
    return f'Квадрат числа = {number}'

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Проверка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
            # Обработка данных формы
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
