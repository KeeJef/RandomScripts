import glob
import hashlib
import os.path

targetdirectory = 'C:/Users/ron/Documents/FilesToHash/*'
hasharray = []
signaturetext = """The following hashes have been signed for verification using keejef's GPG keys
located in the loki core repository at https://github.com/loki-project/loki-core/blob/master/utils/gpg_keys/KeeJef.asc.

SHA256 Hashes\n
"""
stringhashes = ""

filenames = glob.glob(targetdirectory)

for filename in filenames:
    with open(filename, 'rb') as inputfile:
        data = inputfile.read()
        hasharray.append(os.path.basename(inputfile.name) +" "+ hashlib.sha256(data).hexdigest())

for hashes in hasharray:
    stringhashes += hashes+ " \n"
    pass


print(signaturetext + stringhashes)


