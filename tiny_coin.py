import hashlib as hasher
import datetime as date


class Block:
    """
    Defines what a block is on the chain. A block is a segment of the blockchain that stores data and
    the previous hash.
    """
    def __init__(self, index, timestamp, data, previous_hash) -> None:
        #index used to help ensure integrety through out the blockchain
        self.index = index
        self.timestamp = timestamp
        self.data = data 
        #blockchains are just linked lists with extra steps
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """
        Hashes the blocks using SHA-256 algo #thanksNSA
        """
        sha = hasher.sha256()
        sha.update(
            (str(self.index) +
            str(self.timestamp) + 
            str(self.data) + 
            str(self.previous_hash)).encode()
        )
        return sha.hexdigest()
    

def create_genesis_block():
    """
    The genesis block is the first block on the chain
    """
    return Block(0, date.datetime.now(), {"proof-of-work": 9,"transactions": None, "message": "Genesis Block of Tiny Coin made by Markus von Graf"}, "0")

def next_block(last_block: Block, data="") -> Block:
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    #if data is not passed create default data for block
    this_data = data if data != "" else f"Tiny Block: {str(this_index)}"
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


#Create the blockchain and add the genesis block 
blockchain = [create_genesis_block()]

#previous_block = blockchain[0]

#Hard coded amount of blocks on the chain
#num_of_blocks = 20

#add blocks on the chain with default values
# for i in range(0, num_of_blocks):
#     block_to_add = next_block(previous_block)
#     blockchain.append(block_to_add)
#     previous_block = block_to_add
#     print(f"Block #{block_to_add.index} has been added to the chain!")
#     print(f"Hash: {block_to_add.hash}")