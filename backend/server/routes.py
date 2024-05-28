from flask import render_template, url_for, flash, redirect, request
from server import app, db, bcrypt
from server.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
             Transaction_DepositForm, ResetPasswordForm, BotForm)
from server.models import User, Transaction, Binance_Info, Bot
from flask_login import login_user, current_user, logout_user, login_required
import server.trading_bots as trading_bots

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/user")
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    bots = Bot.query.order_by(Bot.id.asc()).paginate(page=page, per_page=5)
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.id.asc()).paginate(page=page, per_page=5)
    return render_template('user.html', bots=bots, transactions=transactions)

@app.route("/purchase")
@login_required
def purchase():
    page = request.args.get('page', 1, type=int)
    bots = Bot.query.order_by(Bot.id.asc()).paginate(page=page, per_page=5)
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.id.asc()).paginate(page=page, per_page=5)
    return render_template('purchase.html', bots=bots, transactions=transactions)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        binance_info = Binance_Info(user_id=user.id)
        db.session.add(binance_info)
        db.session.commit()
        flash('Your account has been created successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        user = Binance_Info.query.filter_by(user_id=current_user.id).first()
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        user = Binance_Info.query.filter_by(user_id=current_user.id).first()
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
    return render_template('account.html', title='Account', form=form)

@app.route("/transactions/deposit", methods=['GET', 'POST'])
@login_required
def transaction_deposit():
    form = Transaction_DepositForm()
    if form.validate_on_submit():
        current_user.balance += form.amount.data
        db.session.commit()
        flash('Deposit Successfull.', 'success')
        return redirect(url_for('user'))
    return render_template('transaction_deposit.html', form=form)

@app.route("/transactions")
@app.route("/transactions/")
def transaction():
    return redirect(url_for('home'))

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

class give_keys():
    def get_key():
        user = Binance_Info.query.filter_by(user_id=current_user.id).first()
        return user.api_key, user.api_secret

@app.route("/bot1", methods=['GET', 'POST'])
@login_required
def bot1():
    #main.presentation_bot("apikey","apisecret","BTC",300)
    bot_id = 1
    temp = 0
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    for transaction in transactions:
        if transaction.bot_id == bot_id:
            temp = 1
    if temp == 0:
        return redirect(url_for('purchase'))
    form = BotForm()
    user = Binance_Info.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('bot1'))
    elif request.method == 'GET':
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
        form.bot_id.data = bot_id
        trading_bots.presentation_bot(user.api_key,user.api_secret,"ETH",200)
    return render_template('bot1.html', title='Account', form=form)

@app.route("/bot2", methods=['GET', 'POST'])
@login_required
def bot2():
    bot_id = 2
    temp = 0
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    for transaction in transactions:
        if transaction.bot_id == bot_id:
            temp = 1
    if temp == 0:
        return redirect(url_for('purchase'))
    form = BotForm()
    user = Binance_Info.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('bot2'))
    elif request.method == 'GET':
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
        form.bot_id.data = bot_id
        trading_bots.rsi_bot(user.api_key,user.api_secret,200)
    return render_template('bot2.html', title='Account', form=form)

@app.route("/bot3", methods=['GET', 'POST'])
@login_required
def bot3():
    bot_id = 3
    temp = 0
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    for transaction in transactions:
        if transaction.bot_id == bot_id:
            temp = 1
    if temp == 0:
        return redirect(url_for('purchase'))
    form = BotForm()
    user = Binance_Info.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('bot3'))
    elif request.method == 'GET':
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
        form.bot_id.data = bot_id
        trading_bots.macd_bot(user.api_key,user.api_secret,200)
    return render_template('bot3.html', title='Account', form=form)

@app.route("/bot4", methods=['GET', 'POST'])
@login_required
def bot4():
    bot_id = 4
    temp = 0
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    for transaction in transactions:
        if transaction.bot_id == bot_id:
            temp = 1
    if temp == 0:
        return redirect(url_for('purchase'))
    form = BotForm()
    user = Binance_Info.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('bot4'))
    elif request.method == 'GET':
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
        form.bot_id.data = bot_id
        trading_bots.ema_bot(user.api_key,user.api_secret,200)
    return render_template('bot4.html', title='Account', form=form)

@app.route("/bot5", methods=['GET', 'POST'])
@login_required
def bot5():
    bot_id = 5
    temp = 0
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    for transaction in transactions:
        if transaction.bot_id == bot_id:
            temp = 1
    if temp == 0:
        return redirect(url_for('purchase'))
    form = BotForm()
    user = Binance_Info.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        user.api_key = form.api_key.data
        user.api_secret = form.api_secret.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('bot5'))
    elif request.method == 'GET':
        form.api_key.data = user.api_key
        form.api_secret.data = user.api_secret
        form.bot_id.data = bot_id
        trading_bots.bollinger_bands_bot(user.api_key,user.api_secret,200)
    return render_template('bot5.html', title='Account', form=form)

@app.route("/purchase_bot1", methods=['GET', 'POST'])
@login_required
def purchase_bot1():
    user = User.query.filter_by(id=current_user.id).first()
    bot = Bot.query.filter_by(id=1).first()
    if user.balance < bot.price:
        flash('Not Enough Balance.', 'danger')
        return redirect(url_for('transaction_deposit'))
    else:
        transaction = Transaction(user_id=current_user.id, bot_id=bot.id, price=bot.price)
        db.session.add(transaction)
        user.balance -= bot.price
        db.session.commit()
        flash('Purchase Successful.', 'success')
        return redirect(url_for('purchase'))

@app.route("/purchase_bot2", methods=['GET', 'POST'])
@login_required
def purchase_bot2():
    user = User.query.filter_by(id=current_user.id).first()
    bot = Bot.query.filter_by(id=2).first()
    if user.balance < bot.price:
        flash('Not Enough Balance.', 'danger')
        return redirect(url_for('transaction_deposit'))
    else:
        transaction = Transaction(user_id=current_user.id, bot_id=bot.id, price=bot.price)
        db.session.add(transaction)
        user.balance -= bot.price
        db.session.commit()
        flash('Purchase Successful.', 'success')
        return redirect(url_for('purchase'))

@app.route("/purchase_bot3", methods=['GET', 'POST'])
@login_required
def purchase_bot3():
    user = User.query.filter_by(id=current_user.id).first()
    bot = Bot.query.filter_by(id=3).first()
    if user.balance < bot.price:
        flash('Not Enough Balance.', 'danger')
        return redirect(url_for('transaction_deposit'))
    else:
        transaction = Transaction(user_id=current_user.id, bot_id=bot.id, price=bot.price)
        db.session.add(transaction)
        user.balance -= bot.price
        db.session.commit()
        flash('Purchase Successful.', 'success')
        return redirect(url_for('purchase'))

@app.route("/purchase_bot4", methods=['GET', 'POST'])
@login_required
def purchase_bot4():
    user = User.query.filter_by(id=current_user.id).first()
    bot = Bot.query.filter_by(id=4).first()
    if user.balance < bot.price:
        flash('Not Enough Balance.', 'danger')
        return redirect(url_for('transaction_deposit'))
    else:
        transaction = Transaction(user_id=current_user.id, bot_id=bot.id, price=bot.price)
        db.session.add(transaction)
        user.balance -= bot.price
        db.session.commit()
        flash('Purchase Successful.', 'success')
        return redirect(url_for('purchase'))

@app.route("/purchase_bot5", methods=['GET', 'POST'])
@login_required
def purchase_bot5():
    user = User.query.filter_by(id=current_user.id).first()
    bot = Bot.query.filter_by(id=5).first()
    if user.balance < bot.price:
        flash('Not Enough Balance.', 'danger')
        return redirect(url_for('transaction_deposit'))
    else:
        transaction = Transaction(user_id=current_user.id, bot_id=bot.id, price=bot.price)
        db.session.add(transaction)
        user.balance -= bot.price
        db.session.commit()
        flash('Purchase Successful.', 'success')
        return redirect(url_for('purchase'))
