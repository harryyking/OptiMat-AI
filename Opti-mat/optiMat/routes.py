from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, flash
)
from flask_login import login_user, logout_user, login_required
from werkzeug.exceptions import abort
from .assistant import AssistantManager
import json
from optiMat.authentication import SignupForm, LoginForm
from optiMat.model import db, User 

bp = Blueprint('routes', __name__)

#route for Homepage
@bp.route('/')
@bp.route('/home')
def index():
    return render_template('index.html')


#Route for signup
@bp.route('/signup', methods= ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already registered', 'Error')
        else:
            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)  # Hash password before saving
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('routes.form'))
    return render_template('signup.html', form=form)

# route for login
@bp.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data): # validate password 
            login_user(user)
            flash('You have succesffully logged in!', 'Success')
            return redirect(url_for('routes.form'))
    return render_template('login.html', form=form)

# route for logout 
@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('routes.index'))


#route for form page 
@bp.route('/form', methods=('GET', 'POST'))
def form():
    return render_template('form.html')

# route for response page 
@bp.route('/response', methods =('GET', 'POST'))
def process():
    if request.method == 'GET':
        print('not allowed')
        return 'method not allowed'
    about: str = request.form.get('about')
    function: str = request.form.get('function')
    cost_constraint: str = request.form.get('cost_constraint')
    
    content = {
        "about": about,
        "function": function,
        "cost_constraint": cost_constraint,
    }

    content = str(content)
    meta_data = 'Recommend only one material and please leave your answer in the following json format.  { title: string (e.g Optimal material for fingerprint replacement), material: string (e.g. Acrylic), reason: string (e.g acrylic is highly biocamptible and as tough as fingerprints), key_properties: array of string(not more than 5) }'
    
    api_prompt = content + '\n' + meta_data
    
    manager = AssistantManager()
    manager.create_assistant()
    manager.create_thread()
    manager.add_message_to_thread(role='user', content=api_prompt)
    manager.run_assistant()
    response = manager.wait_for_completion()
    response = json.loads(response)
    
    keys = list(response.keys())
    isPresent = (('material' in keys) and ('title' in keys) and ('reason' in keys) and ('key_properties' in keys))
    print(isPresent)
    
    if len(keys) == 1:
        response = response[keys[0]]
    
    if isPresent:
        print('in here')
        return render_template('response.html', title = response['title'], material=response['material'], reason=response['reason'], key_properties = response['key_properties'])
        

    return render_template('response.html', title='hello', material='helloo', reason='hellooo', key_properties=['helloooooo']) # render_template('error.html')

