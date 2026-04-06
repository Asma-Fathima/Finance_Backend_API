from flask import Flask
from models import db
import config

from routes.user_routes import user_routes
from routes.finance_routes import finance_routes


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

app.register_blueprint(user_routes)
app.register_blueprint(finance_routes)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
