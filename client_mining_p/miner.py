import hashlib
import requests
import json
import sys
import time


def search_proof(block):
    
    block_string = json.dumps(block, sort_keys=Trur).encode()
    
    proof = 0

    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof

def valid_proof(block_string, proof):
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:3] == "000"

if __name__ == '__main__':
    # What node are we interacting with?

    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    print("Started to mine")
    t_start = time.process_time()

    try:
        while True:
            res = requests.get(node + '/last_block')
            res = json.loads(res.content)

            proof = search_proof(res['last_block'])
            print(f"proof {proof}")

            res = requests.post(node + "/mine", {"proof": proof})
            res_content = json.loads(res.content)

            if res.status_code == 200 and res_content['message'] == "New Block Forged":
                coins_mined += 1
                print(f"{coins_mined} coins mined")
            else:
                print(res_content['message'])

    except:
        print("Finish Mining")
        t_stop = time.process_time()
        print("Time Mining: %.1f seconds" % ((t_stop-t_start)))
    
      