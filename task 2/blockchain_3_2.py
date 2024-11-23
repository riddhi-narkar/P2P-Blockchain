import hashlib
import time

class Block:
    def __init__(self, index, transactions, fees, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # List of transactions
        self.fees = fees  # List of transaction fees
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.hash_current()

    def hash_current(self):
        current_data = f"{self.index}{self.timestamp}{self.transactions}{self.fees}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(current_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.mempool = []  # Unconfirmed transactions list

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], [0], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_to_mempool(self, transaction, fee, dependent=False):
        self.mempool.append({"transaction": transaction, "fee": fee, "dependent": dependent})

    def mine_transactions(self):
        if not self.mempool:
            print("\nNo transactions to mine.")
            return

        # Sort transactions in the mempool by fee (highest first)
        self.mempool.sort(key=lambda x: x["fee"], reverse=True)
        
        transactions_to_mine = []
        fees_to_mine = []
        mined_transactions = []

        for tx in self.mempool:
            if tx["dependent"]:
                print(f"\nDetected dependent (malicious) transaction: '{tx['transaction']}'. Blocking victim's transaction.")
                print("Mining stalled until this transaction is removed or processed.")
                return  # Simulate pinning by not mining any block.
            else:
                transactions_to_mine.append(tx["transaction"])
                fees_to_mine.append(tx["fee"])
                mined_transactions.append(tx)

        # Create and mine the block
        new_block = Block(len(self.chain), transactions_to_mine, fees_to_mine, self.get_latest_block().hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"\nBlock {new_block.index} mined with transaction(s): {transactions_to_mine}")
        
        # Remove mined transactions from mempool
        self.mempool = [tx for tx in self.mempool if tx not in mined_transactions]

    def proof_of_work(self, block):
        block.nonce = 0
        target = '0' * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.hash_current()

    def display_mempool(self):
        print("\nCurrent Mempool:")
        for i, tx in enumerate(self.mempool, 1):
            status = "DEPENDENT" if tx["dependent"] else "Normal"
            print(f"{i}. Transaction: {tx['transaction']}, Fee: {tx['fee']}, Status: {status}")

    def display_chain(self):
        print("\nBlockchain:")
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Transactions: {block.transactions}")
            print(f"  Fees: {block.fees}")
            print(f"  Total Fees: {sum(block.fees)}")
            print(f"  Hash: {block.hash}")
            print("-------------------------")

def simulate_pinning_attack(blockchain):
    print("\n--- Simulating Transaction Pinning Attack ---")
    
    # Victim's transaction
    victim_tx = input("Enter the victim's transaction (legitimate): ")
    victim_fee = int(input("Enter the fee for the victim's transaction: "))

    # Add the victim's transaction to the mempool
    blockchain.add_to_mempool(victim_tx, victim_fee)

    # Malicious dependent transaction
    dependent_tx = f"DEPENDENT on {victim_tx}"
    dependent_fee = int(input("Enter the fee for the dependent malicious transaction: "))

    # Add the dependent transaction to the mempool (mark as dependent)
    blockchain.add_to_mempool(dependent_tx, dependent_fee, dependent=True)
    
    # Display mempool status
    blockchain.display_mempool()

    # Simulate mining attempt
    print("\nAttempting to mine transactions...")
    blockchain.mine_transactions()

    # Display remaining mempool state
    blockchain.display_mempool()

def main():
    blockchain_instance = Blockchain()
    while True:
        print("\n1. Simulate Transaction Pinning Attack")
        print("2. View Blockchain")
        print("3. Mine Pending Transactions")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            simulate_pinning_attack(blockchain_instance)
        elif choice == '2':
            blockchain_instance.display_chain()
        elif choice == '3':
            blockchain_instance.mine_transactions()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
