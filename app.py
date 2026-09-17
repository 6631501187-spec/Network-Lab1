import os
import socket
import paramiko
from flask import Flask, render_template, request

app = Flask(__name__)

SSH_USERNAME = os.getenv("SSH_USERNAME", "admin")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", "admin")
SSH_PORT = int(os.getenv("SSH_PORT", "22"))
SSH_TIMEOUT = int(os.getenv("SSH_TIMEOUT", "10"))


def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except OSError:
        return False


def execute_ssh_command(router_ip, command):
    if not validate_ip(router_ip):
        return False, "Invalid router IP address."

    if not command.strip():
        return False, "Router command cannot be empty."

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=router_ip,
            port=SSH_PORT,
            username=SSH_USERNAME,
            password=SSH_PASSWORD,
            timeout=SSH_TIMEOUT,
            banner_timeout=SSH_TIMEOUT,
            auth_timeout=SSH_TIMEOUT,
            look_for_keys=False,
            allow_agent=False,
        )

        stdin, stdout, stderr = client.exec_command(command, timeout=SSH_TIMEOUT)

        output = stdout.read().decode("utf-8", errors="replace")
        error = stderr.read().decode("utf-8", errors="replace")

        client.close()

        if error:
            return True, output + ("\n" if output else "") + error

        return True, output or "Command executed successfully (no output)."

    except paramiko.AuthenticationException:
        return False, "SSH authentication failed. Check SSH_USERNAME and SSH_PASSWORD."
    except paramiko.SSHException as e:
        return False, f"SSH error: {e}"
    except socket.timeout:
        return False, "Connection timed out."
    except OSError as e:
        return False, f"Network/connection error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"
    finally:
        try:
            client.close()
        except Exception:
            pass


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    success = None
    router_ip = ""
    command = ""

    if request.method == "POST":
        router_ip = request.form.get("router_ip", "").strip()
        command = request.form.get("command", "").strip()

        success, output = execute_ssh_command(router_ip, command)

    return render_template(
        "index.html",
        output=output,
        success=success,
        router_ip=router_ip,
        command=command,
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
