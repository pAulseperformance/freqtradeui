from flask import Flask
from rest_client import load_config, FtRestClient

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/start')
def start_bot():
    config = load_config("config.json")
    url = config.get("api_server", {}).get("server_url", "127.0.0.1")
    port = config.get("api_server", {}).get("listen_port", "8080")
    username = config.get("api_server", {}).get("username")
    password = config.get("api_server", {}).get("password")

    server_url = f"http://{url}:{port}"
    client = FtRestClient(server_url, username, password)

    return client.start()




if __name__ == '__main__':
    app.run(debug=True)
