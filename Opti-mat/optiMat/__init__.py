from flask import Flask 
from optiMat.model import db
from flask_login import LoginManager
from flask_login import login_manager


login_manager = LoginManager()

# create OPTIMAT app
app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = 'material_selection_assistant77234'

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

    

# initialize the database to the app 
db.init_app(app)

# with app in context, create database 
with app.app_context():
    db.create_all()


# initialize logging in 
login_manager.init_app(app) 


@login_manager.user_loader
def load_user(user_id):
    from optiMat.model import User 
    return db.session.execute(db.select(User).filter_by(id=1)).scalar() #Load user from the database 

from . import routes
app.register_blueprint(routes.bp)
   
if __name__ == "__main__":
    app.run(debug=True)
    
        