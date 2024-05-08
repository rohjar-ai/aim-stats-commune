from flask import Flask, jsonify
import typer
from communex.misc import get_map_modules
from communex.cli._common import make_custom_context, ExtraCtxData
from communex.types import ModuleInfoWithOptionalBalance
from flask_cors import CORS
import json

from apscheduler.schedulers.background import BackgroundScheduler
import threading
import time

app = Flask(__name__, template_folder='.')
CORS(app)

scheduler = BackgroundScheduler()
data_lock = threading.Lock()
shared_data = None

with app.app_context():
    scheduler.start()

def heavy_task():
    global shared_data
    print("Collecting data")
    collected_data = get_data()
    with data_lock:
        shared_data = collected_data
    print("Collecting completed.")

@app.route('/')
def index():
    with data_lock:
        data_to_show = shared_data if shared_data else "No data collected yet."
    return f"Hello, World! Here's the latest update: {data_to_show}"

@scheduler.scheduled_job('interval', minutes=10)
def scheduled_job():
    heavy_task()

@app.cli.command()
def shutdown():
    scheduler.shutdown(wait=False)


@app.route('/')
def home():
    with data_lock:
        data_to_show = shared_data if shared_data else "No data collected yet."
    return jsonify(data_to_show)

def get_data():
    ctx = typer.Context
    ctx.obj = ExtraCtxData(output_json=False, use_testnet=False)
    context = make_custom_context(ctx)
    client = context.com_client()
    modules = get_map_modules(client, netuid=17, include_balances=False)
    
    return list(modules.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)