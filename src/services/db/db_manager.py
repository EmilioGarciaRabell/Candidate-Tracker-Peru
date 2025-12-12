import os
from typing import Any, Dict, List, Optional, Sequence, Union

from dotenv import load_dotenv
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import OperationalError, InterfaceError

Param = Union[str, int, float, None]


class Database:

    _pool: Optional[ThreadedConnectionPool] = None

    def __init__(self, table: str):
        load_dotenv()
        self.table = table

        if Database._pool is None:
            db_url = os.environ.get("DATABASE_URL")
            if not db_url:
                raise RuntimeError("DATABASE_URL is not set")

            # Make sure DATABASE_URL includes sslmode=require for Neon, e.g.:
            # postgresql://user:pass@host/dbname?sslmode=require
            Database._pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                dsn=db_url,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=3,
            )

    # ------------------------ Getters / Setters ------------------------

    def get_table(self) -> str:
        return self.table

    def set_table(self, table: str) -> None:
        self.table = table

    # ------------------------ Connection Helpers ------------------------

    def _get_conn(self):
        """Borrow a *healthy* connection from the pool."""
        if Database._pool is None:
            raise RuntimeError("Connection pool not initialized")

        conn = Database._pool.getconn()

        # Health check: Neon may have closed idle connections.
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        except (OperationalError, InterfaceError):
            # This connection is dead. Drop it from the pool and grab a fresh one.
            Database._pool.putconn(conn, close=True)
            conn = Database._pool.getconn()

        return conn

    def _release_conn(self, conn, *, close: bool = False):
        """Return connection to the pool, optionally closing it."""
        if Database._pool:
            Database._pool.putconn(conn, close=close)

    # ------------------------ Internal query helpers ------------------------

    def _run_select(
        self,
        sql_q: str,
        params: Sequence[Param] = (),
    ) -> List[Dict[str, Any]]:
        """Run a SELECT with a small retry on DB connection errors."""
        last_exc: Optional[Exception] = None

        for attempt in range(2):  # try at most twice
            conn = self._get_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(sql_q, params)
                    colnames = [c[0] for c in cur.description]
                    rows = cur.fetchall()
                self._release_conn(conn)
                return [dict(zip(colnames, r)) for r in rows]
            except (OperationalError, InterfaceError) as e:
                last_exc = e
                # Kill this connection and retry with a new one
                self._release_conn(conn, close=True)
                if attempt == 1:
                    raise  # second failure → bubble up

        if last_exc:
            raise last_exc
        return []

    # ------------------------ Public query API ------------------------

    def select(
        self,
        columns: Union[str, List[str]],
        where_sql: Optional[str] = None,
        params: Sequence[Param] = (),
        order_by: Optional[str] = None,
        desc: bool = True,
    ) -> List[Dict[str, Any]]:
        """Simple SELECT helper returning list of dicts."""
        cols = columns if isinstance(columns, str) else ", ".join(columns)
        sql_q = f"SELECT {cols} FROM {self.table}"
        if where_sql:
            sql_q += f" WHERE {where_sql}"
        if order_by:
            sql_q += f" ORDER BY {order_by} {'DESC' if desc else 'ASC'}"

        return self._run_select(sql_q, params)

    def execute(self, sql: str, params: Sequence[Param] = ()) -> None:
        """Execute INSERT/UPDATE/DELETE safely with commit + retry."""
        last_exc: Optional[Exception] = None

        for attempt in range(2):
            conn = self._get_conn()
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                conn.commit()
                self._release_conn(conn)
                return
            except (OperationalError, InterfaceError) as e:
                last_exc = e
                self._release_conn(conn, close=True)
                if attempt == 1:
                    raise

        if last_exc:
            raise last_exc

    # ------------------------ Pool shutdown ------------------------

    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.closeall()
            cls._pool = None
            print("Database pool closed.")

    # ------------------------ Custom query ------------------------

    def get_candidates_with_parties(self):
        query = """
        SELECT
            c.id         AS id,
            c.name       AS name,
            c.age        AS age,
            p.name       AS party,
            c.education  AS education,
            c.summary    AS summary,
            c.ref        AS ref,
            c.nicknames  AS nicknames
        FROM candidate_data.candidate_info c
        LEFT JOIN candidate_data.parties p ON p.id = c.party_id
        """
        return self._run_select(query)
