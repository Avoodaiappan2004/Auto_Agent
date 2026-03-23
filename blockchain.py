import json
import os
import time

CHAIN_FILE = "chain.json"

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def record_transaction(action, data):
    chain = load_chain()

    tx = {
        "timestamp": time.time(),
        "action": action,
        "data": data
    }

    chain.append(tx)
    save_chain(chain)

    return tx


# 🔥 TRUST SYSTEM
TRUST_FILE = "trust.json"

def load_trust():
    if not os.path.exists(TRUST_FILE):
        return {"score": 0}
    with open(TRUST_FILE, "r") as f:
        return json.load(f)

def update_trust(success=True):
    trust = load_trust()

    if success:
        trust["score"] += 1
    else:
        trust["score"] -= 1

    with open(TRUST_FILE, "w") as f:
        json.dump(trust, f, indent=2)

    return trust["score"]