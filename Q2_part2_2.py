import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
pv_key = "925NvBWuEWdw1Au6CYpgqovtQBhtS3TfjXiLo7NhmoBLMYeeby3"
pv_key1 = "92FzYRi2Kz3DZNub9eeHx6466JjDy31J94WCr1T4DhFwYfZri9W"
pv_key2 = "92GcmLAheuU4gBSRYmqF2eCiJtnBDKLrQH3HCQUqPkEZTUCE9gg"
pv_key3 = "91xg28ARkm4RGVqLehMuwPKVnQ99Lw5qSeK4TLGSX5qFQBWeMgc"
my_private_key = bitcoin.wallet.CBitcoinSecret(pv_key)
private_key1 = bitcoin.wallet.CBitcoinSecret(pv_key1)
private_key2 = bitcoin.wallet.CBitcoinSecret(pv_key2)
private_key3 = bitcoin.wallet.CBitcoinSecret(pv_key3)
my_public_key = my_private_key.pub
public_key1 = private_key1.pub
public_key2 = private_key2.pub
public_key3 = private_key3.pub

my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
def P2PKH_scriptPubKey(key):
    return [OP_DUP, OP_HASH160, Hash160(key), OP_EQUALVERIFY, OP_CHECKSIG]

def scriptSig(txin, txout, txin_scriptPubKey):
    signature1 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key1)
    signature2 = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key2)
    return [OP_0, signature1, signature2]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index):
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = [OP_2, public_key1, public_key2, public_key3, OP_3, OP_CHECKMULTISIG]
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = scriptSig(txin, [txout], txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    all_money = 0.0164
    amount_to_send = 0.016
    txid_to_spend = ('1a9e254ee69d1f9cbf4d50240a546701bf1404b462cc3bfc9009e186eb5760fa')
    utxo_index = 0

    print("my address: ", my_address)
    print("my public key: ", my_public_key.hex())
    print("my private key: ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index)
    print("response status code: ", response.status_code)
    print("reponse reason: ", response.reason)
    print("response text: ", response.text)
