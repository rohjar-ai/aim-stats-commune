import threading
import typer

from apscheduler.schedulers.background import BackgroundScheduler
from communex.cli._common import make_custom_context, ExtraCtxData
from communex.client import CommuneClient
from communex.misc import get_map_modules
from communex.types import ModuleInfoWithOptionalBalance
from datetime import datetime
from aim_stats_commune.discord_delegate import send_message

AIM_NET_UID: int = 17
COLLECT_INTERVAL: int = 5


class CommuneStatsCollector:

    def __init__(self):
        print("init stats collector")
        ctx = typer.Context
        ctx.obj = ExtraCtxData(output_json=False, use_testnet=False, yes_to_all=False)
        context = make_custom_context(ctx)
        self.client: CommuneClient = context.com_client()

        self._cache: None
        self._lock = threading.Lock()
        self._scheduler: BackgroundScheduler = BackgroundScheduler()

        self._scheduler.add_job(self._update_cache, 'interval', minutes=COLLECT_INTERVAL, next_run_time=datetime.now())
        self._scheduler.start()

        self._collect_attempts: int = 0

    def _collect(self) -> list[ModuleInfoWithOptionalBalance]:
        print(f"Collecting data: {datetime.now()}")
        map_modules = get_map_modules(self.client, netuid=AIM_NET_UID, include_balances=False)
        if not map_modules:
            send_message("Error getting modules using communex! Empty list returned. Retrying...")
            map_modules = get_map_modules(self.client, netuid=AIM_NET_UID, include_balances=False)
            if not map_modules:
                send_message("Error getting modules using comx! Empty list returned again.")

        print(f"Collecting completed.")
        return list(map_modules.values())

    def _update_cache(self):
        update: list[ModuleInfoWithOptionalBalance] = self._collect()
        with self._lock:
            self._cache = update

    def get(self) -> list[ModuleInfoWithOptionalBalance]:
        with self._lock:
            return self._cache

    def stop(self):
        self._scheduler.shutdown(wait=False)

