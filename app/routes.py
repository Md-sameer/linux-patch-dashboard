from flask import render_template
from app import app
from app.system_info import get_system_info
from app.inventory import load_servers
from app.remote_info import get_remote_system_info
from app.database import get_telemetry_history

@app.route("/")
def home():

    local_system = get_system_info()

    servers = load_servers()

    remote_servers = []

    for server in servers:

        remote_data = get_remote_system_info(server)

        remote_servers.append(remote_data)

    total_nodes = len(remote_servers)

    online_nodes = len([
        s for s in remote_servers
        if s["status"] == "Online"
    ])

    offline_nodes = len([
        s for s in remote_servers
        if s["status"] == "Offline"
    ])

    total_updates = sum([
        int(s["updates"])
        for s in remote_servers
        if str(s["updates"]).isdigit()
    ])

    last_updated = remote_servers[0]["last_check"] \
        if remote_servers else "No Data"

    return render_template(
        "index.html",
        system_info=local_system,
        remote_servers=remote_servers,
        total_nodes=total_nodes,
        online_nodes=online_nodes,
        offline_nodes=offline_nodes,
        total_updates=total_updates,
        last_updated=last_updated
    )

@app.route("/history")
def history():

    telemetry_history = get_telemetry_history()

    return render_template(
        "history.html",
        telemetry_history=telemetry_history
    )

@app.route("/online")
def online_nodes():

    servers = load_servers()

    online_servers = []

    for server in servers:

        remote_data = get_remote_system_info(server)

        if remote_data["status"] == "Online":

            online_servers.append(remote_data)

    return render_template(
        "online.html",
        servers=online_servers
    )

@app.route("/offline")
def offline_nodes_page():

    servers = load_servers()

    offline_servers = []

    for server in servers:

        remote_data = get_remote_system_info(server)

        if remote_data["status"] == "Offline":

            offline_servers.append(remote_data)

    return render_template(
        "offline.html",
        servers=offline_servers
    )

@app.route("/node/<hostname>")
def node_details(hostname):

    servers = load_servers()

    for server in servers:

        remote_data = get_remote_system_info(server)

        if remote_data["hostname"] == hostname:

            return render_template(
                "node_details.html",
                server=remote_data
            )

    return "Node Not Found", 404
