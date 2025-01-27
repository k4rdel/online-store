import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    # Pobierz port z zmiennej środowiskowej lub ustaw domyślny na 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
