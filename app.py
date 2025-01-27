import os
from flask import Flask, render_template
from forms import RegistrationForm

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Zapisz dane do bazy danych
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

def home():
    return render_template('index.html')

if __name__ == "__main__":
    # Pobierz port z zmiennej środowiskowej lub ustaw domyślny na 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
