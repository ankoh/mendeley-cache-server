__author__ = 'kohn'

import os
from os.path import exists
from mendeleycache.utils.files import get_relative_path
from mendeleycache.utils.exceptions import InvalidConfigurationException
from mendeleycache.logging import log

class CacheConfiguration:
    """
    General configuration of the cache server
    The profile_page_pattern is used to map user profiles to joomla links
    The strings :firstname and :lastname are substituted with the respective values
    Example: www1.in.tum.de/:firstname-:lastname
    """
    def __init__(self, profile_page_pattern: str):
        self._profile_page_pattern = profile_page_pattern
        log.debug("Using profile_page_pattern: %s" % profile_page_pattern)

    @property
    def profile_page_pattern(self):
        return self._profile_page_pattern


class CrawlerConfiguration:
    """
    Configuration of a base crawler
    """
    def __init__(self, research_group: str):
        self._research_group = research_group

    @property
    def research_group(self):
        return self._research_group


class SDKCrawlerConfiguration(CrawlerConfiguration):
    """
    Configuration of the SDK crawler
    """
    def __init__(self, research_group: str,  app_id: str, app_secret: str,):
        self._app_id = app_id
        self._app_secret = app_secret
        super(SDKCrawlerConfiguration, self).__init__(research_group)

    @property
    def app_id(self):
        return self._app_id

    @property
    def app_secret(self):
        return self._app_secret


class FileCrawlerConfiguration(CrawlerConfiguration):
    """
    Configuration of the file crawler
    """
    def __init__(self, research_group: str):
        super(FileCrawlerConfiguration, self).__init__(research_group)


class DatabaseConfiguration:
    """
    Configuration of the database access
    """
    def __init__(self, engine: str):
        self._engine = engine

    @property
    def engine(self):
        return self._engine


class SQLiteConfiguration(DatabaseConfiguration):
    def __init__(self, path: str):
        self._path = path
        super(SQLiteConfiguration, self).__init__('sqlite')

    @property
    def path(self):
        return self._path


class ServiceConfiguration:
    """
    Configuration of the Mendeley Cache
    """
    def __init__(self):
        self._crawler = None
        """:type : MendeleyConfiguration"""

        self._database = None
        """:type : DatabaseConfiguration"""

        self._cache = None
        """:type : CacheConfiguration"""

        self._version = "0.1.0"
        self._uses_mendeley = False

    @property
    def crawler(self):
        return self._crawler

    @property
    def cache(self):
        return self._cache

    @property
    def uses_mendeley(self):
        return self._uses_mendeley

    @property
    def database(self):
        return self._database

    @property
    def version(self):
        return self._version

    def load(self):
        """
        The load function loads the configuration from environment variables
        It returns nothing but raises InvalidConfigurationExceptions if something is missing
        :return:
        """

        # First read all environment variables with default values

        # Crawler
        crawler = os.environ['MC_CRAWLER'] if 'MC_CRAWLER' in os.environ else 'file'
        app_id = os.environ['MC_APP_ID'] if 'MC_APP_ID' in os.environ else ''
        app_secret = os.environ['MC_APP_SECRET'] if 'MC_APP_SECRET' in os.environ else ''
        research_group = os.environ['MC_RESEARCH_GROUP'] if 'MC_RESEARCH_GROUP' in os.environ else 'd0b7f41f-ad37-3b47-ab70-9feac35557cc'

        # Cache
        profile_page_pattern = os.environ['MC_PROFILE_PAGE_PATTERN'] if 'MC_PROFILE_PAGE_PATTERN' in os.environ else ""

        # SQLite
        database_path = os.environ['MC_DATABASE_PATH'] if 'MC_DATABASE_PATH' in os.environ else ''

        def missing_attribute(attribute: str):
            raise InvalidConfigurationException("Environment misses variable: %s" % attribute)

        # Store cache settings
        self._cache = CacheConfiguration(profile_page_pattern)

        # Validate crawler settings
        if crawler == 'file':
            self._uses_mendeley = False
            self._crawler = FileCrawlerConfiguration(research_group)
        elif crawler == 'mendeley':
            self._uses_mendeley = True
            if not app_id:
                missing_attribute('MC_APP_ID')
            if not app_secret:
                missing_attribute('MC_APP_SECRET')
            if not research_group:
                missing_attribute('MC_RESEARCH_GROUP')
            self._crawler = SDKCrawlerConfiguration(
                research_group=research_group,
                app_id=app_id,
                app_secret=app_secret
            )
        else:
            raise InvalidConfigurationException('Unknown crawler type %s' % crawler)

        # Configure SQLite
        self._database = SQLiteConfiguration(database_path)
