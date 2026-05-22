from app.inventory import load_servers
from app.remote_info import get_remote_system_info
from app.database import insert_telemetry


def main():

    servers = load_servers()

    for server in servers:

        remote_data = get_remote_system_info(server)

        insert_telemetry(remote_data)

        print(f"Collected telemetry from {server['hostname']}")


if __name__ == "__main__":
    main()
