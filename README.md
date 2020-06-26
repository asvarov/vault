************************************************************************
vault status

vault operator init

vault operator unseal

export VAULT_ADDR='http://192.168.10.10:8200'

vault login

http://192.168.10.10:8200/ui/vault/secrets

vault secrets enable secret

vault kv put secret/database/mysql username=root password=toor

vault kv get secret/database/mysql

export VAULT_TOKEN=s.QwPl8Utcf7cu2uVs1Nyi3SqO

vault token create -policy=mysqldb

curl -X GET -H "X-Vault-Token:$VAULT_TOKEN" http://192.168.10.10:8200/v1/kv/database/mysql

echo 'path "secret/database/mysql" { capabilities = ["read","list"] }' | vault policy write mysqldb -

vault token create -policy=mysqldb -format=json -ttl=30s

while true; do echo -ne "`date`\r"; done

vault token renew <token>

vault token renew -accessor <access_token>
***********************************************

policy.hlc

path "secret/*" {
  capabilities = ["list"]
}
## for KV v2 - must add "/data/" to path secret (existing path to secret - secret/alpkr)
path "secret/data/alpkr" {
  capabilities = ["read", "list"]
}
path "secret/data/dbserver" {
  capabilities = ["read", "list"]
}
## for KV v1 - use simply path to secret
path "kv/*" {
  capabilities = ["read", "list"]
}

## enable audit

vault audit enable file file_path=/vault/logs/vault_audit.json


#Vault MYSQL database 
## create mysql user to create dynamically generates database credentials
CREATE USER 'creater'@'localhost' IDENTIFIED BY 'P@ssw0rd';
GRANT ALL PRIVILEGES ON *.* TO 'creater'@'localhost' WITH GRANT OPTION;
CREATE USER 'creater'@'%' IDENTIFIED BY 'P@ssw0rd';
GRANT ALL PRIVILEGES ON *.* TO 'creater'@'%' WITH GRANT OPTION;

vault write database/config/my-mysql-database \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(192.168.10.10:3306)/" \
    allowed_roles="db-readonly" \
    username="creater" \
    password="P@ssw0rd"
vault write database/roles/db_readonly \
    db_name=my-mysql-database \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="10m" \
    max_ttl="24h"
    
## *** Файл полиси для доступа к БД ***    
db_readonly.hcl
path "database/creds/db_readonly" {
  capabilities = [ "read" ]
}

## *** Создает токен под ПОЛИСИ ***
vault token create -policy=db_readonly

## *** Генерирует логин пароль для МУСКЛА на default_ttl время ***
VAULT_TOKEN=<token of policy=db_readonly> vault read database/creds/readonly

select host, user from mysql.user;
