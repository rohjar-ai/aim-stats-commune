import threading
import typer

from apscheduler.schedulers.background import BackgroundScheduler
from communex.cli._common import make_custom_context, ExtraCtxData
from communex.misc import get_map_modules
from datetime import datetime
from aim_stats_commune.discord_delegate import send_message
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

scheduler = BackgroundScheduler()
data_lock = threading.Lock()
shared_data = None


def collect_subnet_data():
    ctx = typer.Context
    ctx.obj = ExtraCtxData(output_json=False, use_testnet=False, yes_to_all=False)
    context = make_custom_context(ctx)
    client = context.com_client()

    modules = get_map_modules(client, netuid=17, include_balances=False)
    if not modules:
        send_message("Error getting modules using comx! Empty list returned. Retrying...")
        modules = get_map_modules(client, netuid=17, include_balances=False)
        if not modules:
            send_message("Error getting modules using comx! Empty list returned again.")
    return list(modules.values())


def collect_in_background():
    global shared_data
    print(f"Collecting data: {datetime.now()}")
    collected_data = collect_subnet_data()
    with data_lock:
        shared_data = collected_data
    print("Collecting completed.")


with app.app_context():
    scheduler.add_job(collect_in_background, 'date')
    scheduler.start()


@app.route('/')
def home():
    with data_lock:
        subnet_data = shared_data if shared_data else "Collecting data..."
    return jsonify(subnet_data)


@scheduler.scheduled_job('interval', minutes=5)
def scheduled_job():
    collect_in_background()


@app.cli.command()
def shutdown():
    scheduler.shutdown(wait=False)


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
