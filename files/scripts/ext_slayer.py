#!/usr/bin/env python3
import os
import sys
import sqlite3
import json

# Paths
STATE_DB_PATH = os.path.expanduser('~/.config/Code/User/globalStorage/state.vscdb')
EXTENSIONS_JSON_PATH = os.path.expanduser('~/.vscode/extensions/extensions.json') # FIX: path does not exist in the contestant's environment

# Load extensions list from extensions.json
try:
    with open(EXTENSIONS_JSON_PATH, 'r', encoding='utf-8') as f:
        extensions_data = json.load(f)
except FileNotFoundError:
    print(f"Error: extensions.json not found at {EXTENSIONS_JSON_PATH}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: failed to parse extensions.json: {e}", file=sys.stderr)
    sys.exit(1)

# Extract id & uuid pairs
extensions_to_disable = []
for entry in extensions_data:
    ident = entry.get('identifier', {})
    ext_id = ident.get('id')
    uuid = ident.get('uuid')
    if ext_id and uuid:
        extensions_to_disable.append({'id': ext_id, 'uuid': uuid})

if not extensions_to_disable:
    print('No extensions found in extensions.json to disable.')
    sys.exit(0)

# Functions for database operations
def get_disabled_extensions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'extensionsIdentifiers/disabled'")
    row = cursor.fetchone()
    if not row or not row[0]:
        return []
    try:
        # Remove .decode('utf-8') because row[0] is str
        return json.loads(row[0])
    except Exception:
        return []

def update_disabled_extensions(conn, disabled_list):
    cursor = conn.cursor()
    # Store JSON as text string, not bytes
    blob = json.dumps(disabled_list, separators=(',',':'))
    cursor.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        ('extensionsIdentifiers/disabled', blob)
    )
    conn.commit()


# Connect to state DB
if not os.path.isfile(STATE_DB_PATH):
    print(f"Error: state database not found at {STATE_DB_PATH}", file=sys.stderr)
    sys.exit(1)

conn = sqlite3.connect(STATE_DB_PATH)
current_disabled = get_disabled_extensions(conn)
existing_ids = {ext['id'] for ext in current_disabled}

# Append new entries, avoiding duplicates
for ext in extensions_to_disable:
    if ext['id'] not in existing_ids:
        current_disabled.append(ext)

# Save back to DB
update_disabled_extensions(conn, current_disabled)
conn.close()

# Touch main DB file to bump modification time
try:
    os.utime(STATE_DB_PATH, None)
except Exception:
    pass

print('Extensions successfully disabled based on extensions.json.')
