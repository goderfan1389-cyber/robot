# ══════════════════════════════════════════════════════════════
#  db.py — لایه‌ی ذخیره‌سازی PostgreSQL (جایگزین فایل‌های JSON)
# ──────────────────────────────────────────────────────────────
#  هر فایل جیسون قبلی (users_data.json، orders_data.json، ...)
#  حالا یک ردیف در جدول bot_documents است: doc_name + data(JSONB).
#  این یعنی تمام توابع load_x()/save_x() در handlers.py و
#  admin_panel.py بدون تغییرِ ساختار داده یا منطق کسب‌وکار،
#  فقط پشت‌صحنه از Postgres به‌جای دیسک استفاده می‌کنند.
# ══════════════════════════════════════════════════════════════
import os
import json
import threading
import time

try:
    import psycopg2
    import psycopg2.pool
    import psycopg2.extras
except ImportError:  # pragma: no cover
    psycopg2 = None

DATABASE_URL = os.environ.get("DATABASE_URL")

_pool = None
_pool_lock = threading.Lock()


def _get_pool():
    global _pool
    if _pool is not None:
        return _pool
    with _pool_lock:
        if _pool is None:
            if not DATABASE_URL:
                raise RuntimeError(
                    "DATABASE_URL تنظیم نشده است! در Railway باید سرویس PostgreSQL را "
                    "به پروژه اضافه کنی تا این متغیر خودکار ساخته شود."
                )
            if psycopg2 is None:
                raise RuntimeError(
                    "پکیج psycopg2-binary نصب نیست. آن را به requirements.txt اضافه کن."
                )
            _pool = psycopg2.pool.ThreadedConnectionPool(1, 10, dsn=DATABASE_URL)
    return _pool


def _with_conn(fn, retries=2):
    """یک عملیات را با یک کانکشن از pool اجرا می‌کند؛ روی قطعی اتصال یک‌بار دوباره تلاش می‌کند."""
    last_err = None
    for attempt in range(retries + 1):
        pool = _get_pool()
        conn = pool.getconn()
        try:
            result = fn(conn)
            conn.commit()
            pool.putconn(conn)
            return result
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            try:
                pool.putconn(conn, close=True)
            except Exception:
                pass
            last_err = e
            if attempt < retries:
                time.sleep(0.3)
                continue
            raise
    raise last_err


def init_db():
    """یک‌بار در ابتدای اجرای ربات صدا زده می‌شود تا جدول لازم ساخته شود (اگر نبود)."""
    def _run(conn):
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bot_documents (
                    doc_name   TEXT PRIMARY KEY,
                    data       JSONB NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
            """)
    _with_conn(_run)


def load_json(name, default):
    """معادل باز کردن فایل json قدیمی: مقدار را برمی‌گرداند یا default (اگر ردیفی نبود)."""
    def _run(conn):
        with conn.cursor() as cur:
            cur.execute("SELECT data FROM bot_documents WHERE doc_name = %s", (name,))
            row = cur.fetchone()
            if row is None:
                return None
            return row[0]
    try:
        result = _with_conn(_run)
    except Exception as e:
        print(f"[db.load_json] خطا در خواندن '{name}': {e}")
        result = None
    if result is None:
        return default() if callable(default) else default
    return result


def save_json(name, data):
    """معادل نوشتن فایل json قدیمی: کل داده را در ردیف مربوطه ذخیره (upsert) می‌کند."""
    payload = json.dumps(data, ensure_ascii=False)

    def _run(conn):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO bot_documents (doc_name, data, updated_at)
                VALUES (%s, %s::jsonb, now())
                ON CONFLICT (doc_name) DO UPDATE
                SET data = EXCLUDED.data, updated_at = now()
            """, (name, payload))
    try:
        _with_conn(_run)
    except Exception as e:
        print(f"[db.save_json] خطا در نوشتن '{name}': {e}")


def list_docs():
    """لیست تمام doc_name های موجود (معادل لیست فایل‌های json روی دیسک)."""
    def _run(conn):
        with conn.cursor() as cur:
            cur.execute("SELECT doc_name FROM bot_documents ORDER BY doc_name")
            return [r[0] for r in cur.fetchall()]
    try:
        return _with_conn(_run)
    except Exception as e:
        print(f"[db.list_docs] خطا: {e}")
        return []


def doc_has_data(name):
    """معادل چک‌کردن فایل خالی/ناموجود قدیمی."""
    data = load_json(name, None)
    if data is None or data == {} or data == []:
        return False
    return True

def export_database_sql():
    """ساخت بکاپ SQL امن از PostgreSQL - بدون تراکنش یکپارچه"""
    from psycopg2 import sql
    from psycopg2.extras import Json

    def _run(conn):
        output = []
        output.append("-- ARKA PostgreSQL FULL BACKUP")
        output.append("-- Generated automatically by ARKA Bot")
        output.append("")
        output.append("-- Each statement is independent (no wrapping BEGIN/COMMIT)")
        output.append("")

        with conn.cursor() as cur:

            # 1) Sequences
            cur.execute("""
                SELECT sequence_name
                FROM information_schema.sequences
                WHERE sequence_schema = 'public'
                ORDER BY sequence_name;
            """)
            sequences = [r[0] for r in cur.fetchall()]

            for seq in sequences:
                output.append(f'CREATE SEQUENCE IF NOT EXISTS "{seq}";')
            output.append("")

            # 2) Tables
            cur.execute("""
                SELECT c.oid, c.relname
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = 'public' AND c.relkind = 'r'
                ORDER BY c.relname;
            """)
            tables = cur.fetchall()

            for table_oid, table_name in tables:
                cur.execute("""
                    SELECT a.attname,
                           pg_catalog.format_type(a.atttypid, a.atttypmod),
                           a.attnotnull,
                           pg_get_expr(ad.adbin, ad.adrelid)
                    FROM pg_attribute a
                    LEFT JOIN pg_attrdef ad
                        ON a.attrelid = ad.adrelid AND a.attnum = ad.adnum
                    WHERE a.attrelid = %s
                      AND a.attnum > 0
                      AND NOT a.attisdropped
                    ORDER BY a.attnum;
                """, (table_oid,))
                columns = cur.fetchall()

                output.append(f'CREATE TABLE IF NOT EXISTS "{table_name}" (')
                column_lines = []
                for col_name, data_type, not_null, default_value in columns:
                    line = f'    "{col_name}" {data_type}'
                    if default_value:
                        line += f' DEFAULT {default_value}'
                    if not_null:
                        line += ' NOT NULL'
                    column_lines.append(line)
                output.append(",\n".join(column_lines))
                output.append(");")
                output.append("")

            # 3) Constraints (DROP IF EXISTS first)
            cur.execute("""
                SELECT conrelid::regclass::text AS table_name,
                       conname,
                       pg_get_constraintdef(oid)
                FROM pg_constraint
                WHERE contype IN ('p', 'u', 'f')
                  AND connamespace = 'public'::regnamespace
                ORDER BY conrelid::regclass::text, conname;
            """)
            constraints = cur.fetchall()

            for table_name, constraint_name, definition in constraints:
                # حذف constraint موجود (اگه باشه)
                output.append(
                    f'ALTER TABLE "{table_name}" '
                    f'DROP CONSTRAINT IF EXISTS "{constraint_name}";'
                )
                output.append(
                    f'ALTER TABLE "{table_name}" '
                    f'ADD CONSTRAINT "{constraint_name}" {definition};'
                )
            output.append("")

            # 4) Data — با ON CONFLICT برای جلوگیری از خطای duplicate
            for table_oid, table_name in tables:
                cur.execute(
                    sql.SQL('SELECT * FROM {}').format(
                        sql.Identifier(table_name)
                    )
                )
                rows = cur.fetchall()
                if not rows:
                    continue

                column_names = [desc.name for desc in cur.description]
                cur.execute("""
                    SELECT a.attname,
                           pg_catalog.format_type(a.atttypid, a.atttypmod)
                    FROM pg_attribute a
                    WHERE a.attrelid = %s AND a.attnum > 0 AND NOT a.attisdropped
                    ORDER BY a.attnum;
                """, (table_oid,))
                column_types = {n: t for n, t in cur.fetchall()}

                columns_sql = ", ".join(f'"{n}"' for n in column_names)

                for row in rows:
                    values = []
                    for column_name, value in zip(column_names, row):
                        column_type = column_types.get(column_name, "").lower()
                        if column_type in ("json", "jsonb"):
                            if value is None:
                                values.append("NULL")
                            else:
                                json_value = json.dumps(value, ensure_ascii=False)
                                escaped = json_value.replace("\\", "\\\\").replace("'", "''")
                                cast = "::jsonb" if column_type == "jsonb" else "::json"
                                values.append(f"E'{escaped}'{cast}")
                        else:
                            values.append(
                                cur.mogrify("%s", (value,)).decode("utf-8")
                            )

                    values_sql = ", ".join(values)
                    output.append(
                        f'INSERT INTO "{table_name}" ({columns_sql}) '
                        f'VALUES ({values_sql}) '
                        f'ON CONFLICT DO NOTHING;'
                    )
                output.append("")

            # 5) Sequence values (با EXISTS check)
            for seq in sequences:
                try:
                    cur.execute(
                        sql.SQL('SELECT last_value, is_called FROM {}').format(
                            sql.Identifier(seq)
                        )
                    )
                    seq_row = cur.fetchone()
                    if seq_row:
                        last_value, is_called = seq_row
                        output.append(
                            f"SELECT setval('public.{seq}', {last_value}, "
                            f"{str(is_called).upper()});"
                        )
                except Exception:
                    pass
            output.append("")

        return "\n".join(output)

    return _with_conn(_run)
