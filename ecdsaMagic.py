import binascii, base64, ecdsa, hashlib, argparse, sys

# Modulo Inverse Method
def inverse_mod( a, m ):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod( d, c ) + ( c, )
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc

    assert d == 1
    if ud > 0: return ud
    else: return ud + m

# Return int value of byte string
def byteStrToInt(byteStr):
    return int(binascii.hexlify(byteStr),16)

# Return int value of message
def getMsgValue(msg):
    return int(hashlib.sha1(msg).hexdigest(), 16)

# Return Sig Value
def getSigValue(sigPart):
    return byteStrToInt(base64.b64decode(sigPart))

# Calculate Private key, return ruple
def getKey(r, s1 ,s2, m1, m2, n):
    k   = (m1-m2) * inverse_mod((s1-s2), n) % n
    d_a = (s1*k-m1) * inverse_mod(r, n) % n
    return (d_a, k)

# Format Key
def formatKey(key, frmt):
    if frmt == "pem": return key.to_pem()
    if frmt == "der": return key.to_der()
    if frmt == "str": return key.to_string()

# Get curve used
def getCurve(signature):
    curves = {48:ecdsa.NIST192p, 56:ecdsa.NIST224p, 
    64:ecdsa.NIST256p, 96:ecdsa.NIST384p, 132:ecdsa.NIST521p}

    return curves[len(base64.b64decode(signature))]

# Strip file extensions from output name ad apends new extansion
def setOutName(outName, frmt):
    return ((outName+".").split(".")[0])+"."+frmt 

# Create key file
def createFile(outName, key):
    f = open(outName, 'wb')
    f.write(key); f.close()
    print "\nFile: " + outName + "\n" + key

# Argument error handeling
def checkErrors(parser):
    args = parser.parse_args()
    if args.s[0][:len(args.s[0])/2] != args.s[1][:len(args.s[1])/2]:
        return parser.prog + ": error: r of signatures do not match!"

    return None

def main(): 
    parser = argparse.ArgumentParser(description="Calculate ECDSA private Key from signatures (r,s) & (r,s')", version="1.0")
    parser.add_argument('-m', nargs=2, help='Signed message values', metavar=("<msg_1>","<msg_2>"), required=True)
    parser.add_argument('-s', nargs=2, help="Message signature values. Must be (r,s) (r,s')", metavar=("<sig_1>","<sig_2>"), required=True)
    parser.add_argument('-o', help='Output filename', metavar="[output]")
    parser.add_argument('-f', help='Returned private key format', choices=['pem', 'der', 'str', 'raw'], default="pem")
    
    parser.usage = "%(prog)s [-h] [-v] -m <msg_1> <msg_2> -s <sig_1> <sig_2>\n" + \
    (len(sys.argv[0])+8)*" " +"[-o [output]] [-f {pem,der,str,int}]"

    parser._optionals.title = "Arguments"
    args = parser.parse_args()

    # Check or argument errors
    error = checkErrors(parser)
    if error != None:
        parser.print_usage()
        print error; exit(1)

    # Try to parse argument string values to valid numerical values
    try:
        m1 = getMsgValue(args.m[0])
        m2 = getMsgValue(args.m[1])
        r  = getSigValue(args.s[0][:len(args.s[0])/2])
        s1 = getSigValue(args.s[0][len(args.s[0])/2:])
        s2 = getSigValue(args.s[1][len(args.s[1])/2:])

        curve  = getCurve(args.s[0])
        n      = curve.order
        d_a, k = getKey(r, s1 ,s2, m1, m2, n)

        if args.f == "raw": key = d_a
        else: key = formatKey(ecdsa.SigningKey.from_secret_exponent(d_a, curve), args.f)

    # Mathematical error thrown
    except:
        print "[-] Failed to generate Private Key from provied data!"
        print "[-] Check provided values are correct or use -h for more info"; exit(1)

    # If output name provided, save to file.  
    if args.o != None:
        outName = setOutName(args.o, args.f)
        createFile(outName, key)
    
    # If not, print to screen
    else:
        print "\nPrimare Key:"
        print key

    exit(0)

if __name__ == "__main__":
    main()

