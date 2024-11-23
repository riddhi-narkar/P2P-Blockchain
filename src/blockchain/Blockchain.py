from typing import List, Tuple, Set
# local
from networking import config
from blockchain.Block import Block
from blockchain.Transaction import Transaction
import hashlib
import json
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # self.difficulty = config.BLOCKCHAIN_DIFFICULTY
        self.difficulty = 4
        self.index = 0


    def generate_genesis_block(self):
        # add genesis block
        if len(self.chain) == 0:
            print('Mining Block #0...')
            genesis = Block([], 'genesis')
            genesis.mine(self.difficulty)
            self.chain.append(genesis.serialized)

    def is_valid(self, chain_to_validate: List = None) -> bool:
        # if no chain in params, use self.chain. Else use chain in params.
        chain = self.chain if chain_to_validate is None else chain_to_validate
        for index in range(1, len(chain)):
            current_block = chain[index]
            previous_block = chain[index - 1]
            if current_block["previous_hash"] != previous_block["hash"]:
                return False
        return True

    def add_block(self, miner_address):
        # We reward those who mine with 1 coin, so we append a new transaction with this reward
        self.pending_transactions.append(Transaction('blockchain', miner_address, 1).serialized) # from blockchain, to miner, 1 coin
        # construct a new block
        new_block = Block(
            self.pending_transactions,
            self.chain[-1]['hash']
        )
        print(f'Mining block #{len(self.chain)}...')
        # mine its
        new_block.mine(self.difficulty)

        new_block_serialized = new_block.serialized
        new_block_serialized['computed_hash'] = self.compute_block_hash(new_block_serialized)  # Add this line

        # Append to the chain
        self.chain.append(new_block_serialized)

        # Clear the pending transactions
        self.pending_transactions = []


    def new_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction.serialized)

    def replace_chain(self, new_chain: List):
        # if new chain is bigger, replace current with the new one
        if len(new_chain) > len(self.chain):
            self.chain = new_chain

    def get_balance(self, address):
        """
        Iterate through chain and find transactions where provided address appears.
        """
        balance = 100
        for block in self.chain:
            for t in block['transactions']:
                if t['recipient'] == address:
                    balance += t['amount']
                elif t['sender'] == address:
                    balance -= t['amount']
        return balance

    def mine_block(self, block_data):
        """
        Mines a new block by computing its hash based on block data and the previous block's hash.
        """
        # Prepare block data
        block_data['previous_hash'] = self.chain[-1]['hash'] if self.chain else '0'  # Use '0' for the genesis block

        # Compute the hash for the block
        block_data['computed_hash'] = self.compute_block_hash(block_data)

        # Store the hash as the block's official hash
        block_data['hash'] = block_data['computed_hash']

        # Add the mined block to the chain
        self.chain.append(block_data)

    def compute_block_hash(self, block):
        # """
        # Computes the hash of the block by hashing its string representation.
        # """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        # block_string = f"{block_serialized['index']}{block_serialized['previous_hash']}{block_serialized['timestamp']}{block_serialized['nonce']}{block_serialized['transactions']}"
        # return hashlib.sha256(block_string.encode()).hexdigest()

    # def validate_chain(self):
    #     """
    #     Validate the entire blockchain by checking the hashes and the previous block hash.
    #     """
    #     for i in range(1, len(self.chain)):
    #         current_block = self.chain[i]
    #         previous_block = self.chain[i - 1]

    #         if(i==1):
    #             print(f"Blockchain is valid!")

    #         # Ensure the current block's hash matches the computed hash
    #         if current_block['hash'] != current_block['computed_hash']:
    #             print(f"Block {i} has invalid hash!")
    #             return False

    #         # Ensure the previous block's hash matches the 'previous_hash' in the current block
    #         if current_block['previous_hash'] != previous_block['hash']:
    #             print(f"Block {i} has invalid previous_hash!")
    #             return False
    #         else:
    #             print(f"Blockchain is valid!")
    #             return True
    # def validate_chain(self):
    #     """
    #     Validate the entire blockchain by checking the hashes and the previous block hash.
    #     """
    #     for i in range(1, len(self.chain)):
    #         current_block = self.chain[i]
    #         previous_block = self.chain[i - 1]

    #         # Ensure the current block's hash matches the computed hash
    #         if current_block['hash'] != current_block['computed_hash']:
    #             print(f"Block {i} has invalid hash!")
    #             return False

    #         # Ensure the previous block's hash matches the 'previous_hash' in the current block
    #         if current_block['previous_hash'] != previous_block['hash']:
    #             print(f"Block {i} has invalid previous_hash!")
    #             return False

    #     print("Blockchain is valid!")
    #     return True



    def __str__(self):
        return ''.join([(
            14 * '-' + f'Block #{self.chain.index(block)}' + '-' * 14 + '\n' +
            f'data: {block["transactions"]}\n' +
            f'hash: {block["hash"]}\n' +
            f'previous_hash: {block["previous_hash"]}\n' +
            f'timestamp: {block["timestamp"]}\n' +
            f'nonce: {block["nonce"]}\n'
        ) for block in self.chain])
