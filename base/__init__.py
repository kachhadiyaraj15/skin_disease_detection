from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import warnings
from datetime import timedelta

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app=Flask(__name__)
app.secret_key='healthcraechatbot'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['TESTING']=True
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SQLALCHEMY_ECHO']= False
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/pythondb'
app.config['SQLALCHEMY_MAX_OVERFLOW']=0
db=SQLAlchemy(app)

import base.com.controller