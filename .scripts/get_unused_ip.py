import requests
from bs4 import BeautifulSoup
import ipaddress
import sys

def get_unused_ips(pfSense_url_login, pfSense_url_dhcp, username, password):
    # Wyłączenie ostrzeżeń SSL
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Sesja
    session = requests.Session()

    # Pobranie strony logowania, aby uzyskać CSRF token
    response = session.get(pfSense_url_login, verify=False)

    # Parsowanie HTML, aby znaleźć CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '__csrf_magic'})['value']

    # Dane logowania z CSRF token
    login_data = {
        '__csrf_magic': csrf_token,
        'usernamefld': username,
        'passwordfld': password,
        'login': 'Sign In'
    }

    # Logowanie
    response = session.post(pfSense_url_login, data=login_data, verify=False)

    # Sprawdzenie, czy logowanie się powiodło
    if 'services_dhcp.php' in response.text or response.url.endswith('services_dhcp.php'):
        # Połączenie do pfSense DHCP
        response = session.get(pfSense_url_dhcp, verify=False)

        if response.status_code == 200:
            # Parsowanie HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Znalezienie tabeli z DHCP Mappings
            used_ips = set()

            for row in soup.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 6 and 'ondblclick' in cells[0].attrs:
                    ip_address = cells[3].text.strip()
                    if ip_address:
                        used_ips.add(ip_address)

            # Generowanie puli adresów IP od 192.168.100.150 do 192.168.100.250
            ip_pool = [str(ip) for ip in ipaddress.IPv4Network('192.168.100.150/31').hosts()] + \
                      [str(ip) for ip in ipaddress.IPv4Network('192.168.100.152/29').hosts()] + \
                      [str(ip) for ip in ipaddress.IPv4Network('192.168.100.160/27').hosts()] + \
                      [str(ip) for ip in ipaddress.IPv4Network('192.168.100.192/26').hosts()]

            unused_ips = [ip for ip in ip_pool if ip not in used_ips]

            return unused_ips
        else:
            return []
    else:
        return []

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python get_unused_ip.py <pfSense_url_login> <pfSense_url_dhcp> <username> <password>")
        sys.exit(1)

    pfSense_url_login = sys.argv[1]
    pfSense_url_dhcp = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]

    available_ips = get_unused_ips(pfSense_url_login, pfSense_url_dhcp, username, password)

    if available_ips:
        for ip in available_ips:
            print(ip)
    else:
        sys.exit(1)  # Zakończ program z błędem, jeśli brak dostępnych IP lub coś poszło nie tak
