import hvac

client = hvac.Client(url='http://192.168.10.10:8200')
shares = 5
threshold = 3

if client.sys.is_sealed() is True and client.sys.is_initialized() is False:

    result = client.sys.initialize(shares, threshold)
    root_token = result['root_token']
    keys = result['keys']
    client.token = root_token

    with open('root_token_vault.json', mode='w') as f:
        f.write(root_token)

    for i in keys:
        with open(f'individual_key_{keys.index(i) + 1}_vault.json', mode='w') as f:
            f.write(i)

    print(f'Storage is sealed?: {client.sys.is_sealed()}')

    for i in keys:
        print(f'individual key #{keys.index(i) + 1}: {keys[keys.index(i)]}')

    for i in range(threshold):
        unseal_response = client.sys.submit_unseal_key(keys[i])

    unseal_response = client.sys.submit_unseal_keys(keys)
    print(f'Storage is sealed?: {client.sys.is_sealed()}')
else:
    print(f'Storage is unsealed and client is initialized!')
