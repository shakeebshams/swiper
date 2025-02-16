import subprocess
import requests
import time
import json
import datetime
import logging
import os
from supabase import create_client
from dotenv import load_dotenv
import uuid
import pytz

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
eastern_tz = pytz.timezone('US/Eastern')

def buy_token_placeholder(token_details):
    """
    Placeholder function for buying a token.
    In a real implementation, this would contain the logic to execute a buy order.

    Args:
        token_details (dict): Details of the token to buy.
    """
    complete_flag = False

    token_address = token_details.get('address')
    creation_timestamp_unix = token_details.get('pool_creation_timestamp')

    # Check if token already exists in the database
    existing_token_check = supabase.table("positions").select("*").eq("token_address", token_address).execute()
    if existing_token_check.data:
        logging.info(f"Token with address {token_address} already exists in the database. Skipping buy.")
        return False  # Indicate buy was skipped

    # Check if token is less than 60 seconds old
    if creation_timestamp_unix: # Check if timestamp exists before proceeding
        token_creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp_unix)
        time_difference = datetime.datetime.now() - token_creation_datetime
        if time_difference.total_seconds() >= 60:
            logging.info(f"Token is older than 60 seconds. Token creation time: {token_creation_datetime}. Skipping buy.")
            return False  # Indicate buy was skipped
        else:
            logging.info(f"Token is less than 60 seconds old. Proceeding with buy.")
            complete_flag = True # Proceed with buy if checks pass
    else:
        logging.warning("Token creation timestamp is missing. Proceeding with buy without age check.")
        complete_flag = True # Proceed with buy if timestamp is missing (with warning)


    # In a real implementation, add buy order logic here
    if complete_flag:
        log_order(token_details)
        # buy function
        return True # Indicate buy was successful (placeholder)
    else:
        return False # Indicate buy was skipped due to checks

def log_order(token_details):
    data_to_insert = {
        "id": str(uuid.uuid4()),
        "token_address": token_details.get('address'),
        "token_symbol": token_details.get('symbol'),
        "token_creation_timestamp": datetime.datetime.fromtimestamp(token_details.get('pool_creation_timestamp')).isoformat() if token_details.get('pool_creation_timestamp') else None, # Handle potential missing timestamp
        "buy_timestamp": datetime.datetime.now(eastern_tz).isoformat(),
        "buy_price": token_details.get('price'),
        "buy_amount_sol": 1.00, # Default buy amount
        "position_closed": False,
        "sell_timestamp": None,
        "sell_amount_sol": None,
        "sol_delta": None,
        "percentage_delta": None,
        "num_tokens_bought": 1912380.2090
    }
    #token_stats_json = get_token_stats(token_details.get('address'))
    logging.info(f"--- Buying Token (Placeholder) ---")
    logging.info(f"Symbol: {token_details.get('symbol')}")
    logging.info(f"Address: {token_details.get('address')}")
    logging.info(f"Price: {token_details.get('price')}")
    logging.info(f"----------------------------------")
    #data_to_insert["token_intial_stats"] = token_stats_json
    response = supabase.table("positions").insert(data_to_insert).execute()


def get_token_stats(token_address):
    """
    Fetches the token price from gmgn.ai API using a curl command.

    Args:
        token_address (str): The address of the token.

    Returns:
        float: The price of the token, or None if an error occurs.
    """
    curl_command = [
        'curl',
        'https://gmgn.ai/api/v1/mutil_window_token_info?device_id=6531e1ad-81ac-44bf-94bd-a890c1ffd309&client_id=gmgn_web_2025.0215.105604&from_app=gmgn&app_ver=2025.0215.105604&tz_name=America%2FNew_York&tz_offset=-18000&app_lang=en',
        '-H', 'accept: application/json, text/plain, */*',
        '-H', 'accept-language: en-US,en;q=0.9',
        '-H', 'content-type: application/json',
        '-H', 'cookie: sid=gmgn%7Ceac84f530afab428a3ad01b208434159; _ga_UGLVBMV4Z0=GS1.2.1739256544201376.30b3dddf62c63dccd2223ea9d7d6a5e3.2lRMBEoVlqQi3StF3EFjaA%3D%3D.lDHYeGWroVi8a%2Ft7vmcUiA%3D%3D.VLH2N8vnv%2Fo5u4DbM5JAfg%3D%3D.kwmw%2B1%2BYYT0649I%2F8Qx4ww%3D%3D; cf_clearance=vXO_yqlSsXabAVZ25iFyzXx.WyJzolAgLHj3ozJLvTs-1739596266-1.2.1.1-vaQvYzwc5XY5eWhN3HUATjVv22cmbcpIH1mAWxNOY4lzyWlG3bqNelyFsOmIjxKlrlWjkqy8aFJDeoI_3UP8VrC0q34ocHqkEcg9ktM.icDXZI2SnfgNxPoICtz_.DWG67.0G67N36EyGXtQDFKG4UUoOVcqjgkQXz7tIdhdanJ9wu8Znift8da6yBX.mNyXwAJTHyGjc7EAnctLtTOhlEa4Bsrq4tvVVFDGZXEr.3B3iItIcp_Wh2Sybl36JkBW3NKAxc6rSsF_x6jBFkebPvODL1kFKTyz.cx3djStFb4; __cf_bm=YfRh1xY0o2FGo2w0nWFC7mEEvOrt_xkjyskflLWVtIo-1739598084-1.0.1.1-5uVHdagPN9fu27lMqmVs_0QAAsP8k.vT494pR6B3BSSzYOfVMR91LlgYZ_ECTBkwbD5fKNeLmOPBZcac9Pe_4A',
        '-H', 'origin: https://gmgn.ai',
        '-H', 'priority: u=1, i',
        '-H', 'referer: https://gmgn.ai/sol/token/qaxEG3F2_6mPpZCDa75eVTs4oAjDfDnYXB2YMMqw1Luumy1un1AKm', # You might need to dynamically change this referer if needed
        '-H', 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "macOS"',
        '-H', 'sec-fetch-dest: empty',
        '-H', 'sec-fetch-mode: cors',
        '-H', 'sec-fetch-site: same-origin',
        '-H', 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        '--data-raw', f'{{"chain":"sol","addresses":["{token_address}"]}}'
    ]

    try:
        process = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        output_json = json.loads(process.stdout)
        return output_json

    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        print(f"Response content: {process.stdout if 'process' in locals() else 'N/A'}")
        return None
    except KeyError as e:
        print(f"Error accessing key in JSON response: {e}")
        print(f"Response content: {output_json if 'output_json' in locals() else 'N/A'}")
        return None