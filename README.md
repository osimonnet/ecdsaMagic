ecdsaMagic
==========
A tool used to calculate the private key used to generate 2 bad signatures (r,s) (r,s')
Requires 2 flawed signatures & the original data / messages that were signed (assumes sha256 was used)

Dependencies
------------
This program requires the ecdsa library to run.  
You can install ecdsa using pip as shown below:  
`pip install ecdsa`

Command-line
------------
```
$ python ecdsaMagic.py -h
usage: ecdsaMagic.py [-h] [-v] -m <msg_1> <msg_2> -s <sig_1> <sig_2>
                     [-o [output]] [-f {pem,der,str,int}]

Calculate ECDSA private Key from signatures (r,s) & (r,s')

Arguments:
  -h, --help            show this help message and exit
  --mf <base64 | hash>  Message format
  -m <msg_1> <msg_2>    Signed messages
  -s <sig_1> <sig_2>    Message signature values. Must be (r,s) (r,s')
  -o [output]           Output filename
  -f {pem,der,str,raw}  Returned private key format

```

Calculate private key example:
------------
Given the following two Message & Signature pairs:  
```
file1: /media/test/usb/data/image.png
 msg1: 32b4b85c411e2961dfe7a9c784754b6d68ce25b28443a388258bcefb7596547c  
 sig1: 3045022029aa00ee6fd4630fc9c99dc934eb89a...3389f18afeb9398be566297f25d4  

file2: /media/test/usb/data/notes.txt
 msg2: fa2f36aed4aacdc1dd0bd00d0946fdc1c995983777f4ee154627678c59830f15  
 sig2: 3045022029aa00ee6fd4630fc9c99dc934eb89a...b3afa61f8e9bb66639b3f8df2240  
```

The messages can be passed as hashes directly, or generated on the fly as follows:
```
$ export m1=$(cat /media/test/usb/data/image.png | sha256sum | cut -d " " -f 1)
$ export m2=$(cat /media/test/usb/data/notes.txt | sha256sum | cut -d " " -f 1)
```

With the hashes ready, we now want the signatures. In this case they are in DER format: 
```
$ export sig1_asn1=3045022029aa00ee6fd4630fc9c99dc934eb89a...18afeb9398be566297f25d4
$ export sig2_asn1=3045022029aa00ee6fd4630fc9c99dc934eb89a...61f8e9bb66639b3f8df2240
```

The individual r, and s values can be extracted from the DER encoded signature using `openssl asn1parse`: 
```
$ openssl asn1parse -inform DER -in <(echo -n $sig1_asn1 | xxd -r -p)
    0:d=0  hl=2 l=  69 cons: SEQUENCE          
    2:d=1  hl=2 l=  32 prim: INTEGER           :29AA00EE6FD4630FC9C99DC9...510F6F4BA7F1BF6F3
   36:d=1  hl=2 l=  33 prim: INTEGER           :B42777F7A1B5F8743CDDF069...9398BE566297F25D4
```

The scripts expects this to be passed as a pipe-delimited r,s value string. So we can use a one-liner to achieve this using the openssl output: 
```
$ export sig1_raw=$(echo $(openssl asn1parse -inform DER -in <(echo -n $sig1_asn1 | xxd -r -p) | grep INTEGER | awk '{print $7}') | sed 's/ :/|/g' | sed 's/://g')
$ export sig2_raw=$(echo $(openssl asn1parse -inform DER -in <(echo -n $sig2_asn1 | xxd -r -p) | grep INTEGER | awk '{print $7}') | sed 's/ :/|/g' | sed 's/://g')

$ echo sig1 r\|s: $sig2_raw
sig1 r|s: 29AA00EE6...7F1BF6F3|D04E766F6...F8DF2240
$ echo sig1 r\|s: $sig1_raw   
sig1 r|s: 29AA00EE6...7F1BF6F3|B42777F7A...297F25D4
```


With all the values required at hand and in the right format, we can pass them to the script to calculate the private key: 
```
$ python ecdsaMagic.py --mf hash -m "$m1" "$m2" -s "$sig1_raw" "$sig2_raw"

m1  22934947309324038181051892...9084585062070864285728580719740
m2  11316163136559109834809731...96590744536062062720717796085525
 r  18845197221170589343906318...0405879359276255241170402932467
s1  81486047764466539049478553...2048262150788830926374891890132
s2  94219703986050012650860055...8534901308904824552187089592896

-----BEGIN PRIVATE KEY-----
MIGEAgEBMBAG...EGBSuBBAAKBG0wawI...zn4u5dvPS//24TfipY
82O26PkhocPx...uhRANCAASDPma8sE7...60bof6ptho5y3i2wJK
61RZoj57ATcp...VJDDJxRXSgqn2zEz1...+LWZc3
-----END PRIVATE KEY-----
```

License
-------
This software is MIT-Licensed.
