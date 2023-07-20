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

def get_txout_scriptPubKeys(amount_to_send1, amount_to_send2):
    txout1_scriptPubKey = [OP_TRUE]
    txout2_scriptPubKey = [OP_FALSE]
    txout1 = create_txout(amount_to_send1, txout1_scriptPubKey)
    txout2 = create_txout(amount_to_send2, txout2_scriptPubKey)
    return txout1, txout2

def send_from_P2PKH_transaction(amount_to_send1, amount_to_send2, txid_to_spend, utxo_index):
    txout1, txout2 = get_txout_scriptPubKeys(amount_to_send1, amount_to_send2)
    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, [txout1, txout2], txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, [txout1, txout2], txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    all_money = 0.01695566
    amount_to_send1 = 0.0168
    amount_to_send2 = 0.00000001
    txid_to_spend = ('b9a51da87f8bafbf8227ffc029baf800be314aa442574edc501f46144cd5ee3c')
    utxo_index = 0
    print("my address: ", my_address)
    print("my public key: ", my_public_key.hex())
    print("my private key: ", my_private_key.hex())
    response = send_from_P2PKH_transaction(amount_to_send1, amount_to_send2, txid_to_spend, utxo_index)
    print("response status code: ", response.status_code)
    print("reponse reason: ", response.reason)
    print("response text: ", response.text)
