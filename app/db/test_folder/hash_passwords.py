from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

print(password_hasher.hash("atharva123"))
print(password_hasher.hash("rahul123"))
print(password_hasher.hash("priya123"))
print(password_hasher.hash("temporary123"))