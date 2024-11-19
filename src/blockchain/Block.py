from hashlib import sha256
from datetime import datetime
from typing import List


class Block:
    def __init__(self, transactions: List, previous_hash: str):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.nonce: int = 0

    @property
    def serialized(self) -> dict:
        return {
            'transactions': self.transactions,
            'hash': self.get_hash(),
            'previous_hash': self.previous_hash,
            'timestamp': str(self.timestamp),
            'nonce': str(self.nonce),
        }

    def get_hash(self) -> str:
        return sha256(
            (str(self.transactions) + self.previous_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()

    # def mine(self, difficulty: int):
    #     # generate amount of zeros based on difficulty
    #     zeros = ''.join(['0' for o in range(0, difficulty)])
    #     # increment nonce until first symbols of hash are not zeros
    #     while self.get_hash()[0: difficulty] != zeros:
    #         self.nonce += 1

    # def mine(self, difficulty: int):
    #     # zeros = '0000'  # Fixed string of 4 zeros
    #     zeros = '0' * difficulty
    #     while self.get_hash()[0: difficulty] != zeros:
    #         self.nonce += 1
    #     self.hash = self.get_hash()
    #     assert self.get_hash()[0: difficulty] == zeros, "Mining failed to produce valid proof-of-work"

    # def mine(self, difficulty: int):
    #     """
    #     Mines the block by finding a hash with the specified number of leading zeros (difficulty).
    #     Updates the block's hash upon successful mining.
    #     """
    #     assert difficulty > 0, "Difficulty must be a positive integer."

    #     # Generate the required prefix based on the difficulty
    #     target_prefix = '0' * difficulty

    #     # Mining loop: increment the nonce until the hash meets the target
    #     while True:
    #         # Compute the hash with the current nonce
    #         current_hash = self.get_hash()

    #         # Check if the hash meets the difficulty requirement
    #         if current_hash[:difficulty] == target_prefix:
    #             self.hash = current_hash  # Save the valid hash to the block
    #             print(f"Block mined successfully with nonce {self.nonce}. Hash: {self.hash}")
    #             break

    #         self.nonce += 1

    #     # Ensure the final mined hash is valid
    #     assert self.hash[:difficulty] == target_prefix, "Mining failed to produce a valid hash."

    def mine(self, difficulty: int):
        """
        Mines the block by finding a hash with the specified number of leading zeros (difficulty).
        Updates the block's hash upon successful mining.
        """
        assert difficulty > 0, "Difficulty must be a positive integer."

        # Generate the required prefix based on the difficulty
        target_prefix = '0' * difficulty

        # Mining loop: increment the nonce until the hash meets the target
        while True:
            # Compute the hash with the current nonce
            current_hash = self.get_hash()  # Ensure this method properly accounts for the nonce

            # Check if the hash meets the difficulty requirement
            if current_hash[:difficulty] == target_prefix:
                self.hash = current_hash  # Save the valid hash to the block
                print(f"Block mined successfully with nonce {self.nonce}. Hash: {self.hash}")
                break

            self.nonce += 1

        # Ensure the final mined hash is valid
        assert self.hash[:difficulty] == target_prefix, "Mining failed to produce a valid hash."
