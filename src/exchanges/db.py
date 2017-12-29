from pathlib import Path
import logging
import sqlite3

from exchanges import exchanges

class Database:
    def __init__(self):
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Database")
        self._db_path: Path = Path("exchanges.db")

        self._delete()
        self._initialise()
        self._populate()

    def _initialise(self):
        db: sqlite3.Connection = sqlite3.connect(str(self._db_path))
        cursor: sqlite3.Cursor = db.cursor()

        cursor.executescript("""
            create table currencies (
                symbol text,
                name text
            );       

            create table markets (
                id integer primary key autoincrement,
                base text,
                quote text
            );      

            create table exchanges (
                id integer primary key autoincrement,
                name text
            );       

            create table exchange_markets (
                exchange_id integer references exchanges(id) on delete cascade,
                market_id integer references markets(id) on delete cascade,
                name text
            );        
        """)
        db.commit()
        db.close()

    def _delete(self):
        if self._db_path.exists():
            self._db_path.unlink()

    def _populate(self):
        db: sqlite3.Connection = sqlite3.connect(str(self._db_path))
        cursor: sqlite3.Cursor = db.cursor()

        cursor.executemany("insert into currencies values (?, ?)",
                           exchanges.get_currencies())

        for ex in exchanges.get_exchanges():
            cursor.execute("insert into exchanges(name) values (?)", (ex.name,))
            ex_id = cursor.lastrowid

            for name, base, quote in ex.get_markets():
                # Try to get the id of the market from the db.
                cursor.execute(
                        "select id from markets where base = ? and quote = ?",
                        (base, quote))
                market_id = cursor.fetchone()

                # If it doesn't exist, add it.
                if not market_id:
                    cursor.execute(
                        "insert into markets(base, quote) values (?, ?)",
                        (base, quote))
                    market_id = cursor.lastrowid

                cursor.execute("insert into exchange_markets values (?, ?, ?)",
                               (ex_id, market_id, name))

        db.commit()
        db.close()
