import hashlib
import base58
import ecdsa
import secrets

def generate_keys():
    private_key = secrets.token_bytes(32)
    key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key
    public_key = b"\x04" + key.to_string()
    return private_key, public_key

def get_checksum(payload):
    first_hash = hashlib.sha256(payload).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    return second_hash[:4]

def generate_WIF_private_key(private_key, use_compressed = False):
    extended_key = b"\xef" + private_key
    if (use_compressed):
        extended_key += b"\x01"
    checksum_of_extended = get_checksum(extended_key)
    extended_key += checksum_of_extended
    wif_private_key = base58.b58encode(extended_key).decode('utf-8')
    return wif_private_key

def generate_address(public_key, use_compressed = False):
    sha256_pub = hashlib.sha256(public_key).digest()
    ripemd_pub = hashlib.new('ripemd160')
    ripemd_pub.update(sha256_pub)
    ripemd_pub = ripemd_pub.digest()

    extended_ripemd160 = b"\x6f" + ripemd_pub
    if (use_compressed):
        extended_ripemd160 += b"\x01"
    checksum_of_extended = get_checksum(extended_ripemd160)
    extended_ripemd160 += checksum_of_extended
    bitcoin_address = base58.b58encode(extended_ripemd160).decode('utf-8')
    return bitcoin_address


if __name__ == "__main__":
    private_key, public_key = generate_keys()
    print(' private key: ', private_key.hex())
    print(' public key: ', private_key.hex())
    print(' WIF private key: ', generate_WIF_private_key(private_key))
    print(' bitcoin address: ', generate_address(public_key))

