from flask import Flask
from routes import translation_routes

app = Flask(__name__)
app.register_blueprint(translation_routes)

if __name__ == "__main__":
    app.run(debug=True)
