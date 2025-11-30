import os
import sqlite3
from typing import Any, Dict, List, Optional, Sequence, Union
from dotenv import load_dotenv
from psycopg2.pool import ThreadedConnectionPool


Param = Union[str, int, float, None]

class Database:

    _pool: Optional[ThreadedConnectionPool] = None

    def __init__(self, table):
        
        load_dotenv()
        self.table = table
       

        if Database._pool is None:
            db_url = os.environ.get("DATABASE_URL")
            Database._pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                dsn=db_url
            )
            print("Connection pool created")
    # ------------------------ Getters ------------------------
    def get_table(self) -> str:
        return self.table

    def get_database(self) -> str:
        return self.database


    # ------------------------ Setters ------------------------
    def set_table(self, table: str) -> None:
        self.table = table

    def set_database(self, database: str) -> None:
        self.database = database

        
        
    # ------------------------ Connection Helpers ------------------------
    def _get_conn(self):
        """Borrow a connection from the pool."""
        if Database._pool is None:
            raise RuntimeError("Connection pool not initialized")
        return Database._pool.getconn()

    def _release_conn(self, conn):
        """Return connection to the pool."""
        if Database._pool:
            Database._pool.putconn(conn)
            
    # ------------------------ Query Helpers ------------------------------

    def select(
        self,
        columns: Union[str, List[str]],
        where_sql: Optional[str] = None,
        params: Sequence[Param] = None,
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

        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql_q, params)
                colnames = [c[0] for c in cur.description]
                return [dict(zip(colnames, r)) for r in cur.fetchall()]
        finally:
            self._release_conn(conn)

    def execute(self, sql: str, params: Sequence[Param] = ()) -> None:
        """Execute INSERT/UPDATE/DELETE safely with commit."""
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
        finally:
            self._release_conn(conn)
    # ------------------------ Shutdown ------------------------
    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.closeall()
            cls._pool = None
            print("Database pool closed.")
    # ------------------------ Public API ------------------------------
    
    def get_candidates_with_parties(self):
        conn = self._get_conn()
        query = """
        select c.id as id ,c.name as name,c.age as age,p.name as party,c.education as education, c.summary as summary, c.ref as ref
        from candidate_data.candidate_info c
        LEFT JOIN candidate_data.parties p ON p.id=c.party_id
        """
        
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                colnames = [c[0] for c in cur.description]
                return [dict(zip(colnames, r)) for r in cur.fetchall()]
        finally:
            self._release_conn(conn)