from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def generate_dh_parameters():
    """
    Generates Diffie-Hellman parameters with a specified generator and key size.
    """
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def generate_server_key_pair(parameters):
    """
    Generates a Diffie-Hellman private and public key pair for the server
    using the provided parameters.
    """
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def main():
    """
    Main function to orchestrate the generation of DH parameters,
    server key pair, and saving the server's public key to a PEM file.
    """
    parameters = generate_dh_parameters()
    private_key, public_key = generate_server_key_pair(parameters)

    # Save the server's public key to a PEM file
    with open("server_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    main()