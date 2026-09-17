# Router SSH Python App

A Flask web application that connects to a router using Paramiko SSH and executes a command entered through the web interface.

## Project structure

```text
python/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── README.md
└── templates/
    └── index.html
```

## 1. Change SSH credentials

Edit `docker-compose.yml`:

```yaml
environment:
  SSH_USERNAME: "admin"
  SSH_PASSWORD: "admin"
  SSH_PORT: "22"
  SSH_TIMEOUT: "10"
```

Use the username/password configured on your router.

## 2. Start

From the project directory:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

## 3. Open the web interface

From the Ubuntu machine:

```text
http://localhost:5000
```

From another machine on the same network:

```text
http://UBUNTU_IP:5000
```

Example:

```text
http://192.168.1.100:5000
```

## 4. Test

Enter:

Router IP:
```text
192.168.1.1
```

Command:
```text
show version
```

Then click **Execute Command**.

## Important

The router must have SSH enabled and must be reachable from the Docker container.

For a Cisco IOS router, the SSH configuration typically needs an SSH-capable IOS image, a hostname/domain name, a local user, RSA keys, and VTY lines configured for SSH.

This application uses `exec_command()`, which is suitable for one-shot commands such as:

```text
show version
show ip interface brief
show running-config
show interfaces
```

Interactive configuration workflows such as:

```text
enable
configure terminal
interface GigabitEthernet0/0
ip address ...
```

are different because they require an interactive SSH shell and command sequencing.
