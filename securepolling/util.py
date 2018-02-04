class signed_screed(object):
    _prefix = 'Fake signed screed:\n'
    @staticmethod
    def dumps(registrar, phrases, phrases_signature,
              public_key, public_key_signature):
        xs = registrar, phrases, phrases_signature, public_key, public_key_signature
        return signed_screed._prefix + '\n'.join(xs)
    @staticmethod
    def loads(x):
        registrar, phrases, phrases_signature, public_key, public_key_signature = \
            x[len(signed_screed._prefix):].split('\n')
        # TODO: Check phrases signature
        # TODO: Check public key signature
        return {
            'registrar': registrar,
            'phrases': phrases,
            'public_key': public_key,
        }
