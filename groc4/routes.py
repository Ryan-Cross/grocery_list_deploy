from groc4 import app, db, mail
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, redirect, url_for, request, flash
from groc4.forms import LoginForm, RegistrationForm, ListItem, AmendField
from groc4.models import User, Grocery, GrocList
from datetime import datetime
from flask_mail import Message
from sqlalchemy import func


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/fliers')
def fliers():
    return render_template('fliers.html', icon="static/sals.jpg", title="Check the fliers!")


@app.route('/info')
def info():
    return render_template('info.html', title="About this project")


@app.route('/code')
def code():
    return render_template('code.html')


@app.route('/list_check_auth')
def list_check_auth():
    if current_user.is_authenticated:
        return redirect(url_for('bumplist'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bumplist'))
    form = LoginForm()
    if form.validate_on_submit():
        dredge = User.query.filter_by(username=form.username.data).first()
        if dredge is None or not dredge.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(dredge)
        return redirect(url_for('bumplist'))
    return render_template("login.html", form=form, title='Login')


@app.route('/home/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        dredge = User.query.filter_by(username=form.username.data).first()
        login_user(dredge)
        return redirect(url_for('bumplist'))

    return render_template('register.html', form=form, title='Register')


@app.route('/bumplist', methods=['GET', 'POST'])
def bumplist():
    new_list = GrocList(user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('list'))


@app.route('/list', methods=['GET', 'POST'])
def list():
    form = ListItem()
    list_count = db.session.query(GrocList).count()
    # dafuq = "dafuq={}".format(db.session.query(Grocery).filter(Grocery.list_id==list_count).all())
    display = []
    count = 1
    items_current = db.session.query(Grocery).filter(Grocery.list_id == list_count).all()
    for item in items_current:
        display.append({count: (item.item, item.amount)})
        count += 1
    if form.validate_on_submit():
        # how many lists total? last number == count of lists and is current list.use for list id.
        groc = Grocery(list_id=list_count, item=form.item.data, amount=form.amount.data, timestamp=datetime.utcnow())
        db.session.add(groc)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('list.html', form=form, title="{}'s list'".format(current_user.username),present_user=current_user.username, display=display)


@app.route('/amend', methods=['GET', 'POST'])
def amend():
    form = AmendField()
    display = []
    count = 1
    list_count = db.session.query(GrocList).count()
    items_current = db.session.query(Grocery).filter(Grocery.list_id == list_count).all()
    for item in items_current:
        display.append({count: (item.item, item.amount)})
        count += 1
    if form.validate_on_submit():
        if len(display) == 0:
            return redirect(url_for('list'))
        if len(display)>count:
            return redirect(url_for('list'))
        # form.list_item.data is the entry number they want gone
        redacted = (display[form.list_item.data - 1])[form.list_item.data][0]
        edit = db.session.query(Grocery).filter(Grocery.list_id == list_count).filter(Grocery.item == redacted).first()
        db.session.delete(edit)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('amend.html', form=form, display=display, title='Alter your list')


@app.route('/finish')
def finish():
    display = []
    count = 1
    list_count = db.session.query(GrocList).count()
    items_current = db.session.query(Grocery).filter(Grocery.list_id == list_count).all()
    for item in items_current:
        display.append({count: (item.item, item.amount)})
        count += 1
    msg = Message('Your grocery list!', [current_user.email])
    msg2 = Message('new list by user {}'.format(current_user.email), ['smallblackchironomid@gmail.com'])
    msg.body = 'Here is your grocery list:\n\n'
    for thing in display:
        for toop in thing.values():
            msg.body += toop[0]
            msg.body += " x {}".format(str(toop[1]))
            msg.body += '\n'
    msg.body += "\n{}, thanks for using the GroceryList webapp!".format(current_user.username)
    mail.send(msg)
    mail.send(msg2)
    return render_template('finish.html', display=display,  title='Finished up')









