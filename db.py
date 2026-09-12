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
