from socket import *
import pickle 
serverPort = 25000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    #get a confirmed transaction from full node
    confirmedTx = pickle.loads(message)
    print(confirmedTx)
    for trans in confirmedTx:
        print(trans)
        tx = trans.split(':')
        print(tx)
        payer = tx[0]
        payee = tx[1]
        amount = int(tx[2])
        print('payer ', payer[0:1], ' account ' , payer[7:8])
        print('payee ', payee[0:1], ' account ' , payee[7:8])
        print('amount ', amount)
        #this account is the payer
        if payer[0:1] == 'B':
            print('i am the payer')
            unconfirmedTxs = open('Unconfirmed_T.txt').read().splitlines()
            i = 0
            for unconfirmedTx in unconfirmedTxs:
                unconfirmedTx = unconfirmedTx.rstrip()
                if trans == unconfirmedTx:
                    print('trancastions match')
                    #reduce confirmed balance by tx amount + tx fee
                    account_balance = open('balance_B.txt').read().splitlines()               
                    print(account_balance)
                    balance_A1 = account_balance[0].split(':')
                    balance_A2 = account_balance[1].split(':')
                    if payer[7:8] == '1':
                        print('account 1')
                        balance_of_A1 = balance_A1[2]
                        print(balance_of_A1)
                        balance_of_A1 = hex(int(balance_of_A1, 16) - amount -2)
                        print(balance_of_A1)
                        balance_A1[2] = balance_of_A1
                        print(balance_A1)
                        with open('balance_B.txt', 'w') as f:
                            f.write(balance_A1[0] + ':' + balance_A1[1] + ':' + balance_A1[2] + '\n')
                            f.write(balance_A2[0] + ':' + balance_A2[1] + ':' + balance_A2[2])
                    elif payer[7:8] == '2':
                        print('account 2')
                        balance_of_A2 = balance_A2[2]
                        print(balance_of_A2)
                        balance_of_A2 = hex(int(balance_of_A2, 16) - amount -2)
                        print(balance_of_A2)
                        balance_A2[2] = balance_of_A2
                        print(balance_A2)
                        with open('balance_B.txt', 'w') as f:
                            f.write(balance_A1[0] + ':' + balance_A1[1] + ':' + balance_A1[2] + '\n')
                            f.write(balance_A2[0] + ':' + balance_A2[1] + ':' + balance_A2[2])

                    #remove this tx from unconfirmed tx
                    del unconfirmedTxs[i]
                    uTxs = open('Unconfirmed_T.txt', 'w')
                    for line in unconfirmedTxs:
                        uTxs.write(line + '\n')
                        print('writing uct ', line)
                    uTxs.close()

                    #append this tx to confirmed tx
                    confirmedTxs = open('Confirmed.txt', 'a')
                    confirmedTxs.write(trans + '\n')
                    print('writing ct ', trans)
                    confirmedTxs.close()

                    #break when we find a tx match 
                    break
                i+=1

        #this account is the payee
        elif payee[0:1]  == 'B':
            print('i am the payee')

            #add tx amount to confirmed and unconfirmed balance
            account_balance = open('balance_B.txt').read().splitlines()             
            balance_A1 = account_balance[0].split(':')
            balance_A2 = account_balance[1].split(':')
            if payee[7:8] == '1':
                #confirmed balance
                c_balance_of_A1 = balance_A1[2]
                c_balance_of_A1 = hex(int(c_balance_of_A1, 16) + amount)
                balance_A1[2] = c_balance_of_A1
                #unconfirmed balance
                u_balance_of_A1 = balance_A1[1]
                u_balance_of_A1 = hex(int(u_balance_of_A1, 16) + amount)
                balance_A1[1] = u_balance_of_A1
                with open('balance_B.txt', 'w') as f:
                    f.write(balance_A1[0] + ':' + balance_A1[1] + ':' + balance_A1[2] + '\n')
                    f.write(balance_A2[0] + ':' + balance_A2[1] + ':' + balance_A2[2])
            elif payee[7:8] == '2':
                #confirmed balance
                c_balance_of_A2 = balance_A2[2]
                c_balance_of_A2 = hex(int(c_balance_of_A2, 16) + amount)
                balance_A2[2] = c_balance_of_A2
                #unconfirmed balance
                u_balance_of_A2 = balance_A2[1]
                u_balance_of_A2 = hex(int(u_balance_of_A2, 16) + amount)
                balance_A2[1] = u_balance_of_A2
                with open('balance_B.txt', 'w') as f:
                    f.write(balance_A1[0] + ':' + balance_A1[1] + ':' + balance_A1[2] + '\n')
                    f.write(balance_A2[0] + ':' + balance_A2[1] + ':' + balance_A2[2])


            #append this tx to confirmed tx
            confirmedTxs = open('Confirmed.txt', 'a')
            confirmedTxs.write(trans + '\n')
            print('writing ', trans)
            confirmedTxs.close()
