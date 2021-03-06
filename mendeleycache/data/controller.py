__author__ = 'kohn'

from mendeleycache.config import DatabaseConfiguration
from mendeleycache.data.api_data import ApiData
from mendeleycache.data.crawl_data import CrawlData
from mendeleycache.data.reader import read_sql_statements
from mendeleycache.utils.exceptions import InvalidConfigurationException
from mendeleycache.config import DatabaseConfiguration, SQLiteConfiguration
from mendeleycache.logging import log
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DBAPIError

from mendeleycache.logging import log


def create_engine(config: DatabaseConfiguration) -> Engine:
    path = ""
    log_path = path

    if not config.path:
        path = "sqlite://"
        log_path = path
    else:
        path = "sqlite:///{path}".format(
            path=config.path
        )
        log_path = path

    log.info("Creating engine '{engine}' with path {path}".format(
        engine="sqlite",
        path=log_path
    ))

    # create engine
    # Pool recycle:
    # http://stackoverflow.com/questions/26891971/mysql-connection-not-available-when-use-sqlalchemymysql-and-flask
    return sqlalchemy.create_engine(path, encoding="utf-8", pool_recycle=3600)


class DataController:
    """
    The DataController provides access to the engine
    """

    def __init__(self, config: DatabaseConfiguration):
        self._config = config
        self._engine = create_engine(self._config)
        self._api_data = ApiData(self._engine)
        self._crawl_data = CrawlData(self._engine)

    @property
    def engine(self):
        """
        Return the initialized database engine
        :return:
        """
        return self._engine

    @property
    def api_data(self):
        return self._api_data

    @property
    def crawl_data(self):
        return self._crawl_data

    def table_exists(self, table_name: str) -> bool:
        """
        Tests if the database is already initialized
        :return:
        """
        try:
            with self._engine.connect() as conn:
                result = conn.execute("SELECT * FROM %s" % table_name)
                return True
        except DBAPIError as e:
            return False

    def is_initialized(self):
        """
        Checks whether all the different tables exist
        """
        return (
            self.table_exists('document') and
            self.table_exists('profile') and
            self.table_exists('cache_document') and
            self.table_exists('cache_profile') and
            self.table_exists('cache_field') and
            self.table_exists('cache_profile_has_cache_document') and
            self.table_exists('cache_document_has_cache_field') and
            self.table_exists('update_log')
        )

    def run_schema(self):
        """
        Runs the schema initialization and returns if it was successfull
        """
        schema = []
        if self._config.engine == "sqlite":
            schema = read_sql_statements('sql', 'schema', 'sqlite.sql')
        elif self._config.engine == "mysql":
            schema = read_sql_statements('sql', 'schema', 'mysql.sql')

        with self._engine.begin() as conn:
            for cmd in schema:
                conn.execute(cmd)

        log.info("Schema has been initialized")

    def drop_all(self):
        drops = read_sql_statements('sql', 'schema', 'drop_all.sql')

        foreign_key_off = ""
        foreign_key_on = ""

        if self._config.engine == "mysql":
            foreign_key_off = "SET FOREIGN_KEY_CHECKS = 0"
            foreign_key_on = "SET FOREIGN_KEY_CHECKS = 1"
        elif self._config.engine == "sqlite":
            foreign_key_off = "PRAGMA foreign_keys = OFF"
            foreign_key_on = "PRAGMA foreign_keys = ON"

        with self._engine.begin() as conn:
            log.info(foreign_key_off)
            conn.execute(foreign_key_off)
            for drop in drops:
                log.info(drop)
                conn.execute(drop)
            log.info(foreign_key_on)
            conn.execute(foreign_key_on)

        log.info("Database has been dropped")

    def assert_schema(self):
        if self.is_initialized():
            log.info("Schema is already initialized")
        else:
            log.warning("The current schema is incomplete. Starting migration.")
            # TODO: Backup && Restore as soon as the database has state
            self.drop_all()
            self.run_schema()
