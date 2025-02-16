import subprocess
import json

def get_token_price(token_address):
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

        if output_json['code'] == 0 and output_json['data']:
            token_data = output_json['data'][0]
            token_price = token_data['price']['price']
            return float(token_price)
        else:
            print(f"Error from API: {output_json.get('message') or output_json.get('reason')}")
            return None

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

if __name__ == '__main__':
    token_address = "EcV5KB5mtKmoVeV6kjAnaCWWtHe3wEi1bLYxpejpJwwT"  # Example token address
    token_price = get_token_price(token_address)

    if token_price is not None:
        print(f"Token price for address {token_address}: {token_price}")
    else:
        print(f"Could not retrieve token price for address {token_address}")



