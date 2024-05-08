from flask import Flask, jsonify
import typer
from communex.misc import get_map_modules
from communex.cli._common import make_custom_context, ExtraCtxData
from communex.types import ModuleInfoWithOptionalBalance
from flask_cors import CORS
import json

app = Flask(__name__, template_folder='.')
CORS(app)

@app.route('/')
def home():
    data = get_data()
    return jsonify(data)

def get_data():
    ctx = typer.Context
    ctx.obj = ExtraCtxData(output_json=False, use_testnet=False)
    context = make_custom_context(ctx)
    client = context.com_client()
    modules = get_map_modules(client, netuid=17, include_balances=False)
    
    return list(modules.values())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)