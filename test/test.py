import pdb
import paramiko

rsa_key = paramiko.RSAKey.generate(bits=2048, progress_func=None)
rsa_key.write_private_key_file('tmp.pem')


class TestClass(object):
    def test_method(self, input):
        pdb.set_trace()
        print (input)