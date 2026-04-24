import requests
import time
import zipfile
import os
import signal

INTERVAL = 7.5 # you can change this
BACKUP_DIR = "logs" # don't change this unless you know what you are doing

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup(previous_data):
    try:
        current_data = requests.get(
            'https://data.vatsim.net/v3/vatsim-data.json',
            timeout=5
        )
    except requests.RequestException:
        print("Request failed")
        return previous_data

    if current_data.status_code != 200:
        print("Request failed")
        return previous_data

    current_data_json = current_data.json()
    current_ts = current_data_json.get("general", {}).get("update_timestamp")

    if not current_ts:
        print("Missing timestamp, skipping")
        return previous_data

    if previous_data is not None:
        prev_ts = previous_data.json().get("general", {}).get("update_timestamp")
        if prev_ts == current_ts:
            print("Backup skipped")
            return previous_data

    zip_path = os.path.join(BACKUP_DIR, f"{current_ts}.zip")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{current_ts}.json", current_data.text)

    print("Backup saved:", zip_path)
    return current_data

def shutdown(signum, frame):
    global running
    print("Shutting down...")
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

next_run = time.monotonic()
data = None
running = True

while running:
    next_run += INTERVAL
    data = backup(data)

    sleep_time = next_run - time.monotonic()
    if sleep_time > 0:
        time.sleep(sleep_time)