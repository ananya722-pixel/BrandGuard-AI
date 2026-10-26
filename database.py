import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "brandguard.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                content TEXT NOT NULL,
                guidelines TEXT NOT NULL,
                rule_findings TEXT NOT NULL,
                ai_result TEXT NOT NULL,
                decision TEXT NOT NULL DEFAULT 'Pending',
                reviewer_comment TEXT DEFAULT ''
            )
            """
        )


def save_review(content, guidelines, rule_findings, ai_result):
    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reviews (
                created_at,
                content,
                guidelines,
                rule_findings,
                ai_result
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                created_at,
                content,
                guidelines,
                json.dumps(rule_findings, ensure_ascii=False),
                json.dumps(ai_result, ensure_ascii=False),
            ),
        )

        return cursor.lastrowid


def update_review_decision(review_id, decision, comment):
    allowed_decisions = {
        "Pending",
        "Approved",
        "Rejected",
        "Changes Requested",
    }

    if decision not in allowed_decisions:
        raise ValueError("Invalid review decision.")

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE reviews
            SET decision = ?, reviewer_comment = ?
            WHERE id = ?
            """,
            (decision, comment, review_id),
        )


def get_reviews(limit=50):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM reviews
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    reviews = []

    for row in rows:
        review = dict(row)

        review["rule_findings"] = json.loads(
            review["rule_findings"]
        )

        review["ai_result"] = json.loads(
            review["ai_result"]
        )

        reviews.append(review)

    return reviews


initialize_db()