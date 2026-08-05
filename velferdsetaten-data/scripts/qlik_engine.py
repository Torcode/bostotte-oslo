"""Minimal Qlik Engine API-klient for Husbankens statistikkbank (public-proxy).

Brukes til å hente bostøttestatistikk direkte fra Qlik-appen bak
https://statistikk.husbanken.no/bostotte

Engine-API = JSON-RPC over WebSocket:
  wss://qlik.husbanken.no/public/app/{APP_ID}
"""
import json
import ssl
import time

import websocket

QLIK_HOST = "qlik.husbanken.no"
QLIK_PREFIX = "/public"
APP_ID = "ee185fe5-e94d-463e-bff8-cd1c5f2f566f"
ORIGIN = "https://statistikk.husbanken.no"


class QlikEngine:
    def __init__(self, identity=None):
        identity = identity or str(int(time.time() * 1000))
        url = f"wss://{QLIK_HOST}{QLIK_PREFIX}/app/{APP_ID}/identity/{identity}"
        self.ws = websocket.create_connection(
            url,
            origin=ORIGIN,
            sslopt={"cert_reqs": ssl.CERT_REQUIRED},
            timeout=60,
            header=["User-Agent: Mozilla/5.0 (X11; Linux x86_64)"],
        )
        self._id = 0
        # Server sender gjerne en OnConnected-notification først
        self.notifications = []
        self._drain_initial()

    def _drain_initial(self):
        self.ws.settimeout(5)
        try:
            while True:
                msg = json.loads(self.ws.recv())
                self.notifications.append(msg)
                if msg.get("method") == "OnConnected" or "result" in msg:
                    break
        except Exception:
            pass
        self.ws.settimeout(60)

    def call(self, method, handle=-1, params=None):
        self._id += 1
        req = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "handle": handle,
            "params": params if params is not None else [],
        }
        self.ws.send(json.dumps(req))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg["result"]
            # ignorér notifications/changes

    def open_doc(self):
        r = self.call("OpenDoc", -1, [APP_ID])
        return r["qReturn"]["qHandle"]

    def close(self):
        self.ws.close()


if __name__ == "__main__":
    eng = QlikEngine()
    print("connect-notifications:", json.dumps(eng.notifications)[:300])
    h = eng.open_doc()
    print("app handle:", h)
    layout = eng.call("GetAppLayout", h)
    print("app title:", layout["qLayout"].get("qTitle"))
    print("last reload:", layout["qLayout"].get("qLastReloadTime"))
    eng.close()
