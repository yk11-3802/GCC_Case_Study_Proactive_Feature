from cryptography.fernet import Fernet

# Generate a random encryption key
def generate_key():
    key = Fernet.generate_key()
    return key

# Encrypt a password using the encryption key
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Example usage
encryption_key = generate_key()
password = "<Enter_password_to_be_encrypted>"

# Encrypt the password
encrypted_password = encrypt_password(password, encryption_key)
print("Encrypted password:", encrypted_password.decode())
print("Encryption key:",encryption_key.decode())
