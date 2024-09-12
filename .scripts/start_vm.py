import XenAPI
import ssl
import sys
import xmlrpc.client

class UnverifiedSSLTransport(xmlrpc.client.SafeTransport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = ssl._create_unverified_context()

    def make_connection(self, host):
        connection = super().make_connection(host)
        connection._context = self.context
        return connection

def create_session(url, username, password):
    print(f"Creating session with XenServer at {url}...")
    if not url.startswith("https://"):
        url = "https://" + url
    try:
        transport = UnverifiedSSLTransport()
        session = XenAPI.Session(url, transport=transport)
        session.xenapi.login_with_password(username, password, "1.0", "XenAPI Client")
        print("Session created successfully.")
        return session
    except Exception as e:
        print(f"Failed to create session: {e}")
        sys.exit(1)

def start_vm(session, vm_name):
    print(f"Attempting to start VM: {vm_name}")
    try:
        vms = session.xenapi.VM.get_by_name_label(vm_name)
        if not vms:
            print(f"No VM found with name {vm_name}")
            sys.exit(1)

        vm = vms[0]  # Zakładając, że nazwa VM jest unikalna
        session.xenapi.VM.start(vm, False, True)
        print(f"VM '{vm_name}' has been started.")
    except Exception as e:
        print(f"Failed to start VM: {e}")
        sys.exit(1)

def main(url, username, password, vm_name):
    session = create_session(url, username, password)
    try:
        start_vm(session, vm_name)
    finally:
        print("Logging out of the session.")
        session.xenapi.session.logout()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python start_vm.py <url> <username> <password> <vm_name>")
        sys.exit(1)

    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    vm_name = sys.argv[4]

    main(url, username, password, vm_name)

