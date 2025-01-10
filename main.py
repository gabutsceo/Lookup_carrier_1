import requests
import time
import os
import random
from colorama import Fore, Style, init

# Initialize colorama to support colored output on all platforms
init(autoreset=True)

# Define your API and proxy credentials
API_URL = "https://api.clearoutphone.io/v1/phonenumber/validate"
API_TOKEN = "173654fc367f118bf183f5f91dc6ba3e:a88c0d020e69048abaf45f20bd9914f370ab23c54a3aaaf1f11df28cb1c0f7e9"
PROXY_USERNAME = "52xrymt17qdjxdn-odds-6+100"
PROXY_PASSWORD = "00h90dhkmyeephq"
PROXY = "rp.scrapegw.com:6060"
PROXY_AUTH = "{}:{}@{}".format(PROXY_USERNAME, PROXY_PASSWORD, PROXY)

# Proxy setup
proxies = {
    "http": f"http://{PROXY_AUTH}",
    "https": f"http://{PROXY_AUTH}"
}

# Ensure result folder exists
os.makedirs('result', exist_ok=True)

# Define file paths
VALID_FILE = 'result/valid.txt'
INVALID_FILE = 'result/die.txt'
ERROR_LOG_FILE = 'result/error_log.txt'

# List of color options for random coloring (without red for valid)
COLOR_OPTIONS_VALID = [Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]
COLOR_OPTIONS_INVALID = [Fore.RED]  # Red color for invalid numbers

# Function to log results
def log_to_file(file_path, text):
    with open(file_path, 'a') as f:
        f.write(text + '\n')

# Function to process the API response
def process_phone_number(number):
    payload = f'{{ "number": "{number}", "country_code": "US" }}'
    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {API_TOKEN}",
    }

    try:
        response = requests.post(API_URL, data=payload, headers=headers, proxies=proxies)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Check if response has valid data
        if data.get('status') == 'success':
            status = data['data']['status']
            line_type = data['data']['line_type']
            location = data['data']['location']
            carrier = data['data']['carrier']
            country_code = data['data']['country_code']

            # Random color selection for valid numbers (without red)
            if status == "valid":
                random_color = random.choice(COLOR_OPTIONS_VALID)
                output = f"{random_color}VALID =>> {number} - {carrier} - {line_type} - {location} - {country_code}{Style.RESET_ALL}"
                print(output)
                # Same format saved to file
                log_to_file(VALID_FILE, f"VALID =>> {number} - {carrier} - {line_type} - {location} - {country_code}")
            else:
                # Red color for invalid numbers
                random_color = random.choice(COLOR_OPTIONS_INVALID)
                output = f"{random_color}INVALID =>> {number} - {carrier} - {line_type} - {location} - {country_code}{Style.RESET_ALL}"
                print(output)
                # Same format saved to file
                log_to_file(INVALID_FILE, f"INVALID =>> {number} - {carrier} - {line_type} - {location} - {country_code}")
        else:
            # In case status is not 'success', log an error
            output = f"{Fore.YELLOW}UNKNOWN =>> {number}{Style.RESET_ALL}"
            print(output)
            log_to_file(ERROR_LOG_FILE, f"UNKNOWN - {number}")

    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., timeouts, API issues)
        output = f"{Fore.RED}ERROR =>> {number} - ERROR: {str(e)}{Style.RESET_ALL}"
        print(output)
        log_to_file(ERROR_LOG_FILE, f"ERROR - {number} - {str(e)}")

# Function to read phone numbers from file and process them
def process_phone_numbers(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            number = line.strip()
            if len(number) == 10 and number.isdigit():  # Check if the number is valid (10 digits)
                process_phone_number(number)
            else:
                print(f"Invalid number format: {number}")
                log_to_file(ERROR_LOG_FILE, f"INVALID FORMAT - {number}")

            time.sleep(3)  # 3 seconds delay between requests

# Main function to start the process
if __name__ == "__main__":
    process_phone_numbers('mobile.txt')
