import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
pv_key = "925NvBWuEWdw1Au6CYpgqovtQBhtS3TfjXiLo7NhmoBLMYeeby3"
my_private_key = bitcoin.wallet.CBitcoinSecret(pv_key)
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey(key):
    return [OP_DUP, OP_HASH160, Hash160(key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index):
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = [OP_TRUE]
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = []

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    all_money = 0.0168
    amount_to_send = 0.0166
    txid_to_spend = ('44f28dcfed5759766ff76603585e80cd7fe121aabae9c45ec7f2303e484d6892')
    utxo_index = 0

    print("my address: ", my_address)
    print("my public key: ", my_public_key.hex())
    print("my private key: ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index)
    print("response status code: ", response.status_code)
    print("reponse reason: ", response.reason)
    print("response text: ", response.text)
