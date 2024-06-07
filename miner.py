from flask import Flask
from flask import request 
import json
from tiny_coin import *


node = Flask(__name__)

#This is just a random address
miner_address = "HSrOJoR3OraHHphZO1pPfSKMEM1AX3TqiKDidx4XbTo="

#Store the transactions that this node has in a list
this_nodes_transactions = []

peer_nodes = []

@node.route('/tx', methods=["POST"])
def transaction():
    if request.method == "POST":
        #extracts the json from the request
        new_transaction = request.get_json()
        #add transaction to list
        this_nodes_transactions.append(new_transaction)

        print("New Transaction!")
        print(f"FROM: {new_transaction['from']}")
        print(f"TO: {new_transaction['to']}")
        print(f"AMOUNT: {new_transaction['amount']}")
        
        return "Transaction submission Successful"



def proof_of_work(last_proof) -> int:
    #create a nonce
    nonce = last_proof + 1
    #while the nonce is not divisible by 9 and the last_proof increment the nonce
    while not (nonce % 9 ==0 and nonce % last_proof == 0):
        nonce += 1
        print(nonce)
    #once the nonce is found return it
    return nonce

@node.route("/mine", methods=['GET'])
def mine():
    #get the last block
    last_block = blockchain[len(blockchain) - 1]
    #get the last proof
    last_proof = last_block.data['proof-of-work']
    #mine the block
    proof = proof_of_work(last_proof=last_proof)
    #append the transaction to the list
    this_nodes_transactions.append(
        {'from': "network", "to": miner_address, "amount": 1}
    )
    #create the new block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp =  date.datetime.now()
    last_block_hash = last_block.hash

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)
    #empty the list
    this_nodes_transactions[:] = []
    #let the client know the block has been mined
    return json.dumps({"index": new_block_index, "timestamp": str(new_block_timestamp), "data": new_block_data, "hash": last_block_hash})


@node.route("/blocks", methods=["GET"])
def get_blocks():
    chain_to_send = blockchain
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = str(block.hash)
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send

def find_new_chains():
    other_chains = []

    for node_url in peer_nodes:
        block = request.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain 
    blockchain = longest_chain 




node.run()