import hvac
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

client = hvac.Client(url='http://192.168.10.10:8200', token='s.E2fgkWhNLtEYSJmR6vySwKRo') # token policy mysql
r = client.is_authenticated()
print(f'Client is authenticated: {r}')

read_response = client.secrets.kv.read_secret_version(path='pythonapp1')
login = read_response['data']['data']['mysqllogin']
password = read_response['data']['data']['mysqlpwd']
hostip = read_response['data']['data']['mysqlserverip']
print(f'Value "login": {login}')
print(f'Value "password": {password}')
print(f'Value "ip": {hostip}')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{login}:{password}@{hostip}/test1'
db = SQLAlchemy(app)

print(app.config['SQLALCHEMY_DATABASE_URI'])