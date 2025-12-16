# nodes/checkpoint.py

import sqlite3
import json
import uuid
import os

def checkpoint_node(state):
    print("CHECKPOINT reached — pausing workflow")

    checkpoint_id = str(uuid.uuid4())

    # Always use absolute path
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "demo.db")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ALWAYS create table first
    cur.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            checkpoint_id TEXT PRIMARY KEY,
            state_json TEXT,
            status TEXT
        )
    """)

    cur.execute(
        "INSERT INTO checkpoints (checkpoint_id, state_json, status) VALUES (?, ?, ?)",
        (checkpoint_id, json.dumps(state), "PENDING")
    )

    conn.commit()
    conn.close()

    state["hitl_checkpoint_id"] = checkpoint_id

    print(f"Workflow paused at checkpoint: {checkpoint_id}")

    return state
