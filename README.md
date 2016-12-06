ecdsaMagic
==========
A tool used to calculate the private key used to generate 2 bad signatures (r,s) (r,s')
Requires 2 flawed signatures & the original messages/nonces that were signed

Dependencies
------------
This program requires the ecdsa Librarie to run.  
You can install ecdsa using pip as shown below:  
`pip install ecdsa`

Command-line
------------
```
> python python ecdsaMagic.py -h
usage: ecdsaMagic.py [-h] [-v] -m <msg_1> <msg_2> -s <sig_1> <sig_2>
                     [-o [output]] [-f {pem,der,str,raw}]

Calculate ECDSA Private Key from signatures (r,s) & (r,s')

Arguments:
  -h, --help          show this help message and exit
  -v, --version       show program's version number and exit
  -m <msg_1> <msg_2>  Signed Message Values
  -s <sig_1> <sig_2>  Message Signature Values. Must be (r,s) (r,s')
  -o [output]         Output filename
  -f {pem,der,str,raw}    Returned Private Key Format
```

Calculate private key example:
Given these 2 Message & Signature pairs:  
msg1: VGhpcyBpcyBOb25jZSBvbmVzIFZhbHVl  
sig1: WG05dVkyVWdkSGR2Y3lCV1lXeDFaU0JwVkcwNWRWa3lWV2RrU0dSMlkzbENWMWxY  
msg2: Tm9uY2UgdHdvcyBWYWx1ZSBpcyB0aGlz  
sig2: WG05dVkyVWdkSGR2Y3lCV1lXeDFaU0JwT2tjd05XUldhM2xXVjJSclUwZFNNbGt6  

```
> python ecdsaMagic.py -m VGhpcyBpcyBOb25jZSBvbmVzIFZhbHVl Tm9uY2UgdHdvcyBWYWx1ZSBpcyB0aGlz -s WG05dVkyVWdkSGR2Y3lCV1lXeDFaU0JwVkcwNWRWa3lWV2RrU0dSMlkzbENWMWxY WG05dVkyVWdkSGR2Y3lCV1lXeDFaU0JwT2tjd05XUldhM2xXVjJSclUwZFNNbGt6

Primare Key:
-----BEGIN EC PRIVATE KEY-----
MF8CAQEEGKyazj7qlGXIch9LnKILzbJJ1/hJ6EZyjaAKBggqhkjOPQMBAaE0AzIA
BDoGv/iV//ZB8gnVjIsfCL+p4hmdvDyKj9hjx7lXSRJTVatlh1ZgpbQ+92hz/YdI
VA==
-----END EC PRIVATE KEY-----
```

License
-------
This software is MIT-Licensed.