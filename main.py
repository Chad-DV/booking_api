from app.views import app
from app.models import db
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig

app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
