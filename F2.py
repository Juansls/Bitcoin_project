from socket import *
import pickle, hashlib

# initialize global variables
balance = 0  # full nodes balance
Tx_fees = 8     # Tax for mining a block
mining_fee = 30     # Fee for mining a block
# block_number variable is used for two things
# 1. Keeping track of each new block
# 2. Will decide which full node will mine the next block
block_number = 1

# A function to connect to other files
# It is used to send data between full nodes and clients
def sendTransaction(Tx, port):
    serverName = 'localhost'
    serverPort = port
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = pickle.dumps(Tx)
    clientSocket.sendto(message, (serverName, serverPort))
    clientSocket.close()

# Function to check if Temp_F1.txt is full with 4 transactions
def is_temp_file_full():
    counter = 0
    with open('Temp_F2.txt', 'r') as f:
        content = f.readlines()
        for i in content:
            if i:
                counter += 1
    if counter == 4:
        return True     # 4 transactions in the file. Ready for mining
    return False

def find_nonce(prev, merkle_root):
    hashHandler = hashlib.sha256()
    nonce = 0
    while True:
        block_header = str(nonce) + prev + merkle_root
        hashHandler.update(block_header.encode('utf-8'))
        hashValue = hashHandler.hexdigest()
        print('nonce:{0},hash:{1}'.format(nonce, hashValue))
        nounceFound = True
        for i in range(4):
            if hashValue[i] != '0':
                nounceFound = False
        if nounceFound:
            break
        else:
            nonce = nonce + 1
    # Create a file to store the hasValue
    # This will be use to easily get the previous block hash
    with open('blockchain_hash.txt', 'a') as f:
        f.write(hashValue)
        f.write('\n')
    return nonce

def create_block():
    with open('Temp_F2.txt', 'r') as f:
        Tx = f.readlines()
    # Remove \n at the end of each transaction
    Tx = [x.strip() for x in Tx]

    # Hash each Tx to create the leaves of the Merkle tree
    hash_A = hash(Tx[0])
    hash_B = hash(Tx[1])
    hash_C = hash(Tx[2])
    hash_D = hash(Tx[3])

    # Concatenate two hashes and hash the result
    hash_AB = hash(hash_A + hash_B)
    hash_CD = hash(hash_C + hash_D)

    # Concatenate the two new hashes and hash the result to get the Merkle root
    hash_ABCD = str(hash(hash_AB + hash_CD))

    # Calculate the SHA256 hash of hash_ABCD and return the result
    m = hashlib.sha256()
    m.update(hash_ABCD.encode('utf-8'))
    return m.hexdigest()

def create_blockchain(block, nonce, last_block, merkle_root):
    # Get the 4 transaction in order to create the blockchain
    with open('Temp_F2.txt', 'r') as f:
        lines = f.readlines()

    # Since lines will have a string with no spaces e.g
    # we need to split it. The first 8 characters contains the Payers account
    # The second 8 numbers contains the Payee account. Lastly, the last characters
    # contain the amount of bitcoins that are been transfer.
    n = 8
    line_one = lines[0]
    Tx_one = [(line_one[i:i + n]) for i in range(0, len(line_one), n)]
    line_two = lines[1]
    Tx_two = [(line_two[i:i + n]) for i in range(0, len(line_two), n)]
    line_three = lines[2]
    Tx_three = [(line_three[i:i + n]) for i in range(0, len(line_three), n)]
    line_four = lines[3]
    Tx_four = [(line_four[i:i + n]) for i in range(0, len(line_four), n)]

    # Strip the new line('\n) at the end of each transaction
    Tx_one[2] = Tx_one[2].strip('\n')
    Tx_two[2] = Tx_two[2].strip('\n')
    Tx_three[2] = Tx_three[2].strip('\n')
    Tx_four[2] = Tx_four[2].strip('\n')

    # Send the 4 Tx to it's client. The purpose is to let the client
    # know these Tx are confirmed. This will be in the form of A00000001:B000000001:100
    Tx_list = [None,None,None,None]
    Tx_list[0] = Tx_one[0] + ':' + Tx_one[1] + ':' + Tx_one[2]
    Tx_list[1] = Tx_two[0] + ':' + Tx_two[1] + ':' + Tx_two[2]
    Tx_list[2] = Tx_three[0] + ':' + Tx_three[1] + ':' + Tx_three[2]
    Tx_list[3] = Tx_four[0] + ':' + Tx_four[1] + ':' + Tx_four[2]
    sendTransaction(Tx_list,25000)

    # Concatenate the header and body fields and store the block as a 116-byte hex
    # Save new block into blockchain.txt
    with open('blockchain_F2.txt', 'a') as f:
        f.write('BLock: ' + str(block) + '\n')
        f.write('Nonce (4-byte): ' + str(nonce) + '\n')
        f.write('Last Block hash (32-byte): ' + last_block + '\n')
        f.write('Merkle root (32-byte): ' + merkle_root + '\n')
        f.write('Tx1 (12-byte):' + Tx_one[0] + ' paid ' + Tx_one[1] + ' the amount of ' + Tx_one[2] + ' BC.' + '\n')
        f.write('Tx2 (12-byte):' + Tx_two[0] + ' paid ' + Tx_two[1] + ' the amount of ' + Tx_two[2] + ' BC.' + '\n')
        f.write('Tx3 (12-byte):' + Tx_three[0] + ' paid ' + Tx_three[1] + ' the amount of ' + Tx_three[2] + ' BC.' + '\n')
        f.write('Tx4 (12-byte):' + Tx_four[0] + ' paid ' + Tx_four[1] + ' the amount of ' + Tx_four[2] + ' BC.' + '\n')
    global block_number
    # Also send the block to the other full node
    if block_number % 2 == 0:
         block_chain = [block, nonce, last_block,merkle_root]
         sendTransaction(block_chain,10000)
         # empty Temp_F1 file since all four transactions have been mine
         with open('Temp_F2.txt', 'r+') as f:
                f.truncate(0)

    block_number += 1  # increment block number

def mine(merkle_root):
    # Add mining fee (30 BC) and the total of Tx_fee(8 BC)
    global balance
    global block_number
    balance += mining_fee + Tx_fees
    last_block = ' '
    if(block_number == 1): # First block
        for i in range(32):
            last_block += '0' # previous block is 32 0's
        with open('blockchain_hash.txt','a') as f:
            f.write(last_block + '\n')
    else:
        # Get last block hash
        with open('blockchain_hash.txt', 'r') as f:
            block_chain = f.readlines()
            last_block = block_chain[block_number-1].strip('\n')

    # Find nonce for the block
    nonce = find_nonce(last_block, merkle_root)

    # Create blockchain
    create_blockchain(block_number, nonce, last_block, merkle_root)

def TTT_instructions(Tx):
    # Concatenate Tx into one string
    # This will upload the new Tx to the tmp file nicely
    global block_number
    new_Tx = Tx[0] + Tx[1] + str(Tx[2])
    with open('Temp_F2.txt', 'a') as f:
        f.write(new_Tx + '\n')
        # If the requester is the full node's client, send the Tx to the other full node as well.
    if Tx[3] == 'client_B':
       sendTransaction(Tx, 10000)


    # Check if the number of Tx in Temp_T.txt has reached 4
    if is_temp_file_full():

        if(block_number%2==1):
            return      # It is other full node's turn to mine, exit

        # Create block
        merkle_root = create_block()

        # Mine new block
        mine(merkle_root)


serverPort = 20000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
while True:
    message, clientAddress = serverSocket.recvfrom(4096)
    Tx = pickle.loads(message)

    # Check if the requester is the client or the other full node

    # If Tx is client B then call TTT_instructions and pass the new Tx
    if Tx[3] == 'client_B': # Request from client A
        TTT_instructions(Tx)
    # If Tx is client A then also call TTT_instructions and pass the Tx
    elif Tx[3] == 'client_A':
        TTT_instructions(Tx)
    # If message is a block, then append block to the blockchain.txt file
    # Remove the 4 Tx of the block from Temp_T.txt file
    # Send the 4 Tx of the block to it's client to confirm transactions
    else:
        # Create blockchain
        # This function will also send the 4 Tx to clients to confirm the transactions
        create_blockchain(Tx[0],Tx[1],Tx[2],Tx[3])
        # empty Temp_F1 file since all four transactions have been mine
        with open('Temp_F2.txt', 'r+') as f:
             f.truncate(0)






