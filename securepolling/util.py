class signed_screed(object):
    _prefix = 'Fake signed screed:\n'
    @staticmethod
    def dumps(registrar, phrases, phrases_signature,
              public_key, public_key_signature):
        xs = registrar, phrases_signature, public_key, public_key_signature,
        for phrase in phrases:
            xs += phrase.replace('\n', ' '),
        return signed_screed._prefix + '\n'.join(xs)
    @staticmethod
    def loads(x):
        registrar, phrases_signature, public_key, public_key_signature, *phrases = \
            x[len(signed_screed._prefix):].split('\n')
        # TODO: Check phrases signature
        # TODO: Check public key signature
        return {
            'registrar': registrar,
            'phrases': phrases,
            'public_key': public_key,
        }

def keygen():
    return 'Fake private key', 'Fake public key'
