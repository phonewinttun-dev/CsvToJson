import psycopg2
from psycopg2.extras import execute_values
from db_config import DB_CONFIG

INSERT_SQL = """
INSERT INTO locations
(region, township, quarter_village_tract, postal_code, is_deleted)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (postal_code) DO NOTHING;
"""

def insert_locations(records: list[dict]) -> int:
    """
    Bulk insert location records into PostgreSQL.
    Returns number of attempted inserts.
    """
    if not records:
        return 0

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        values = [
            (
                r["region"],
                r["township"],
                r["quarter_village_tract"],
                r["postal_code"],
                r["is_deleted"]
            )
            for r in records
        ]

        execute_values(cur, INSERT_SQL, values, page_size=1000)
        conn.commit()

        return len(values)

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
