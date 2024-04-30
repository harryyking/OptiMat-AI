from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

# declaring the base 
class Base(DeclarativeBase):
    pass

# defining database to base
db = SQLAlchemy(model_class= Base)

# declaration of tables and models 
# user table, password and email set
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key= True)
    email: Mapped[str] = mapped_column(unique=True, nullable= False)
    password_hash : Mapped[str] = mapped_column(unique= True, nullable= False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    