import pulumi


# Get the config ready to go.
config = pulumi.Config()


# If keyName is provided, an existing KeyPair is used, else if publicKey is provided a new KeyPair derived from the
# publicKey is created.
key_name = config.get('keyName')
public_key = config.get('publicKey')


# The privateKey associated with the selected key must be provided (either directly or base64 encoded)
def decode_key(key):
    try:
        key = base64.b64decode(key.encode('ascii')).decode('ascii')
    except:
        pass
    if key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
        return key
    return key.encode('ascii')


# Decode priviate key.
private_key = config.require_secret('privateKey').apply(decode_key)
