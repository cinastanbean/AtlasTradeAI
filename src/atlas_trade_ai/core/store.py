from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS counters (
                prefix TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                customer_level TEXT,
                business_type TEXT,
                owner_id TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                order_no TEXT NOT NULL,
                customer_id TEXT,
                customer_name TEXT,
                business_type TEXT,
                current_status TEXT,
                sub_status TEXT,
                risk_level TEXT,
                planned_delivery_date TEXT,
                payment_status TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_type TEXT,
                task_title TEXT,
                related_order_id TEXT,
                assignee_id TEXT,
                priority TEXT,
                task_status TEXT,
                created_at TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS exceptions (
                exception_id TEXT PRIMARY KEY,
                exception_type TEXT,
                exception_level TEXT,
                related_order_id TEXT,
                source_event_id TEXT,
                owner_id TEXT,
                exception_status TEXT,
                created_at TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT,
                order_id TEXT,
                customer_id TEXT,
                event_time TEXT,
                source_system TEXT,
                created_at TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS agent_runs (
                run_id TEXT PRIMARY KEY,
                agent_name TEXT,
                trigger_event_type TEXT,
                order_id TEXT,
                created_at TEXT,
                data TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notifications (
                notification_id TEXT PRIMARY KEY,
                channel TEXT,
                template_code TEXT,
                sent INTEGER,
                created_at TEXT,
                data TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(current_status);
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(task_status);
            CREATE INDEX IF NOT EXISTS idx_tasks_order ON tasks(related_order_id);
            CREATE INDEX IF NOT EXISTS idx_exceptions_order ON exceptions(related_order_id);
            CREATE INDEX IF NOT EXISTS idx_events_order ON events(order_id);
            CREATE INDEX IF NOT EXISTS idx_agent_runs_order ON agent_runs(order_id);
            """
        )
        self.conn.commit()

    def reset(self) -> None:
        cursor = self.conn.cursor()
        cursor.executescript(
            """
            DELETE FROM customers;
            DELETE FROM orders;
            DELETE FROM tasks;
            DELETE FROM exceptions;
            DELETE FROM events;
            DELETE FROM agent_runs;
            DELETE FROM notifications;
            DELETE FROM counters;
            """
        )
        self.conn.commit()

    def next_id(self, prefix: str) -> str:
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT value FROM counters WHERE prefix = ?",
            (prefix,),
        ).fetchone()
        value = 1 if row is None else int(row["value"]) + 1
        cursor.execute(
            """
            INSERT INTO counters(prefix, value)
            VALUES(?, ?)
            ON CONFLICT(prefix) DO UPDATE SET value = excluded.value
            """,
            (prefix, value),
        )
        self.conn.commit()
        return f"{prefix}_{value:03d}"

    def seed(self, payload: dict[str, list[dict[str, Any]]]) -> None:
        self.reset()
        for item in payload.get("customers", []):
            self.save_customer(item)
        for item in payload.get("orders", []):
            self.save_order(item)
        for item in payload.get("tasks", []):
            self.save_task(item)
        for item in payload.get("exceptions", []):
            self.save_exception(item)
        for item in payload.get("events", []):
            self.save_event(item)
        for item in payload.get("agent_runs", []):
            self.save_agent_run(item)
        for item in payload.get("notifications", []):
            self.save_notification(item)
        self._seed_counters(payload)

    def _seed_counters(self, payload: dict[str, list[dict[str, Any]]]) -> None:
        mapping = {
            "task": payload.get("tasks", []),
            "exception": payload.get("exceptions", []),
            "event": payload.get("events", []),
            "notification": payload.get("notifications", []),
            "agent_run": payload.get("agent_runs", []),
        }
        cursor = self.conn.cursor()
        for prefix, items in mapping.items():
            cursor.execute(
                "INSERT OR REPLACE INTO counters(prefix, value) VALUES(?, ?)",
                (prefix, len(items)),
            )
        self.conn.commit()

    def _dump(self, item: dict[str, Any]) -> str:
        return json.dumps(item, ensure_ascii=False)

    def _load_row(self, row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        return json.loads(row["data"])

    def save_customer(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO customers(
                customer_id, customer_name, customer_level, business_type, owner_id, data
            ) VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                item["customer_id"],
                item["customer_name"],
                item.get("customer_level"),
                item.get("business_type"),
                item.get("owner_id"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_customers(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM customers ORDER BY customer_id"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def get_customer(self, customer_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT data FROM customers WHERE customer_id = ?",
            (customer_id,),
        ).fetchone()
        if row is None:
            raise KeyError(customer_id)
        return json.loads(row["data"])

    def save_order(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO orders(
                order_id, order_no, customer_id, customer_name, business_type,
                current_status, sub_status, risk_level, planned_delivery_date,
                payment_status, data
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["order_id"],
                item["order_no"],
                item.get("customer_id"),
                item.get("customer_name"),
                item.get("business_type"),
                item.get("current_status"),
                item.get("sub_status"),
                item.get("risk_level"),
                item.get("planned_delivery_date"),
                item.get("payment_status"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_orders(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM orders ORDER BY order_no"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def get_order(self, order_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT data FROM orders WHERE order_id = ?",
            (order_id,),
        ).fetchone()
        if row is None:
            raise KeyError(order_id)
        return json.loads(row["data"])

    def save_task(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO tasks(
                task_id, task_type, task_title, related_order_id, assignee_id,
                priority, task_status, created_at, data
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["task_id"],
                item.get("task_type"),
                item.get("task_title"),
                item.get("related_order_id"),
                item.get("assignee_id"),
                item.get("priority"),
                item.get("task_status"),
                item.get("created_at"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_tasks(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM tasks ORDER BY task_id DESC"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def save_exception(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO exceptions(
                exception_id, exception_type, exception_level, related_order_id,
                source_event_id, owner_id, exception_status, created_at, data
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["exception_id"],
                item.get("exception_type"),
                item.get("exception_level"),
                item.get("related_order_id"),
                item.get("source_event_id"),
                item.get("owner_id"),
                item.get("exception_status"),
                item.get("created_at"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_exceptions(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM exceptions ORDER BY exception_id DESC"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def save_event(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO events(
                event_id, event_type, order_id, customer_id, event_time,
                source_system, created_at, data
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["event_id"],
                item.get("event_type"),
                item.get("order_id"),
                item.get("customer_id"),
                item.get("event_time"),
                item.get("source_system"),
                item.get("created_at"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_events(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM events ORDER BY COALESCE(event_time, created_at, event_id) DESC"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def save_agent_run(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO agent_runs(
                run_id, agent_name, trigger_event_type, order_id, created_at, data
            ) VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                item["run_id"],
                item.get("agent_name"),
                item.get("trigger_event_type"),
                item.get("order_id"),
                item.get("created_at"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_agent_runs(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM agent_runs ORDER BY run_id DESC"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def save_notification(self, item: dict[str, Any]) -> dict[str, Any]:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO notifications(
                notification_id, channel, template_code, sent, created_at, data
            ) VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                item["notification_id"],
                item.get("channel"),
                item.get("template_code"),
                1 if item.get("sent") else 0,
                item.get("created_at"),
                self._dump(item),
            ),
        )
        self.conn.commit()
        return item

    def list_notifications(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT data FROM notifications ORDER BY notification_id DESC"
        ).fetchall()
        return [json.loads(row["data"]) for row in rows]
