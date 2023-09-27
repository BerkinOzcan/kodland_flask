# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os
import logging
import requests
import json
import time
import random


# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from jinja2 import TemplateNotFound

# App modules
from app import app, lm, db, bc
from app.models import Users
from app.forms import LoginForm, RegisterForm, CityForm, QuizForm
CITY = "ankara"
URL_MY = "http://api.weatherapi.com/v1/forecast.json?key=e5f57591945a43e88ed104908232609&q=" + \
    CITY + "&days=3&aqi=no&alerts=no"
qnumber=0

def ep_to_day(ep):
    day = time.strftime('%A', time.localtime(ep))
    return day

# provide login manager with load_user callback


@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Logout user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user


@app.route('/register', methods=['GET', 'POST'])
def register():

    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None
    success = False

    if request.method == 'GET':

        return render_template('register.html', form=form, msg=msg)

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        nickname = request.form.get('nickname', '', type=str)

        # filter User out of database through username
        user = Users.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_nickname = Users.query.filter_by(nickname=nickname).first()

        if user or user_by_nickname:
            msg = 'Error: User exists!'

        else:

            pw_hash = bc.generate_password_hash(password)

            user = Users(username, nickname, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + \
                url_for('login') + '">login</a>'
            success = True

    else:
        msg = 'Input error'

    return render_template('register.html', form=form, msg=msg, success=success)

# Authenticate user


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        print(username + " BITCHHHHHHHHHHH")

        # filter User out of database through username
        user = Users.query.filter_by(user=username).first()

        if user:

            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template('login.html', form=form, msg=msg)

# App main route + generic routing


@app.route('/', defaults={'path': 'index'}, methods=['GET', 'POST'])
@app.route('/<path>', methods=['GET', 'POST'])
def index(path):
    datelist = list()
    mintemplist = list()
    maxtemplist = list()
    ##
    questiontextlist = list()
    optiontextlist = list()
    correctlist = list()
    correctsublist = list()
    optiontextsublist = list()
    city = ""

    # if not current_user.is_authenticated:
    #     return redirect(url_for('login'))
    form = CityForm(request.form)
    msg = None
    if form.validate_on_submit():
        city = request.form.get('city', '', type=str)
        print("im here bitch, city name is : ")
        print(city)
        global CITY
        CITY = city
        global URL_MY
        URL_MY = "http://api.weatherapi.com/v1/forecast.json?key=e5f57591945a43e88ed104908232609&q=" + \
            CITY + "&days=3&aqi=no&alerts=no"

        # datelist=""
        # mintemplist=""
        # maxtemplist=""
        response = requests.get(URL_MY)

        if response.status_code == 200:
            # retrieving data in the json format
            data = response.json()
            print(f"{CITY:-^35}")
    # take the main dict block
            forecast = data['forecast']
            forecastdays = forecast['forecastday']
            for fc in range(len(forecastdays)):
                fc_epoch = forecastdays[fc]['date_epoch']
                fc_date = forecastdays[fc]['date']
                fc_day = forecastdays[fc]['day']
                mintemp_c = fc_day['mintemp_c']
                maxtemp_c = fc_day['maxtemp_c']
                date_to_display = fc_date + "-" + ep_to_day(fc_epoch)
                dateinfo = "epoch date: " + \
                    str(fc_epoch) + ", " + "Full Date: " + date_to_display
                tempinfo = "minimum temperature: " + \
                    str(mintemp_c) + "\nmaximum temperature: " + str(maxtemp_c)

                datelist.append(date_to_display)
                mintemplist.append(mintemp_c)
                maxtemplist.append(maxtemp_c)
                print(dateinfo)
                print(tempinfo)
                print("-------------------------------------")
                print(datelist, mintemplist, maxtemplist)

        else:
            msg = "Geçerli bir şehir ismi gir napıyosun<br><small>üzgünüm :( türkçe karakterlerde sıkıntı yaşamış olabilirsin)</small"
            print(msg)

    else:
        msg = "Şehir ismi giriniz"
        print(msg)
    print("path is: " + path)
    print("--------------BITCHING IS DONE-----------------------")
    # print(datelist,mintemplist,maxtemplist)
    try:

        if (path == "quiz"):
            global qnumber
            
            print("qnumber at the beggining" + str(qnumber))
            
            # qnumber = random.randint(0, 4)
            fq = open("app/templates/questions.json")
            qdata = json.load(fq)
            print(qdata['questions'])
            print("----------------------------------------")

            for index, qs in enumerate(qdata['questions']):
                # optiontextsublist.clear()
                # correctsublist.clear()
                correctsublist = list()
                optiontextsublist = list()
                questext = qs['questiontext']
                print("QUESTION- " + str(index) + " TEXT:")
                print(questext)
                opts = qs['options']
                print("QUESTION- " + str(index) + " OPTION TEXTLERI:")

                for i, ops in enumerate(opts):
                    # print(opts[i])
                    optiontext = ops['optiontext']
                    correct = ops['correct']
                    print(optiontext + " : " + str(correct))
                    optiontextsublist.append(optiontext)
                    correctsublist.append(correct)
                    print("OPTION TEXT SUB LIST:")
                    print(optiontextsublist)
                    print(ops['correct'])

                questiontextlist.append(questext)
                optiontextlist.append(optiontextsublist)
                correctlist.append(correctsublist)
                print("appended em bitch!")
                print("FULL LISTS")
                print(questiontextlist)
                print("-------------------")
                print(optiontextlist)
                print("-------------------")
                print(correctlist)
                print("-------------------")

            questionform = QuizForm(request.form)
            print("MOMBO JOMBO BITTI \n ---------------- \n \n --------------------")
            # questionform.question.choices = [(g.)]
            print(questiontextlist)
            print("-------------------")
            print(optiontextlist)
            print("-------------------")
            print(correctlist)
            print("-------------------")
            #questionform.question.choices=[j, j.]
            #qnumber=random.randint(0,4)
            questionform.question.choices = [(index, optiontextlist[qnumber][index]) for index in range(len(optiontextlist[qnumber]))]
            print("qnumber before valid:" + str(qnumber))
            
            if questionform.validate_on_submit():
                    # global qnumber
                    
                print("qnumber after valid:" + str(qnumber))
                print("form data biatch")
                ans=questionform.question.data
                ansint=int(ans)
                print(ansint)
                correctindex=correctlist[qnumber].index(True)
                #truans=correctlist[qnumber][correctindex]
                print("true answer= " + str(correctindex))
                if(ansint==correctindex):
                    print("congrats correct")
                else:
                    print("wrong answer")
                qnumber += 1
                if(qnumber==5): qnumber=0        
            else: print("lokk at em errors biatch: ");print(questionform.errors)
                
            #else: print("something went wrong")
            
            return render_template('quiz.html', form=questionform, questiontext=questiontextlist[qnumber])
        print(datelist, mintemplist, maxtemplist)
        return render_template('index.html', city=city, form=form, msg=msg, datelist=datelist, mintemplist=mintemplist, maxtemplist=maxtemplist)
        # return render_template('index.html', form=form)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
        # return "wtf lmao u got 404'ed"

    # except Exception as e:
    #     return render_template('page-500.html', msg=e), 500

# Return sitemap
# @app.route('/sitemap.xml')
# def sitemap():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/quizy', methods=['GET', 'POST'])
def quizy():
    return "quiz boi"