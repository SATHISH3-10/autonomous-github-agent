# erc8004_identity.py
import json
import os
from web3 import Web3

AGENT_FILE = "agent_identity.json"

def create_agent_identity(agent_name, operator_wallet):
    """Create a new agent identity"""
    agent = {
        "agent_name": agent_name,
        "operator_wallet": operator_wallet,
        # Example ERC-8004 identity, can be a new wallet or derived address
        "agent_address": Web3.toChecksumAddress(Web3.keccak(text=agent_name).hex()[:42])
    }
    with open(AGENT_FILE, "w") as f:
        json.dump(agent, f, indent=4)
    return agent

def load_agent_identity():
    """Load agent identity if exists"""
    if os.path.exists(AGENT_FILE):
        with open(AGENT_FILE) as f:
            return json.load(f)
    return None

def register_agent_onchain(agent):
    """Simulate on-chain registration"""
    print(f"Registering agent {agent['agent_name']} with ERC-8004 address {agent['agent_address']}")
    # Here you could add web3.py code to submit a transaction
    return True