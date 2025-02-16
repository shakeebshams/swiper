import os
import datetime
import logging
import time
from dotenv import load_dotenv
from supabase import create_client
from gmgn_price import get_token_price
import pytz

# Load environment variables and create a Supabase client.
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
eastern_tz = pytz.timezone('US/Eastern')

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Assume that check_price and sell_token are already defined elsewhere.

def sell_token(token_details):
    """
    This function is assumed to be defined elsewhere.
    It should perform the swap/sell operation and return stats about the sale.
    """
    logging.info(f"Selling token: {token_details.get('token_address')}")
    # Dummy implementation; in reality, this would execute the sell.
    return {"sell_amount_sol": token_details.get("buy_amount_sol", 1.00)}

def process_open_positions():
    # Query all positions that have not been closed.
    try:
        response = supabase.table("positions").select("*").eq("position_closed", False).execute()
        # Access the data directly from the .data attribute
        positions = response.data
        logging.info(f"Found {len(positions)} open positions.")
    except Exception as e:
        logging.error(f"Error fetching positions from Supabase: {e}")
        return  # Exit the function if there's an error fetching data

    for pos in positions:
        token_address = pos.get("token_address")
        # Added more robust error handling and input validation
        if not token_address:
            logging.error("Position missing token_address. Skipping.")
            continue

        try:
            buy_price = float(pos.get("buy_price"))
            buy_amount_sol = float(pos.get("buy_amount_sol"))
            # Handle cases where buy_timestamp might be None
            buy_timestamp_str = pos.get("buy_timestamp")
            if buy_timestamp_str is None:
                logging.error(f"buy_timestamp is None for token {token_address}. Skipping.")
                continue
            # Parse the string (handles 'Z' and '+00:00')
            buy_timestamp = datetime.datetime.fromisoformat(buy_timestamp_str.replace("Z", "+00:00"))
            if buy_timestamp.tzinfo is None:
                buy_timestamp = eastern_tz.localize(buy_timestamp)  # Localize to Eastern time if not already timezone-aware

        except (TypeError, ValueError) as e:
            logging.error(f"Invalid buy price, amount, or timestamp for token {token_address}: {e}. Skipping.")
            continue
        except Exception as e:
            logging.error(f"Error parsing buy_timestamp for token {token_address}: {e}")
            continue

        now = datetime.datetime.now(eastern_tz)
        elapsed_seconds = (now - buy_timestamp).total_seconds()

        # Get the current price. Add error handling for get_token_price
        try:
            current_price = get_token_price(token_address)
            if current_price is None:
                logging.error(f"Could not retrieve price for token {token_address}. Skipping.")
                continue
            current_price = float(current_price)  # Ensure it's a float
        except Exception as e:
            logging.error(f"Error getting price for {token_address}: {e}")
            continue
        logging.info(f"Token {token_address} - current price: {current_price}, buy price: {buy_price}")

        sell = False
        reason = ""

        # Condition 1: Price is at least 2.5% higher than buy_price.
        if current_price >= buy_price * 1.025:
            sell = True
            reason = "Price increased by at least 2.5%."
            logging.info(f"Token {token_address} - Price increased by at least 2.5%.")

        # Condition 2: Position has been open for more than 5 minutes.
        elif elapsed_seconds > 300:
            sell = True
            reason = "Position open for more than 5 minutes."
            logging.info(f"Token {token_address} - Position open for more than 5 minutes.")

        # Condition 3: Price dropped more than 50% from purchase price.
        elif current_price <= buy_price * 0.5:
            sell = True
            reason = "Price dropped more than 50% from purchase price."
            logging.info(f"Token {token_address} - Price dropped more than 50% from purchase price.")

        if sell:
            logging.info(f"Selling token {token_address}: {reason}")
            # Execute the sell operation.
            sell_result = sell_token(pos)  # Capture the result
            sell_timestamp = datetime.datetime.now().isoformat()

            # Update the record in Supabase (only marking as closed with sell details).
            update_data = {
                "position_closed": True,
                "sell_timestamp": sell_timestamp,
                "sell_amount_sol": sell_result.get("sell_amount_sol", buy_amount_sol),  # Use result, fallback to buy
                "sell_price": current_price,
            }

            try:
                update_response = supabase.table("positions").update(update_data).eq("id", pos.get("id")).execute()
                # Check for successful update.  .data will be an empty list if nothing was updated.
                if not update_response.data:
                    logging.warning(f"Failed to update position {pos.get('id')} in Supabase.")
                else:
                    logging.info(f"Successfully updated position {pos.get('id')}: {update_response.data}") # Log updated data
            except Exception as e:
                logging.error(f"Error updating position in Supabase: {e}")
        else:
            logging.info(f"Holding token {token_address}: Conditions not met for selling.")

if __name__ == "__main__":
    while True:
        process_open_positions()
        # Wait 1 second before running the check again.
        time.sleep(1)