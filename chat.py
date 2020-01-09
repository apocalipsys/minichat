from flask import Flask, render_template, redirect, session, url_for
from flask_socketio import SocketIO, send
from foms import Nombre

app = Flask(__name__)
app.config['SECRET_KEY'] ='secret'
socketio = SocketIO(app=app, manage_session = True )

@app.route('/', methods=['GET','POST'])
def index():
    form = Nombre()
    session['nombre'] = form.nombre.data
    if form.validate_on_submit():
        return redirect(url_for('.chat', user = session['nombre'] + ' dice:'))
    return render_template('index.html', form = form)

@app.route('/chat/<string:user>', methods=['GET','POST'])
def chat(user):
    return render_template('chat.html', user = user)
'''
@socketio.on('user')
def handleUser(usr):
    print('Usuario ' + usr)
    send(usr, broadcast = True)
'''
@socketio.on('message')
def handleMessage(msg):
    print(msg)
    send(msg, broadcast = True)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5058)

