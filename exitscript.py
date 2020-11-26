import sys
import base64

# targetdirectory = '/var/lib/lokinet/lokinetExitCodes.txt'
targetdirectory = 'C:/Users/Potter/Downloads/Hashedbianries/ExitCodes.txt'

with open(targetdirectory) as f:
    data = f.read().splitlines() 

b64args = base64.b64decode(sys.argv[2])
b64args = b64args.decode('ascii')
b64args = b64args.rstrip()

if any(b64args in s for s in data):
    print("Exited With code 0")
    sys.exit(0)
    pass
else:
    print("Exited With code 1")
    sys.exit(1)
    pass
