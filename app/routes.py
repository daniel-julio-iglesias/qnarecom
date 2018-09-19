#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Views
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, QAForm
from app.bayesTextClassifyTemplateDI import BayesText
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
import os
from config import basedir


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Daniel'}
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/questionanswer', methods=['GET', 'POST'])
@login_required
def questionanswer():
    form = QAForm()
    if form.validate_on_submit():

        # Calling Recommendation Engine
        # training_dir = "./app/static/app/app-kb/app-kb-train/"
        training_dir = os.path.join(basedir, 'app/static/app/app-kb/app-kb-train/')
        # stop_list_file = "./app/static/app/app-kb/stopwords174.txt"
        stop_list_file = os.path.join(basedir, 'app/static/app/app-kb/stopwords174.txt')
        bt = BayesText(training_dir, stop_list_file)

        question = form.question.data
        category = bt.classify_text(question)
        form.category.data = category
        content = bt.read_file_content(training_dir, category)
        form.answer.data = content

        # flash('Answer for  question {}, category={}, answer={}'.format(
        #     form.question.data, form.category.data, form.answer.data))
        # return redirect(url_for('index'))
        return render_template('questionanswer.html', title='Question and Answer', form=form)
    return render_template('questionanswer.html', title='Question and Answer', form=form)
