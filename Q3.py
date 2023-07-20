import bitcoin.wallet
from bitcoin.core import b2lx, b2x
from utils import *
import time
import struct
from hashlib import sha256

BLOCK_REWARD = 6.25
COINBASE_DATA = '810199501AvaMirmohammadmahdi'.encode('utf-8').hex()
BITS = '0x1f010000'
VERSION = 2

bitcoin.SelectParams("mainnet")
pv_key = "5K4544JNYMJbJUKbDYd7xwXrsi828PLi48DVDx7AfeWz1ZD9Bea"
my_private_key = bitcoin.wallet.CBitcoinSecret(pv_key)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)


def P2PKH_scriptPubKey(key):
    return [OP_DUP, OP_HASH160, Hash160(key), OP_EQUALVERIFY, OP_CHECKSIG]

def reverse(x):
    return x[::-1]

def get_tx(txin, txout):
    txin.scriptSig =  CScript([int(COINBASE_DATA, 16).to_bytes(len(COINBASE_DATA)//2, 'big')])
    tx = CMutableTransaction([txin], [txout])
    return tx

def create_transaction():
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txid_to_spend, index = (64*'0'), int('0xFFFFFFFF', 16)
    txin = create_txin(txid_to_spend, index)
    txout = create_txout(BLOCK_REWARD, txout_scriptPubKey)
    return get_tx(txin, txout)

def calculate_target():
    exponent = BITS[2:4]
    coefficient = BITS[4:]
    target = int(coefficient, 16) * (int('2', 16) ** (8 * (int(exponent, 16) - 3)))
    target_hex = format(target, 'x')
    target_hex = str(target_hex).zfill(64)
    print("Target in hex: ", target_hex, '\n')
    return bytes.fromhex(target_hex)

def get_block(header, block_body):
    tx_count = b'\x01'
    block_size = len(header) + len(tx_count) + len(block_body)
    magic_number = 0xD9B4BEF9.to_bytes(4, "little")
    block = magic_number + struct.pack("<L", block_size) + header + tx_count + block_body
    return block

def print_info(nonce, hash, header, hash_rate, time_stamp, block_body):
    print("Success Mining!\n")
    print("nonce:", nonce, '\n')
    print("Hash rate:", hash_rate, "H/s\n")
    print("Block hash:", b2lx(hash))
    print("Block header:", header.hex(), '\n')
    block = get_block(header, block_body)
    print("Block in hex:", b2x(block), '\n')
    print("Version:", VERSION, '\n')
    print("Bits:", BITS, '\n')
    print("Time stamp:", time_stamp, '\n')

def mine_bitcoin(prev_block_hash):
    tx = create_transaction()
    merkle_root = b2lx(sha256(sha256(tx.serialize()).digest()).digest())
    print("\nMerkle root: ", merkle_root, '\n')
    block_body = tx.serialize()
    print("Block body: ", block_body.hex(), '\n')
    target = calculate_target()
    time_stamp = int(time.time())
    partial_header = struct.pack("<L", VERSION) + reverse(bytes.fromhex(prev_block_hash)) + reverse(bytes.fromhex(merkle_root)) + struct.pack('<LL', time_stamp, int(BITS, 16))
    nonce = 0
    start_time = time.time()
    while nonce <= 2**32:
        header = partial_header + struct.pack('<L', nonce)
        hash = sha256(sha256(header).digest()).digest()
        if reverse(hash) < target:
            hash_rate = nonce / (time.time() - start_time)
            print_info(nonce, hash, header, hash_rate, time_stamp,block_body)
            return
        nonce += 1


if __name__ == '__main__':
    n = input("please enter your block number: ")
    prev_block_hash = input("please enter prevoius block hash: ")
    # prev_block_hash = '000000004383fe923306472b416c0c2432523b3f5fbc2ca25def2c7155f9b5bb'
    # n = 9501
    mine_bitcoin(prev_block_hash)
