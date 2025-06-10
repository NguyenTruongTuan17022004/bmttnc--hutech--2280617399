from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def generate_client_key_pair(parameters):
    """
    Generates a Diffie-Hellman private and public key pair for the client
    using the provided parameters.
    """
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, server_public_key):
    """
    Derives the shared secret using the client's private key and the server's public key.
    """
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    """
    Main function to load the server's public key, generate the client's key pair,
    derive the shared secret, and print it.
    """
    # Load server's public key
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read())

    # Get the parameters from the server's public key
    parameters = server_public_key.parameters()

    private_key, public_key = generate_client_key_pair(parameters)
    shared_secret = derive_shared_secret(private_key, server_public_key)

    print("Shared Secret:", shared_secret.hex())

if __name__ == "__main__":
    main()