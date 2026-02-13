import psycopg2
from psycopg2.extras import execute_values
from db_config import DB_CONFIG

INSERT_LOCATIONS = """
INSERT INTO locations
(region, township, quarter_village_tract, postal_code, region_id)
VALUES %s
ON CONFLICT (postal_code) DO NOTHING;
"""

INSERT_REGION = """INSERT INTO regions
(name) VALUES %s
ON CONFLICT (name) DO NOTHING;"""

def sync_regions(region_names: list) -> dict:
    """Inserts unique regions and returns a mapping of {name: uuid}"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # 1. Insert unique regions
        region_tuples = [(name,) for name in set(region_names)]
        execute_values(cur, INSERT_REGION, region_tuples)

        # 2. Fetch all regions to get their generated UUIDs
        cur.execute("SELECT name, id FROM regions")
        region_map = {name: id for name, id in cur.fetchall()}

        conn.commit()
        return region_map
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def insert_locations(records: list[dict], region_map: dict) -> int:
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
                r["region_id"]
            )
            for r in records
        ]

        execute_values(cur, INSERT_LOCATIONS, values)
        conn.commit()

        return len(values)

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
