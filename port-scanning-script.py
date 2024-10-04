import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((host, port))
        return port if result == 0 else None

def scan_ports(host, start_port, end_port):
    open_ports = []
    total_ports = end_port - start_port + 1

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        for i, future in enumerate(as_completed(futures)):
            port = futures[future]
            if future.result() is not None:
                open_ports.append(port)

            # Print progress bar
            progress = (i + 1) / total_ports
            bar_length = 40
            block = int(bar_length * progress)
            progress_bar = "#" * block + "-" * (bar_length - block)
            sys.stdout.write(f"\rScanning Ports: [{progress_bar}] {progress * 100:.2f}%")
            sys.stdout.flush()

    print()  # New line after progress bar
    return open_ports

def main():
    url = input("Enter the website URL or IP address: ")

    # Try to resolve the IP address from the URL
    try:
        ip_address = socket.gethostbyname(url)
        print(f"Resolving {url} to IP address: {ip_address}")
    except socket.gaierror:
        print("Invalid hostname or IP address.")
        return

    start_port = 1
    end_port = 65535  # Scanning all ports

    print(f"Scanning {url} ({ip_address}) from port {start_port} to {end_port}...")

    try:
        open_ports = scan_ports(ip_address, start_port, end_port)

        if open_ports:
            print(f"Open ports on {url} ({ip_address}): {open_ports}")
            print(f"Total open ports: {len(open_ports)}")
        else:
            print(f"No open ports found on {url} ({ip_address}).")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
