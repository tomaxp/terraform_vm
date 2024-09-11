import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

# Wyłączanie ostrzeżeń dotyczących niezaufanych połączeń HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_to_pfsense(session, pfSense_url_login, username, password):
    response = session.get(pfSense_url_login, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__csrf_magic'})['value']

    login_data = {
        '__csrf_magic': csrf_token,
        'usernamefld': username,
        'passwordfld': password,
        'login': 'Sign In'
    }
    session.post(pfSense_url_login, data=login_data, verify=False)

def configure_dhcp(session, pfSense_url_dhcp, mac, ip, hostname, description, client_identifier):
    response = session.get(pfSense_url_dhcp, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__csrf_magic'})['value']

    dhcp_data = {
        '__csrf_magic': csrf_token,
        'mac': mac,
        'cid': client_identifier,
        'ipaddr': ip,
        'hostname': hostname,
        'descr': description,
        'save': 'Save'
    }
    response = session.post(pfSense_url_dhcp, data=dhcp_data, verify=False)
    return response.status_code, response.text

def apply_changes(session, pfSense_url_apply):
    # Upewnij się, że masz ważny token CSRF
    response = session.get(pfSense_url_apply, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__csrf_magic'})['value']

    # Wysłanie żądania POST, aby zastosować zmiany
    apply_data = {
        '__csrf_magic': csrf_token,
        'apply': 'Apply Changes'
    }
    response = session.post(pfSense_url_apply, data=apply_data, verify=False)
    return response.status_code, response.text

if __name__ == '__main__':
    if len(sys.argv) != 10:
        print("Usage: python register_in_pfsense.py <username> <password> <mac_address> <ip_address> <hostname> <template_name> <cpus> <memory> <disk_size>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    mac_address = sys.argv[3]
    ip_address = sys.argv[4]
    hostname = sys.argv[5]
    template_name = sys.argv[6]
    cpus = sys.argv[7]
    memory = sys.argv[8]
    disk_size = sys.argv[9]

    # Pobieranie aktualnej daty
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Generowanie opisu na podstawie podanych parametrów
    description = f"Created on {current_date}. VM {hostname} from template {template_name} with {cpus} CPUs, {memory} MB RAM and {disk_size} GB disk" if disk_size else f"Created on {current_date}. VM {hostname} from template {template_name} with {cpus} CPUs and {memory} MB RAM"

    pfSense_url_login = 'https://192.168.101.1/index.php'
    pfSense_url_dhcp = 'https://192.168.101.1/services_dhcp_edit.php?if=lan'
    pfSense_url_apply = 'https://192.168.101.1/services_dhcp.php?apply=Apply+Changes'
    client_identifier = hostname

    with requests.Session() as session:
        login_to_pfsense(session, pfSense_url_login, username, password)
        status_code, response_text = configure_dhcp(session, pfSense_url_dhcp, mac_address, ip_address, hostname, description, client_identifier)
        print(f"Successfully created VM '{hostname}' from template '{template_name}' with {cpus} CPUs, {memory} MB RAM and {disk_size} GB disk. MAC address: {mac_address}")

        if status_code == 200:
            print(f"Successfully added IP address {ip_address} to pfSense DHCP.")

            # Apply changes
            apply_status, apply_response = apply_changes(session, pfSense_url_apply)
            if apply_status == 200:
                print("Successfully applied changes in pfSense.")
            else:
                print(f"Failed to apply changes in pfSense. Status Code: {apply_status}")
        else:
            print(f"Failed to add IP address {ip_address} to pfSense DHCP. Status Code: {status_code}")
