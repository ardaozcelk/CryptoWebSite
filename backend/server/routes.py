from flask import render_template, url_for, flash, redirect, request
from server import app, db, bcrypt
from server.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
             Transaction_DepositForm, ResetPasswordForm, BotForm)
from server.models import User, Transaction, Binance_Info, Bot
from flask_login import login_user, current_user, logout_user, login_required
import server.trading_bots as trading_bots

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