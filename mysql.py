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

vault write database/config/test1
plugin_name = mysql - database - plugin
connection_url = "{{username}}:{{password}}@tcp(192.168.10.10:3306)/"
allowed_roles = "my-role"
username = "root"
password = "P@ssw0rd"


vault write database/roles/my-role \
    db_name=test1 \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"

vault read database/creds/my-role