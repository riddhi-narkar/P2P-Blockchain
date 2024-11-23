import sys
import os
from typing import Tuple, Set
from PyInquirer import prompt
# local
from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction


def use_blockchain(blockchain: Blockchain, current_address: Tuple[str, int], peers: Set[Tuple[str, int]]):

    questions = {
        'main': {
            'type': 'list',
            'name': 'main',
            'message': f'Actions:',
            'choices': ['Refresh', 'Show peers', 'Show chain', 'New transaction', 'Mine block', 'Quit'],
        },
        'transaction': {
            'type': 'list',
            'name': 'transaction',
            'message': 'Whom to send?',
            'choices': [str(p) for p in peers]
        },
        'amount': {
            'type': 'input',
            'name': 'amount',
            'message': 'What amount would you like to send?'
        }
    }

    print(f'\nAddress: {current_address}')
    print(f'Balance: {blockchain.get_balance(current_address)}')
    answer = prompt(questions['main'])
    # REFRESH
    if answer['main'] == 'Refresh':
        clearconsole()
        return
    # SHOW PEERS
    elif answer['main'] == 'Show peers':
        if len(peers) == 0:
            print('No peers in the network :(')
        else:
            [print(str(p)) for p in peers]
        input('\nPress [ Enter ] to continue')
        clearconsole()
    # GET CHAIN
    # ______________________________________________________

    # elif answer['main'] == 'Show chain':
    #     print(blockchain.__str__)
    #     input('\nPress [ Enter ] to continue')
    #     clearconsole()
    # ______________________________________________________
    # elif answer['main'] == 'Show chain':
    #     print("\nBlockchain:")
    #     # print(blockchain.__str__())  # Display the chain
    #     print(blockchain)  # Display the chain

    #     is_valid, message = blockchain.validate_chain()  # Check validation
    #     if is_valid:
    #         print("\n[Success] Blockchain is valid.")
    #     else:
    #         print(f"\n[Error] Blockchain validation failed: {message}")
    #     input('\nPress [ Enter ] to continue')
    #     clearconsole()
    # ______________________________________________________
    elif answer['main'] == 'Show chain':
        print(blockchain)  # Display the chain
        # if blockchain.validate_chain():  # Assuming validate_chain is a method for chain validation
        if blockchain.is_valid()[1]:
            print("\nChain is valid.")
            print(f"Time to validate chain (nanoseconds): {blockchain.is_valid()[0]}")
        else:
            print("\nChain is invalid!")
            print(f"Time to validate chain (nanoseconds): {blockchain.is_valid()[0]}")
        input('\nPress [ Enter ] to continue')
        clearconsole()

    # NEW TRANSACTION
    elif answer['main'] == 'New transaction':
        try:
            answer = prompt(questions['transaction'])
            recipient = answer['transaction'].split(', ')
            recipient = (recipient[0][2: -1], int(recipient[1][0: -1]))
            answer = prompt(questions['amount'])
            if int(answer['amount']) < 1:
                print(f"You can\'t send {answer['amount']} coins")
            elif blockchain.get_balance(current_address) >= int(answer['amount']):
                t = Transaction(current_address, recipient, int(answer['amount']))
                blockchain.new_transaction(t)
            else:
                print('Not enough coins :(')
            input('\nPress [ Enter ] to continue')
            clearconsole()
        except IndexError:
            # This error raises when we get an empty set of peers
            print('No peers in the network :(')
            input('\nPress [ Enter ] to continue')
            clearconsole()
    # MINE BLOCK
    elif answer['main'] == 'Mine block':
        time = blockchain.add_block(current_address)
        print(f"Time to add block (nanoseconds): {time}")
        clearconsole()
    # QUIT
    elif answer['main'] == 'Quit':
        # Catch and handle this exception out of this function
        raise KeyboardInterrupt


def clearconsole():
    """
    Clear the console. Thanks stackoverflow.
    """
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
