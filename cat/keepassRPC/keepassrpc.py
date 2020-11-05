import asyncio
import websockets
import json
import hashlib

async def main():
    #default port is used
    uri = "ws://localhost:12546"

    srpc = {
        "stage": "identifyToServer",
        "I": "6780a1fd-99c5-4937-b6d9-ade4b68fa04e",
        "A": "0",
        "securityLevel": 2
    }
    payload = {
        "protocol": "setup",
        "srp": srpc,
        "key": None,
        "version":131072,
        "features": ["KPRPC_FEATURE_VERSION_1_6","KPRPC_FEATURE_WARN_USER_WHEN_FEATURE_MISSING","KPRPC_FEATURE_BROWSER_HOSTED","BROWSER_SETTINGS_SYNC"],
        "clientTypeId":"keefox",
        "clientDisplayName":"Kee",
        "clientDisplayDescription":"A browser addon that securely enables automatic login to most websites. Previously known asKeeFox."
    }

    pl = json.dumps(payload)

    print(pl)

    async with websockets.connect(uri) as websocket:
        if websocket.open:
            print("open\n")
            await websocket.send(pl)
            response = await websocket.recv()

            data = json.load(response)
            h = hashlib.sha256()
            h.update(0)
            h.update(data["B"])
            h.update(0)
            m = h.digest()


asyncio.get_event_loop().run_until_complete(main())