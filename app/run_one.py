from flask import Flask
from routes import translation_routes  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(translation_routes, url_prefix="/api/v1")

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
