import traceback
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()


try:
    port = int(os.environ.get("PORT", "8080"))
except ValueError:
    port = -1
if not 1 <= port <= 65535:
    print("Please make sure the PORT environment variable is an integer between 1 and 65535")
    sys.exit(1)

try:
    privatekey = os.environ.get("PRIVATEKEY", None)
except:
    print("Api unsecure use private ")


try:
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
except (KeyError, ValueError):
    traceback.print_exc()
    print("\n\nPlease set the API_ID and API_HASH environment variables correctly")

    sys.exit(1)

try:

    index_settings_str = os.environ.get("INDEX_SETTINGS")

    index_settings_str = index_settings_str.replace("'", '"')
    index_settings = json.loads(index_settings_str)
    '''
    {"index_all": true, "index_private":false, "index_group": false,
        "index_channel": true, "include_chats": [], "exclude_chats": []}

    '''
except:
    traceback.print_exc()
    print("\n\nPlease set the INDEX_SETTINGS environment variable correctly")
    sys.exit(1)

try:
    session_string = os.environ["SESSION_STRING"]
except (KeyError, ValueError):
    traceback.print_exc()
    print("\n\nPlease set the SESSION_STRING environment variable correctly")
    sys.exit(1)

host = os.environ.get("HOST", "0.0.0.0")
debug = bool(os.environ.get("DEBUG"))
chat_ids = []
alias_ids = []
