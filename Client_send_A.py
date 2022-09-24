
# //////////////////////////////////////////////////////////////////////////////////
# //         CS 436 - Project: Network programming to implement Bitcoin           //
# //                                                                              //
# //          Authors: Juan Solis Melgar                                          //
# //          Course: CS 436                                                      //
# //          Date: April 9, 2021                                                 //
# //          Files: Client_send_A.py, Client_send_B.py, F1.py, F2.py,            //
# //                   Client_receive_A.py, Client_receive_B.py                   //
# //          Description: In this project we implement a simplified Bitcoin      //
# //          system. In our project there are two clients (A and B) and each     //
# //          client has two accounts. Each client connects to one full node.     //
# //          F1 and F2 are two full nodes.                                       //
# //                                                                              //
# //                                                                              //
# //////////////////////////////////////////////////////////////////////////////////

from socket import*
import pickle


# initialize clients A1 and A2 with account name and balance
# Store clients info into a file name balance.txt (Account#:Unconfirmed_balance:Confirmed_balance)
# e.g A0000001:0x000003E8:0x000003E8
# place their information into a txt file
clientAccount =['A0000001','A0000002']
clientBalance = ['0x000003E8','0x000003E8']
with open('balance.txt', 'w') as w:
    w.write(clientAccount[0] + ':' + clientBalance[0] + ':' + clientBalance[0] + '\n')
    w.write(clientAccount[1] + ':' + clientBalance[1] + ':' + clientBalance[1] + '\n')

# convert a hex value to a decimal
def convert_hex_toDecimal(hexVal):
    value = int(hexVal, 16)
    return value
# convert decimal value to it's hex representation
def convert_decimal_toHex(decimalVal):
    value = '0x{0:0{1}X}'.format(decimalVal,8) # get hex value
    return value

# function to return the current unconfirmed balance
def get_balance(account):

    index = int(account) - 1
    balance = clientBalance[index]
    # convert balance to a decimal value
    balance = convert_hex_toDecimal(balance)
    return int(balance)  # return balance

# function to send a transaction to the full node
# The input is a transaction that will be sent to F1
def sendTransaction(Tx):
    # Create connection to F1
    serverName = 'localhost'
    serverPort = 10000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = pickle.dumps(Tx)
    clientSocket.sendto(message, (serverName, serverPort))
    clientSocket.close()

def unconfirmed_balance(account_number, Tx_amount):

    # account_number has an input of either a 1 or 2
    # however, our index can only be 0 or 1
    # index at 0 = Account 1
    # index at 1 = Account 2
    index = int(account_number) - 1

    # open balance.txt which holds the unconfirmed balance
    with open('balance.txt', 'r') as f:
        account_balance = f.readlines()
    # We need to split the data to get only the unconfirmed balance
    get_only_balance = account_balance[index].split(':')
    # Convert balance to an integer value so we can compare if balance is less than (Tx_amount + Tx_fee)
    balance = convert_hex_toDecimal(get_only_balance[1])
    # Check if new transaction will not exceed unconfirmed balance
    Tx_fee = 32
    if balance >= (Tx_amount + Tx_fee):
          return True # Success
    return False    # Insufficient funds


while True:
    print('Please make a choice from the following selection:')
    print('1. Enter a new transaction.')
    print('2. The current balance for each account.')
    print('3. Print the unconfirmed transactions.')
    print('4. Print the confirmed transactions.')
    print('5. Print the blockchain.')
    print('6. Exit.')
    userInput = int(input('Choice: '))

    # Go through a list of cases
    # First case: new transaction
    if userInput == 1:
        print('Select the Payer:')
        print('1. A0000001')
        print('2. A0000002')
        accountInput = int(input('Choice: '))
        payer = ' '
        payee = ' '
        # will use conditional statements to get only the
        # hexadecimal of the payer account
        if accountInput == 1:
            payer = 'A0000001'
        elif accountInput == 2:
            payer = 'A0000002'
        print('Select the Payee:')
        print('1. B0000001')
        print('2. B0000002')
        payeeInput = int(input('Choice:'))
        # get hexadecimal of payee account
        if payeeInput == 1:
            payee = 'B0000001'
        elif payeeInput == 2:
            payee = 'B0000002'
        print('Enter the amount of payment in decimal.')
        amount = int(input())
        # check if there is sufficient funds in the account
        # if there is sufficient funds the process the transaction
        # else print to the user 'Insufficient funds.'
        confirm = unconfirmed_balance(accountInput, amount)
        if confirm:
            # There is sufficient funds
            # Create list to store all of the client information (payer, payee, amount, client)
            Tx = [payer,payee,amount,'client_A']
            print('Tx: ' + payer + ' pays ' + payee + ' the amount of ' + str(amount) + ' BC.')
            with open('Unconfirmed_T.txt', 'a') as f:
                f.write(payer+':'+payee+':'+ str(amount)+'\n')

            # Send a new transaction to the full node F1
            sendTransaction(Tx)
        else:    # Not enough funds in unconfirmed balance
            print('Insufficient funds.')

    # Second Case: Print current balance for each account
    elif userInput == 2:
        with open('balance.txt' , 'r') as f:
            account_balance = f.readlines() # Get current balance for each account from file
        balance_A1 = account_balance[0].split(':')  # first balance
        balance_A2 = account_balance[1].split(':')  # second balance
        balance_of_A1 = convert_hex_toDecimal(balance_A1[2])
        balance_of_A2 = convert_hex_toDecimal(balance_A2[2])
        print(clientAccount[0] + ' has a balance of ' + str(balance_of_A1) + ' BC')
        print(clientAccount[1] + ' has a balance of ' + str(balance_of_A2) + ' BC')

    # Third case: print unconfirmed transactions
    elif userInput == 3:
        with open('Unconfirmed_T.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            print("{}".format(line.strip()))

    # Fourth Case: print confirmed transactions
    elif userInput == 4:
        with open('Confirmed.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            print("{}".format(line.strip()))

    # Fifth Case: Print blockchain
    elif userInput == 5:
        with open('blockchain.txt', 'r') as f:
            block_chain = f.read().splitlines()
        for line in block_chain:
            print(line)
    # Sixth Case: Exit
    elif userInput == 6:
        break


