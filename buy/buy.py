import json
import base64
from dotenv import load_dotenv
import requests
import os
import base58
import logging
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction  # Use versioned transaction
from solders import message
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned
from solana.rpc.commitment import Processed

# Load environment variables
load_dotenv()
RPC_NODE = os.getenv("RPC_NODE")

def load_wallet() -> Keypair:
    """Load the private key from the environment variable (base58-encoded)."""
    private_key_str = os.getenv("PRIVATE_KEY")
    if not private_key_str:
        raise ValueError("PRIVATE_KEY environment variable not set.")
    try:
        private_key_bytes = base58.b58decode(private_key_str)
    except Exception as e:
        raise ValueError("Failed to decode PRIVATE_KEY") from e
    wallet = Keypair.from_bytes(private_key_bytes)
    return wallet

def buy_memecoin(sol_amount: float, memecoin_mint: str, wallet: Keypair) -> str:
    """
    Buys a memecoin token using SOL via the Jupiter Swap API on Solana.
    
    Parameters:
      - sol_amount (float): Amount of SOL to spend.
      - memecoin_mint (str): The token mint address of the memecoin.
      - wallet (Keypair): Your wallet used to sign and send the transaction.
    
    Returns:
      - str: Transaction signature if successful.
    """
    try:
        # Convert SOL to lamports (1 SOL = 1e9 lamports)
        lamports = int(sol_amount * 1e9)
        sol_mint = "So11111111111111111111111111111111111111112"  # SOL mint address

        # --- Step 1: Get Quote from Jupiter (v6 endpoint) ---
        quote_url = "https://quote-api.jup.ag/v6/quote"
        quote_params = {
            "inputMint": sol_mint,
            "outputMint": memecoin_mint,
            "amount": str(lamports),
            "slippageBps": "1000"  # 10% slippage tolerance
        }
        quote_resp = requests.get(quote_url, params=quote_params)
        if quote_resp.status_code != 200:
            raise Exception(f"Quote API failed with status {quote_resp.status_code}: {quote_resp.text}")
        quote_response = quote_resp.json()
        logging.info(f"Quote response: {quote_response}")

        # --- Step 2: Build Swap Transaction via Jupiter Swap API (v6 endpoint) ---
        swap_url = "https://quote-api.jup.ag/v6/swap"
        swap_payload = {
            "quoteResponse": quote_response,
            "userPublicKey": str(wallet.pubkey()),
            "wrapUnwrapSOL": True
        }
        headers = {"Content-Type": "application/json"}
        swap_resp = requests.post(swap_url, headers=headers, data=json.dumps(swap_payload))
        if swap_resp.status_code != 200:
            raise Exception(f"Swap API failed with status {swap_resp.status_code}: {swap_resp.text}")
        swap_response = swap_resp.json()
        if "swapTransaction" not in swap_response:
            raise Exception("Swap response does not contain swapTransaction.")
        swap_tx_base64 = swap_response["swapTransaction"]

        raw_transaction = VersionedTransaction.from_bytes(
            base64.b64decode(swap_tx_base64)
        )

        # --- Step 3: Deserialize & Sign the Transaction ---
        signature = wallet.sign_message(to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(raw_transaction.message, [signature])
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)

        # --- Step 4: Send the Transaction ---
        client = Client(RPC_NODE)

        send_resp = client.send_raw_transaction(
            txn=bytes(signed_txn),
            opts=opts
        )
        transaction_id = json.loads(send_resp.to_json())['result']
        print(f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")
        return transaction_id

    except Exception as e:
        print(f"Error in buy_memecoin: {e}")
        raise

if __name__ == "__main__":
    # Replace MEME_TOKEN_MINT with the actual memecoin token mint address.
    MEME_TOKEN_MINT = "hTRDn7zE5tDHRnjj6Qms2WG1zEGv9ii6AiwfgbFpump"
    SOL_AMOUNT = 0.0001  # Amount of SOL to spend
    try:
        wallet = load_wallet()
        print("Loaded wallet with public key:", wallet.pubkey())
        tx_signature = buy_memecoin(SOL_AMOUNT, MEME_TOKEN_MINT, wallet)
        print(f"Transaction successful! Signature: {tx_signature}")
    except Exception as e:
        print("Swap failed:", e)
