from flask import Flask, request, make_response, render_template, session, redirect, url_for


app = Flask(__name__)
app.secret_key ='5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/user')
def index():
    if 'username' in session and 'user_email' in session:
        response = make_response("Cookie установлен")
        response.set_cookie('username', 'user_email')
        return render_template('user.html', name=session["username"])
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        session['user_email'] = request.form.get('user_email') or 'NoImail'
        return redirect(url_for('index'))
    return render_template('username_form.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()