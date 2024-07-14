#  JOIN TELEGRAM : https://t.me/apsstudiotech
#  JOIN DISCORD : https://discord.gg/N9caefVJ7F

import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

get_url = "https://cellcoin.org/users/session"
post_claim_storage_url = "https://cellcoin.org/cells/claim_storage"
post_submit_clicks_url = "https://cellcoin.org/cells/submit_clicks"
post_upgrade_url = "https://cellcoin.org/cells/levels/upgrade"

ascii_art = f"""
{Fore.GREEN}
 █████╗ ██████╗ ███████╗    ███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
███████║██████╔╝███████╗    ███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
██╔══██║██╔═══╝ ╚════██║    ╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
██║  ██║██║     ███████║    ███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ 
{Style.RESET_ALL}
{Fore.CYAN}JOIN TELEGRAM : https://t.me/apsstudiotech
JOIN DISCORD  : https://discord.gg/N9caefVJ7F{Style.RESET_ALL}
"""

def load_auth_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def main(auth_token):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Authorization': auth_token,
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://cell-frontend.s3.us-east-1.amazonaws.com/',
        'Origin': 'https://cell-frontend.s3.us-east-1.amazonaws.com',
    }

    try:
        # Perform the GET request
        get_response = requests.get(get_url, headers=headers)
        get_response.raise_for_status()  # Raise an error for bad responses

        response_json = get_response.json()
        user_id = response_json.get('user', {}).get('ID')
        username = response_json.get('user', {}).get('username')
        balance = response_json.get('cell', {}).get('balance')
        print(f"{Fore.CYAN}ID: {user_id}, \nUsername: {username}, \nBalance: {balance}{Style.RESET_ALL}")

        # Perform the POST request to upgrade level
        post_upgrade_data = '{"level_type":"bonus"}'
        post_upgrade_headers = headers.copy()
        post_upgrade_headers['Content-Type'] = 'application/json'
        post_upgrade_response = requests.post(post_upgrade_url, headers=post_upgrade_headers, data=post_upgrade_data)

        if post_upgrade_response.status_code == 200:
            print(f"{Fore.GREEN}Level upgrade success{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Level upgrade failed{Style.RESET_ALL}")

        # Perform the POST request to claim storage
        post_claim_storage_headers = headers.copy()
        post_claim_storage_headers['Content-Length'] = '0'
        post_claim_storage_response = requests.post(post_claim_storage_url, headers=post_claim_storage_headers)

        # Log the result of the first POST request
        if post_claim_storage_response.status_code == 200:
            print(f"{Fore.GREEN}Daily claim success{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Daily claim sudah diambil{Style.RESET_ALL}")

        # Perform the second POST request (submit_clicks) regardless of the claim_storage response
        post_submit_clicks_headers = headers.copy()
        post_submit_clicks_headers.update({
            'Content-Type': 'application/json',
        })
        post_submit_clicks_data = '{"clicks_amount": 10000}'

        # Perform the preflight (OPTIONS) request
        options_response = requests.options(post_submit_clicks_url, headers=post_submit_clicks_headers)
        if options_response.status_code == 204:
            print(f"{Fore.GREEN}Preflight OPTIONS request successful{Style.RESET_ALL}")

            # Perform the submit_clicks request
            post_submit_clicks_response = requests.post(
                post_submit_clicks_url, headers=post_submit_clicks_headers, data=post_submit_clicks_data)

            if post_submit_clicks_response.status_code == 200:
                response_json = post_submit_clicks_response.json()
                print(f"{Fore.GREEN}Tap Success{Style.RESET_ALL}")

                # Check the energy amount
                energy_amount = response_json.get('cell', {}).get('energy_amount', 0)
                if energy_amount > 10:
                    print(f"{Fore.GREEN}Tapp success{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Tap done!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Energy amount is less than 10.{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}OPTIONS request failed with status code {options_response.status_code}{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def execute_all_accounts():
    auth_tokens = load_auth_tokens('token.txt')
    for auth_token in auth_tokens:
        main(auth_token)
        print(f"{Fore.MAGENTA}Sleeping for 2 seconds before retrying next account...{Style.RESET_ALL}")
        time.sleep(2) 
if __name__ == "__main__":
    print(ascii_art)
    while True:
        execute_all_accounts()
        print(ascii_art)
        print(f"{Fore.MAGENTA}Restarting after all accounts are executed. Sleeping for 10 seconds...{Style.RESET_ALL}")
        time.sleep(10) 
