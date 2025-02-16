import requests
import time
import json
from web3 import Web3
from eth_account.messages import encode_defunct
from datetime import datetime, timezone
from colorama import Fore, init, Style
from fake_useragent import UserAgent
import random
import os

init(autoreset=True)

# Function to display a rainbow banner
def rainbow_banner():
    os.system("clear" if os.name == "posix" else "cls")
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = """
  _______                          
 |     __|.--.--.---.-.-----.---.-.
 |__     ||  |  |  _  |-- __|  _  |
 |_______||___  |___._|_____|___._|
          |_____|                   
    """
    
    for i, char in enumerate(banner):
        print(colors[i % len(colors)] + char, end="")
        time.sleep(0.007)
    print(Fore.LIGHTYELLOW_EX + "\nPlease wait...\n")
    time.sleep(2)
    os.system("clear" if os.name == "posix" else "cls")
    for i, char in enumerate(banner):
        print(colors[i % len(colors)] + char, end="")
    print(Fore.LIGHTYELLOW_EX + "\n")

# Read private keys from file
def read_private_keys(file_path):
    private_keys = []
    with open(file_path, 'r') as file:
        for line in file:
            private_key = line.strip()
            if private_key:
                private_keys.append(private_key)
    return private_keys

# Read user agents from file
def read_user_agents(file_path):
    user_agents = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            user_agents = json.load(file)
    return user_agents

# Save user agents to file
def save_user_agents(file_path, user_agents):
    with open(file_path, 'w') as file:
        json.dump(user_agents, file)

# Read session data from file
def read_session_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

# Save session data to file
def save_session_data(file_path, session_data):
    with open(file_path, 'w') as file:
        json.dump(session_data, file)

# Read referral codes from file
def read_referral_codes(file_path):
    referral_codes = []
    with open(file_path, 'r') as file:
        for line in file:
            ref_code = line.strip()
            if ref_code:
                referral_codes.append(ref_code)
    return referral_codes

# Save referral codes to file
def save_referral_codes(file_path, referral_codes):
    with open(file_path, 'w') as file:
        for ref_code in referral_codes:
            file.write(ref_code + '\n')

# Data from privatekeys.txt
private_keys = read_private_keys('privatekeys.txt')

# User agents file path
user_agents_file = 'ua.txt'
user_agents = read_user_agents(user_agents_file)

# Session data file path
session_data_file = 'session_data.json'
session_data = read_session_data(session_data_file)

# Referral codes from code.txt
referral_codes_file = 'code.txt'
referral_codes = read_referral_codes(referral_codes_file)

# URL endpoints for session initiation, authentication, and quests
init_endpoint = 'https://auth.privy.io/api/v1/siwe/init'
authenticate_endpoint = 'https://auth.privy.io/api/v1/siwe/authenticate'
login_endpoint = 'https://api.service.crestal.network/v1/login?is_privy=true'
quests_endpoint = 'https://api.service.crestal.network/v1/quests'
latest_quests_endpoint = 'https://api.service.crestal.network/v1/quests/latest?user_address={user_address}'
profile_endpoint_template = 'https://api.service.crestal.network/v1/users/{user_address}'
complete_quest_endpoint_template = 'https://api.service.crestal.network/v1/report?user_address={user_address}&type={activity_action}'
claim_referral_endpoint_template = 'https://api.service.crestal.network/v1/referral/{ref_code}/claim'

allowed_activity_actions = [
    "interact_with_dashboard",
    "use_deployed_blueprint_proposal",
    "feedback",
    "read_blog",
    "follow_crestal_on_x",
    "join_telegram",
    "join_discord",
    "post_about_crestal",
    "interact_with_crestal_x",
    "submit_intent_kit_pr",
    "start_intent_kit",
    "nft_weekly_award"
]

# Function to initiate session with exponential backoff
def init_session(address, headers, retries=5):
    payload = {"address": address}
    for attempt in range(retries):
        response = requests.post(init_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            log("\n✔ Init session successful")
            return response.json()
        elif response.status_code == 429:
            delay = 5 * (2 ** attempt)
            log(f"\n♻ Rate limit exceeded, retrying in {delay} seconds...", end="")
            time.sleep(delay)
        else:
            log(f"\n✖ Init session failed (HTTP {response.status_code})")
            log(f"⚠ Response: {response.text}")
    return None

# Function to sign message
def sign_message(private_key, message):
    web3 = Web3()
    message = encode_defunct(text=message)
    signed_message = web3.eth.account.sign_message(message, private_key=private_key)
    return signed_message.signature.hex()

# Function to authenticate with retry and exponential backoff
def authenticate(private_key, init_data, headers, retries=5):
    web3 = Web3()
    account = web3.eth.account.from_key(private_key)
    issued_at = datetime.now(timezone.utc).isoformat()
    message = (
        f"app.crestal.network wants you to sign in with your Ethereum account:\n{account.address}\n\n"
        "By signing, you are proving you own this wallet and logging in. This does not initiate a transaction or cost any fees.\n\n"
        f"URI: https://app.crestal.network\nVersion: 1\nChain ID: 8453\nNonce: {init_data['nonce']}\n"
        f"Issued At: {issued_at}\nResources:\n- https://privy.io"
    )
    signature = "0x" + sign_message(private_key, message)
    log("✔ Message signed")
    payload = {
        "message": message,
        "signature": signature,
        "chainId": "eip155:8453",
        "walletClientType": "okx_wallet",
        "connectorType": "injected",
        "mode": "login-or-sign-up"
    }
    for attempt in range(retries):
        response = requests.post(authenticate_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            log("\n✔ Authenticate successful")
            return response.json()
        elif response.status_code == 429:
            delay = 5 * (2 ** attempt)
            log(f"\n♻ Rate limit exceeded, retrying in {delay} seconds...", end="")
            time.sleep(delay)
        else:
            log(f"\n✖ Authenticate failed (HTTP {response.status_code})")
            log(f"⚠ Response: {response.text}")
    return None

# Function to login with privy token and get crestal token with retry and exponential backoff
def login_with_privy_token(privy_token, user_address, headers, retries=5):
    payload = {"privy_token": privy_token, "user_address": user_address}
    for attempt in range(retries):
        response = requests.post(login_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            log("✔ Login successful")
            return response.json()
        elif response.status_code == 429:
            delay = 5 * (2 ** attempt)
            log(f"\n♻ Rate limit exceeded, retrying in {delay} seconds...", end="")
            time.sleep(delay)
        else:
            log(f"\n✖ Login failed (HTTP {response.status_code})")
            log(f"⚠ Response: {response.text}")
    return None

# Function to get account profile
def get_profile(access_token, user_address, headers):
    headers['Authorization'] = f"Bearer {access_token}"
    profile_endpoint = profile_endpoint_template.format(user_address=user_address)
    response = requests.get(profile_endpoint, headers=headers)
    if response.status_code == 200:
        log("\n✔ Account profile loaded")
        return response.json()
    elif response.status_code == 400 and "token is expired" in response.text.lower():
        return "token_expired"
    else:
        log(f"\n✖ Account profile retrieval failed (HTTP {response.status_code})")
        log(f"⚠ Response: {response.text}")
        return None

# Function to get latest quests
def get_latest_quests(access_token, user_address, headers):
    headers['Authorization'] = f"Bearer {access_token}"
    response = requests.get(latest_quests_endpoint.format(user_address=user_address), headers=headers)
    if response.status_code == 200:
        log("✔ Latest quest retrieved")
        return response.json()
    else:
        log(f"✖ Latest quest retrieval failed (HTTP {response.status_code})")
        log(f"⚠ Response: {response.text}")
        return []

# Function to get quests
def get_quests(access_token, headers):
    headers['Authorization'] = f"Bearer {access_token}"
    response = requests.get(quests_endpoint, headers=headers)
    if response.status_code == 200:
        log("✔ Quest retrieved")
        return response.json()
    else:
        log(f"✖ Quest retrieval failed (HTTP {response.status_code})")
        log(f"⚠ Response: {response.text}")
        return []

# Function to complete quest
def complete_quest(access_token, quest, user_address, headers):
    if quest['activity_action'] not in allowed_activity_actions:
        log(f"✖ Quest '{quest['title']}' not allowed: {quest['activity_action']}")
        return False
    log(f"↻ Completing quest '{quest['title']}'")
    headers['Authorization'] = f"Bearer {access_token}"
    complete_quest_endpoint = complete_quest_endpoint_template.format(user_address=user_address, activity_action=quest['activity_action'])
    response = requests.post(complete_quest_endpoint, headers=headers)
    
    if response.status_code == 200:
        log(f"✔ Quest '{quest['title']}' completed successfully")
        return True
    else:
        try:
            error_msg = response.json().get('msg', response.text)
        except json.JSONDecodeError:
            error_msg = response.text
        log(f"✖ Quest '{quest['title']}' completion failed: {response.status_code}, {error_msg}")
        return False

# Function to claim referral code
def claim_ref_code(access_token, ref_code, headers):
    headers['Authorization'] = f"Bearer {access_token}"
    claim_referral_endpoint = claim_referral_endpoint_template.format(ref_code=ref_code)
    response = requests.post(claim_referral_endpoint, headers=headers)
    
    if response.status_code == 200:
        log(f"✔ Referral code '{ref_code}' claimed successfully")
        return response
    else:
        return response

# Function to generate or retrieve User-Agent
def generate_headers(account):
    if account not in user_agents:
        ua = UserAgent()
        user_agents[account] = ua.random
        save_user_agents(user_agents_file, user_agents)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agents[account],
        'Privy-App-Id': 'cm4v61vl108sdivml83sbeykh',
        'Privy-Ca-Id': 'ce166674-fc02-4f23-9d31-fe4e2ed29533',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://app.crestal.network',
        'Referer': 'https://app.crestal.network/',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    return headers

# Function to display loading with random delay
def display_loading(seconds):
    for remaining in range(seconds, 0, -1):
        log(f"⟳ Waiting {remaining} seconds...", end="\r")
        time.sleep(1)
    print()

# Function to log messages with rainbow effect
log_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
log_index = 0

def log(message, end="\n"):
    global log_index
    color = log_colors[log_index % len(log_colors)]
    print(color + message + Style.RESET_ALL, end=end)
    log_index += 1

# Function to handle token expiration and re-authentication
def handle_token_expiration(account, private_key, headers):
    log(f"\nToken expired for Wallet {account}, re-authenticating...", Fore.RED)
    init_data = init_session(account, headers)
    if init_data:
        auth_data = authenticate(private_key, init_data, headers)
        if auth_data:
            login_data = login_with_privy_token(auth_data['privy_access_token'], account, headers)
            if login_data:
                access_token = login_data['access_token']
                session_data[account] = {'access_token': access_token}
                save_session_data(session_data_file, session_data)
                return access_token
            else:
                log("✖ Login status: Failed")
        else:
            log("\n✖ Authentication status: Failed")
    else:
        log("\n✖ Session initiation status: Failed")
    return None

# Display banner
rainbow_banner()

# Process session initiation, authentication, login, profile retrieval, quest retrieval, quest completion, and referral code claim for each private key
while True:
    for private_key in private_keys:
        web3 = Web3()
        account = web3.eth.account.from_key(private_key).address
        headers = generate_headers(account)

        # Check if session data exists for the account
        if account in session_data:
            access_token = session_data[account]['access_token']
            log(f"\nUsing saved session for Wallet {account}", Fore.CYAN)
        else:
            log(f"\n↻ Processing Wallet {account}", Fore.CYAN)
            init_data = init_session(account, headers)
            if init_data:
                auth_data = authenticate(private_key, init_data, headers)
                if auth_data:
                    login_data = login_with_privy_token(auth_data['privy_access_token'], account, headers)
                    if login_data:
                        access_token = login_data['access_token']
                        session_data[account] = {'access_token': access_token}
                        save_session_data(session_data_file, session_data)
                    else:
                        log("✖ Login status: Failed")
                        continue
                else:
                    log("\n✖ Authentication status: Failed")
                    continue
            else:
                log("\n✖ Session initiation status: Failed")
                continue

        profile_data = get_profile(access_token, account, headers)
        if profile_data == "token_expired":
            access_token = handle_token_expiration(account, private_key, headers)
            if not access_token:
                continue
            profile_data = get_profile(access_token, account, headers)

        if profile_data:
            log("✔ Account profile retrieved")
            log("✔ Account Information:")
            log(f"✔ ID: {profile_data['id']}")
            log(f"✔ Rank: {profile_data['rank']}")
            log(f"✔ Total Points: {profile_data['total_point']}")
            log(f"✔ User Address: {profile_data['user_address']}")

            # Skip claiming referral code if already referred
            if not profile_data.get('is_referred', False):
                for ref_code in referral_codes:
                    response = claim_ref_code(access_token, ref_code, headers)
                    if response.status_code == 200:
                        referral_codes.remove(ref_code)
                        save_referral_codes(referral_codes_file, referral_codes)
                        break
                    elif response.status_code == 409:
                        referral_codes.remove(ref_code)
                        save_referral_codes(referral_codes_file, referral_codes)

            latest_quests = get_latest_quests(access_token, account, headers)
            latest_activity_actions = [quest['activity_action'] for quest in latest_quests]
            quests = get_quests(access_token, headers)
            if quests:
                for quest in quests:
                    if quest['activity_action'] not in latest_activity_actions:
                        success = complete_quest(access_token, quest, account, headers)
                        if not success:
                            response = requests.post(complete_quest_endpoint_template.format(user_address=account, activity_action=quest['activity_action']), headers=headers)
                            if "token is expired" in response.text.lower():
                                access_token = handle_token_expiration(account, private_key, headers)
                                if access_token:
                                    complete_quest(access_token, quest, account, headers)
                    else:
                        log(f"✔ Quest '{quest['title']}' already completed")
            else:
                log("✖ Quest retrieval status: Failed")
        
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Save user agents to file
    save_user_agents(user_agents_file, user_agents)

    # Random delay between 1 to 7 hours after all accounts are processed
    wait_time = random.randint(3600, 25200)  # Seconds
    display_loading(wait_time)
