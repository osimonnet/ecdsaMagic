import binascii, base64, hashlib, argparse, sys, ecdsa
from ecdsa.numbertheory import inverse_mod

# defines a signature object for sig verification 
class Sig(object):
    def __init__(self, s, r):
        self.s = s 
        self.r = r

# Return int value of byte string
def byteStrToHex(byteStr):
    return binascii.hexlify(byteStr).decode("utf-8")

def byteStrToInt(byteStr):
    return int(binascii.hexlify(byteStr),16)

# Return int value of message
def getMsgValue(msg, fmt):
    if fmt == "base64":
        data = base64.b64decode(msg)
        return int(hashlib.sha256(data).hexdigest(), 16)

    return int(msg, 16)

# Return Sig Value
def getSigValue(sigPart, fmt="raw"):
    return(int(sigPart, 16))

# Calculate Private key, return ruple
def getKey(r, s1 ,s2, m1, m2, n, curve):

    for v in (s1 - s2, s1 + s2, -s1 - s2, -s1 + s2):
        k = (m1 - m2) * inverse_mod(v, n) % n
        d = (k*s1 - m1) * inverse_mod(r, n) % n
        
        private_key = ecdsa.SigningKey.from_secret_exponent(d, curve)
        print(formatKey(private_key, "pem"))

        if private_key.get_verifying_key().pubkey.verifies(m1, Sig(s1, r)):
            return (d, k)

    return (None, None)
    

# Format Key
def formatKey(key, frmt):
    if frmt == "pem": return key.to_pem(format="pkcs8").decode("utf-8")
    if frmt == "der": return base64.b64encode((key.to_der(format="pkcs8"))).decode("utf-8")
    if frmt == "str": return key.to_string()

# Get curve used
def getCurve(signature):
    curves = {48:ecdsa.NIST192p, 56:ecdsa.NIST224p, 
    64:ecdsa.SECP256k1, 96:ecdsa.NIST384p, 132:ecdsa.NIST521p}

    return curves[len(base64.b64decode(signature))]

# Strip file extensions from output name ad apends new extansion
def setOutName(outName, frmt):
    return ((outName+".").split(".")[0])+"."+frmt 

# Create key file
def createFile(outName, key):
    f = open(outName, 'wb')
    f.write(key); f.close()
    print("\nFile: " + outName + "\n" + key)

# Argument error handeling
def checkErrors(parser):
    args = parser.parse_args()
    if args.s[0][:int(len(args.s[0])/2)] != args.s[1][:int(len(args.s[1])/2)]:
        return parser.prog + ": error: r of signatures do not match!"

    return None

def fail():
    print("[-] Failed to generate Private Key from provied data!")
    print("[-] Check provided values are correct or use -h for more info"); 
    exit(1)

def main(): 
    parser = argparse.ArgumentParser(description="Calculate ECDSA private Key from signatures (r,s) & (r,s')")
    parser.add_argument('--mf',help='Message format', metavar=("<base64 | hash>"), required=True)
    parser.add_argument('-m',  nargs=2, help='Signed messages', metavar=("<msg_1>","<msg_2>"), required=True)
    parser.add_argument('-s',  nargs=2, help="Message signature values. Must be (r,s) (r,s')", metavar=("<sig_1>","<sig_2>"), required=True)
    parser.add_argument('-o',  help='Output filename', metavar="[output]")
    parser.add_argument('-f',  help='Returned private key format', choices=['pem', 'der', 'str', 'raw'], default="pem")
    
    parser.usage = "%(prog)s [-h] [-v] -m <msg_1> <msg_2> -s <sig_1> <sig_2>\n" + \
    (len(sys.argv[0])+8)*" " +"[-o [output]] [-f {pem,der,str,int}]"

    parser._optionals.title = "Arguments"
    args = parser.parse_args()

    # Check or argument errors
    error = None #checkErrors(parser)
    if error != None:
        parser.print_usage()
        print(error); exit(1)

    # Try to parse argument string values to valid numerical values
    try:

        r_raw  = args.s[0][:int(len(args.s[0])/2) ]
        s1_raw = args.s[0][ int(len(args.s[0])/2):]
        s2_raw = args.s[1][ int(len(args.s[0])/2):]

        m1 = getMsgValue(args.m[0], args.mf)
        m2 = getMsgValue(args.m[1], args.mf)
        r  = getSigValue(r_raw)
        s1 = getSigValue(s1_raw)
        s2 = getSigValue(s2_raw)

        print()
        print("m1 ", (m1))
        print("m2 ", (m2))
        print(" r ", (r))
        print("s1 ", (s1))
        print("s2 ", (s2))
        print()

        curve  = getCurve(args.s[0])
        n      = curve.order
        d, k   = getKey(r, s1 ,s2, m1, m2, n, curve)

        if d is None: fail()

        if args.f == "raw": key = d
        else: key = formatKey(ecdsa.SigningKey.from_secret_exponent(d, curve), args.f)

    # Mathematical error thrown
    except Exception as e:
        print(e)
        fail()

    # If output name provided, save to file.  
    if args.o != None:
        outName = setOutName(args.o, args.f)
        createFile(outName, key)
    
    # If not, print to screen
    else:
        print(key)

    exit(0)

if __name__ == "__main__":
    main()
