import os
import pyotp
import qrcode

key = "TOPSECRETKEYLOLOLOLOL"

# uri = pyotp.totp.TOTP(key).provisioning_uri(name="Yash_Batish",issuer_name="VVT Engineering")

# print(uri)
# qrcode.make(uri).save("totp.png")

totp = pyotp.TOTP(key)

def verify_passcode(passcode):
    return totp.verify(passcode)
