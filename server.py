from flask_app import app
from flask_app.controller import user,recipe



if __name__ == "__main__":
    app.run(debug=True,port=5000)