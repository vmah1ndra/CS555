python3 server.py
python3 client.py (4 separate times) - Enter 'player' for 3 clients and 'client' for 1 client. The order does not matter, as the server will wait for 3 players to connect, then generate the El Gamal and MPC, and then send the information to the client.

Algorand: We use the escrow contract to form the transaction for 10000 ALGO.  
This is first built using `./build.sh contracts.escrow.step_01` in a git bash shell while in the project/ folder and in a venv environment.  
Next, we `cd ../sandbox/`. 
Use `./sandbox up` to start the Docker accounts. 
Use `./sandbox enter algod` to be able to pass functions. 
Use `goal account list` to get a list of possible account numbers that can be used here. 
Use `ONE=<account number>` and replace <account number> with a copied online or offline account in the above list. 
Use `goal app create --creator=$ONE --approval-prog /data/build/create.teal --clear-prog /data/build/clear.teal --global-byteslices 3 --global-ints 1 --local-byteslices 0 --local-ints 0` to create app with index <index_number> (note down this number). 
Use `goal app call --app-id <index_number> --from $ONE` with the right input arguments as in escrow/step_01.py: owner address, beneficiary address, hashed_secret, unlock at round (timeout period). This carries out the transaction. 
If the right information (key to decrypt (m1*m2)+m3 mod p) is given in time, the transaction carries through. 
Use `exit` to exit algod. 
Use `./sandbox down` to close Docker. 
