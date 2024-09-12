import random
import socket
import threading
import time

NETWORK_RANGE = "192.168.1.{}"

VULNERABLE_SERVICES = {
    "sendmail": 25,
    "finger": 79,
    "rexec": 512,
    "rsh": 514
}


def scan_target(target_ip):
    """ Simulate port scanning to find open ports on the target machine. """
    open_ports = []
    print(f"Scanning {target_ip} for open ports...")

    for service, port in VULNERABLE_SERVICES.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    print(f"Port {port} (service: {service}) open on {target_ip}")
                    open_ports.append(port)
        except socket.error as e:
            print(f"Error scanning {target_ip} on port {port}: {e}")

    return open_ports


def exploit_service(service_name, target_host, port):
    """ Simulate an exploit for a vulnerable service. """
    try:
        if service_name == "sendmail":
            payload = "MAIL FROM: <worm@worm.com>\r\n"
        elif service_name == "finger":
            payload = "finger worm\r\n"
        else:
            payload = "exploit payload for " + service_name + "\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_host, port))
            s.sendall(payload.encode())
            print(f"Successfully exploited {service_name} on {target_host}:{port}")

            # Simulate dropping a payload (replication)
            install_payload(target_host)
    except socket.error as e:
        print(f"Failed to exploit {service_name} on {target_host}:{port}: {e}")


def install_payload(target_ip):
    """ Simulate dropping a payload on the infected machine. """
    print(f"Installing worm on {target_ip}...")

    try:
        fake_payload = f"Worm payload on {target_ip}\n"
        with open(f"/tmp/worm_{target_ip}.txt", "w", encoding="utf-8") as f:
            f.write(fake_payload)
        print(f"Worm installed on {target_ip}.")
    except IOError as e:
        print(f"Failed to install worm on {target_ip}: {e}")


def replicate():
    """ Simulate the worm's replication process. """
    while True:
        target_ip = NETWORK_RANGE.format(random.randint(1, 254))
        print(f"Attempting to replicate to {target_ip}...")

        open_ports = scan_target(target_ip)
        if open_ports:
            for port in open_ports:
                for service, service_port in VULNERABLE_SERVICES.items():
                    if service_port == port:
                        exploit_service(service, target_ip, port)

        time.sleep(random.randint(5, 15))


def main():
    """ Main function to start the Morris worm simulation. """
    print("Morris Worm simulation started...")

    # Start multiple threads to simulate worm replication across different machines
    for _ in range(3):  # Simulate 3 instances of the worm
        thread = threading.Thread(target=replicate)
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(60)  # Simulate worm staying active
    except KeyboardInterrupt:
        print("Worm terminated by user.")


if __name__ == "__main__":
    main()
