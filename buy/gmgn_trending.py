import subprocess
import requests
import time
import json
import datetime
import logging
from swap import buy_token_placeholder


def fetch_trending_tokens():
    """
    Fetches trending tokens from the gmgn.ai API.

    Returns:
        dict: JSON response from the API if successful, None otherwise.
    """
    curl_command = [
    'curl',
    'https://gmgn.ai/defi/quotation/v1/rank/sol/swaps/1m?device_id=6531e1ad-81ac-44bf-94bd-a890c1ffd309&client_id=gmgn_web_2025.0208.195617&from_app=gmgn&app_ver=2025.0208.195617&tz_name=America%2FNew_York&tz_offset=-18000&app_lang=en&orderby=open_timestamp&direction=desc&limit=20&min_liquidity=50000&min_marketcap=1000000',
    '-H', 'accept: application/json, text/plain, */*',
    '-H', 'accept-language: en-US,en;q=0.9',
    '-H', 'cookie: sid=gmgn%7Ceac84f530afab428a3ad01b208434159; _ga_UGLVBMV4Z0=GS1.2.1739256544201376.30b3dddf62c63dccd2223ea9d7d6a5e3.2lRMBEoVlqQi3StF3EFjaA%3D%3D.lDHYeGWroVi8a%2Ft7vmcUiA%3D%3D.VLH2N8vnv%2Fo5u4DbM5JAfg%3D%3D.kwmw%2B1%2BYYT0649I%2F8Qx4ww%3D%3D; cf_clearance=HqRtGYG1Z281QzCaO7qblXbJoIEjqUFvEzBoMTdzDM4-1739775287-1.2.1.1-tU5osfhVkF.kdAt3MNXMxrtMlwKa58QWsblmtg3TsQRU33x9kUaRpi0TcC7KXF9eUB1s0ji4TYV2VO_2APNaV4utmRVJAy6F6MBo4rPrlF6TczlDTk5WduFDlJQtxF60SOfB2OSVl8iQd3kOV_p.OyyQsIT3FaGH7iKU8IX_wvgXSHHD_c6OE2z_wQSk_bCEZBi.i9cRE7Bs.c_SpWNsNL2MTb8VMJ0hRFoYEqh1dCdk65yhLInu4SL6ZtZDi3XHI5zrQ3I5sxA7ScE5ZhldK6Pk0zfm_oZ.CAT3lhD9RPM; __cf_bm=6vV5yUIvRe3mWCARvvqvWQ8JbSdllLPMFmuAFVKJs4Q-1739775299-1.0.1.1-em1UuQBW3PFrfwKd8mrSPJ3q1b6UpVFVn1H8JSp3oQIkG1zLmc2pgjYCGy4EnujrXu5jb5FsSJbqoeep_HtWOw',
    '-H', 'if-none-match: W/"5d1a-owTyDIaOAn3M0HLeoVbDMuzknnA"',
    '-H', 'priority: u=1, i',
    '-H', 'referer: https://gmgn.ai/?chain=sol&ref=qaxEG3F2&tab=trending',
    '-H', 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    '-H', 'sec-ch-ua-mobile: ?0',
    '-H', 'sec-ch-ua-platform: "macOS"',
    '-H', 'sec-fetch-dest: empty',
    '-H', 'sec-fetch-mode: cors',
    '-H', 'sec-fetch-site: same-origin',
    '-H', 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    ]

    try:
        process = subprocess.run(curl_command, capture_output=True, text=True, check=True) # check=True will raise an exception for non-zero return codes
        logging.info("Successfully fetched trending tokens from API.")
        return json.loads(process.stdout) # Parse JSON here, after successful execution
    except subprocess.CalledProcessError as e:
        logging.error(f"curl command failed with return code: {e.returncode}")
        logging.error(f"stderr: {e.stderr}")
        return None # Indicate failure
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response from API.")
        #logging.error(f"Raw response: {process.stdout if 'process' in locals() else 'No response due to curl failure'}") # Handle case where process failed before stdout capture
        return None
    
def process_tokens(data):
    """
    Processes the JSON response to identify and buy new tokens.

    Args:
        data (dict): JSON response from the API.
    """
    if not data or data.get('code') != 0 or not data.get('data') or not data.get('data').get('rank'):
        logging.warning("No valid token data received or API error.")
        return

    current_time = datetime.datetime.now(datetime.timezone.utc) # Use UTC for time comparison

    for token in data['data']['rank']:
        open_timestamp = token.get('pool_creation_timestamp') # Using open_timestamp as creation time
        if open_timestamp:
            token_creation_time = datetime.datetime.fromtimestamp(open_timestamp, tz=datetime.timezone.utc) # Assuming timestamp is UTC
            age = current_time - token_creation_time
            if age < datetime.timedelta(minutes=1):
                logging.info(f"New token found: {token.get('symbol')} - Age: {age}")
                buy_token_placeholder(token) # Call buy function for tokens less than 1 minute old
            else:
                logging.debug(f"Token {token.get('symbol')} is older than 1 minute, age: {age}") # Debug log for tokens older than 1 minute
        else:
            logging.warning(f"Token {token.get('symbol')} has no open_timestamp.") # Handle case of missing timestamp
