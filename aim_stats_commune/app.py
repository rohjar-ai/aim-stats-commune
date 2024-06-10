from commune_stats_collector import CommuneStatsCollector
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)
stats_collector = CommuneStatsCollector()


@app.route('/')
def home():
    subnet_data = stats_collector.get()
    return jsonify(subnet_data)


@app.cli.command()
def shutdown():
    stats_collector.stop()


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
