from flask import Flask, render_template
from flask import request

from view import index

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tipo = request.form['tipo']
        if tipo:
            response = index(tipo=tipo)
            return render_template('index.html',
                                   resp=response,
                                   has_tipo=True)
        else:
            return render_template('index.html',
                                   resp={},
                                   has_tipo=False)
    else:
        return render_template('index.html',
                               resp={},
                               has_tipo=False)


if __name__ == '__main__':
    app.run(debug=False)
