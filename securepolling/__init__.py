def users():
    '''
    Get list of users created on this client.
    '''

def user_create(registrar, identity):
    '''
    Create a user.

    Add random salt to identity to prevent others from querying registrars'
    servers on users' behalf, when identity is their real name.

    :param registrar: the registrar's server URL
    :param identity: A unique string with information that the registrar will
    use to verify user identity in person.
    '''

def user_get(registrar, identity):
    '''
    Get a user with the given identity.
    '''

def user_tally_spiders(registrar, identity, *tallyspiders):
    '''
    Update the user options as provided in `createUser` function.

    :param tallyspiders: preferred tallyspiders
    '''

def user_generate_keypair(registrar, identity):
    '''
    Generates a new keypair and save it.
    If a keypair already exists with a valid registrar signature, return an
    error, otherwise overwrite an existing signature.
    '''

def _user_send_blinded_key(registrar, identity):
    '''
    App generates and stores a random salt. The client acquires a public subkey
    from the registrar. The app uses that public subkey to generate a blinded
    version of the user's public key, then sends the blinded version to the
    registrar.
    '''

def _user_signature_valid(registrar, identity):
    '''
    Returns true if the locally-stored registrar signature is valid. Returns false if the registrar signature is expired or not present.
    '''

def _user_get_signature(registrar, identity):
    '''
    Get the registrar signature for the given identity. This function will
    attempt to retrieve the registrar's signature of user's blinded key, unblind
    it using the stored salt, store the result (a signature of user's public
    key) locally, and return true. If there is no valid signature data supplied
    by the registrar, it will return false.
    '''




### ```user.screed.append(msg, cb)```

Add a message to the local screed.

### ```user.screed.remove(index, cb)```

Remove a message from the local screed using the given index.

### ```user.screed.list(cb)```

List the current messages in the local screed, along with their indexes.

### ```user.uploadScreed(cb)```

Uploads the user's local screed to the registrar. If there is no valid signature for the user's registrar, or the server refuses to accept, or can't be reached, will return an error.
