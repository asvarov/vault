import hvac

with open('root_token_vault.json', mode='r') as f:
    root_token = f.read()
client = hvac.Client(url='http://192.168.10.10:8200', token=root_token)
r = client.is_authenticated()
print(f'Client is authenticated: {r}')

secrets_engines_list = client.sys.list_mounted_secrets_engines()['data']

print(secrets_engines_list.keys())

#Read Mount Configuration
secret_backend_tuning = client.sys.read_mount_configuration(path='secret')
print('The max lease TTL for the "secret" backend is: {max_lease_ttl}'.format(
    max_lease_ttl=secret_backend_tuning['data']['max_lease_ttl'],))

client.secrets.kv.v2.create_or_update_secret(
    path='pythonapp1',
    secret=dict(login='username', password='userpassword'),
)

read_response = client.secrets.kv.read_secret_version(path='pythonapp1')
login = read_response['data']['data']['login']
password = read_response['data']['data']['password']
print(f'Value under path "secret/pythonapp" / key "login": {login}')
print(f'Value under path "secret/pythonapp" / key "password": {password}')

list_response = client.secrets.kv.v2.list_secrets(path='/',)
list_secrets = list_response.get('data').get('keys')
print(f'List secrets: {list_secrets}')

# list_response = client.secrets.kv.v2.list_secrets(
#     path='pythonapp/login',
# )
#
# print('The following paths are available under "hvac" prefix: {keys}'.format(
#     keys=','.join(list_response['data']['keys']),
# ))