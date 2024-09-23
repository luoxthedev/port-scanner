import socket
import webbrowser
import threading

def scan_port(ip, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    except Exception as e:
        print(f"Error for port {port}: {e}")

def scan_all_ports(ip):
    open_ports = []
    threads = []
    for port in range(1000, 65536):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if open_ports:
        open_ports_response = input("Do you want to open the valid ports in the browser? (y/n): ")
        if open_ports_response.lower() == 'y':
            for port in open_ports:
                url = f"https://{ip}:{port}"
                print(f"Opening {url} in the browser.")
                webbrowser.open(url)

if __name__ == "__main__":
    ip_to_scan = input("Enter the IP address to scan: ")
    scan_all_ports(ip_to_scan)
