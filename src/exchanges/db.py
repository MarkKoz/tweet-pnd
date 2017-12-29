import logging
import sqlite3

from exchanges import exchanges

class Database:
    def __init__(self):
        self._log: logging.Logger = logging.getLogger("bot.exchanges.Database")
        self._db: sqlite3.Connection = sqlite3.connect("exchanges.db")

        self.cursor: sqlite3.Cursor = self._db.cursor()

        self._drop()
        self._initialise()
        self._populate()
        self.commit()

    def __del__(self):
        self._db.close()

    def commit(self):
        self._db.commit()

    def _initialise(self):
        self.cursor.executescript("""
            create table if not exists currencies (
                symbol text,
                name text,
                primary key (symbol, name)
            );       

            create table if not exists markets (
                id integer primary key autoincrement,
                base text references currencies(symbol) on delete cascade,
                quote text references currencies(symbol) on delete cascade
            );      

            create table if not exists exchanges (
                id integer primary key autoincrement,
                name text
            );       

            create table if not exists exchange_markets (
                exchange_id integer references exchanges(id) on delete cascade,
                market_id integer references markets(id) on delete cascade,
                name text
            );        
        """)

    def _drop(self):
        self.cursor.executescript("""
            drop table exchange_markets;
            drop table exchanges;
            drop table markets;
            drop table currencies;
        """)

    def _populate(self):
        self.cursor.executemany("insert into currencies values (?, ?)",
                                exchanges.get_currencies())

        for ex in exchanges.get_exchanges():
            self.cursor.execute("insert into exchanges(name) values (?)",
                                (ex.name,))
            ex_id = self.cursor.lastrowid

            for name, base, quote in ex.get_markets():
                # Try to get the id of the market from the db.
                self.cursor.execute(
                        "select id from markets where base = ? and quote = ?",
                        (base, quote))
                market_id = self.cursor.fetchone()

                # If it doesn't exist, add it.
                if not market_id:
                    self.cursor.execute(
                            "insert into markets(base, quote) values (?, ?)",
                            (base, quote))
                    market_id = self.cursor.lastrowid
                else:
                    market_id = market_id[0]

                self.cursor.execute(
                        "insert into exchange_markets values (?, ?, ?)",
                        (ex_id, market_id, name))
