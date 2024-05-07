from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

from communex.misc import get_map_modules
from communex.cli._common import (make_custom_context, ExtraCtxData)
from rich.console import Console
import typer
from typer import Context
from communex.types import ModuleInfoWithOptionalBalance


@app.route('/')
def home():
    # Fetch your data
    data = get_data()
    # Pass data to the template
    return render_template('index.html', data=data)

def get_data():
    # Your code to fetch data
    
    ctx = typer.Context
    ctx.obj = ExtraCtxData(output_json=False, use_testnet=False)


    context = make_custom_context(ctx)
    client = context.com_client()
    modules = get_map_modules(client, netuid=17, include_balances=False)

    data = []
    for module_info in modules.values():
        data.append(module_info['name'])
        print(f"NAME: {module_info['name']}, EMISSION: {module_info['emission']}")
    
    return modules.values()

if __name__ == '__main__':
    app.run(debug=True)
