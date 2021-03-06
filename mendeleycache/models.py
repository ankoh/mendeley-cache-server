__author__ = 'kohn'

from dateutil.parser import parse
import datetime


class Member:
    """
    Class that represents a member of a group via profile_id, a join date and a role
    """
    def __init__(self,
                 profile_id: str,
                 joined: datetime,
                 role: str):
        self.__profile_id = profile_id
        self.__joined = joined
        self.__role = role

    @property
    def profile_id(self) -> str:
        return self.__profile_id

    @property
    def joined(self) -> datetime:
        return self.__joined

    @property
    def role(self) -> str:
        return self.__role


class Document:
    """
    Class that represents the core attributes of a single document.
    As this application will make heavy use of tags and bibtex, those are stored as well
    """
    def __init__(self,
                 core_id: str,
                 core_profile_id: str,
                 core_title: str,
                 core_type: str,
                 core_created: datetime,
                 core_last_modified: datetime,
                 core_abstract: str,
                 core_source: str,
                 core_year: int,
                 core_authors: [(str, str)],
                 core_keywords: [str],
                 doc_website: str,
                 conf_website: str,
                 conf_city: str,
                 conf_month: int,
                 conf_pages: str,
                 tags: [str]):
        self.__core_id = str(core_id)
        self.__core_profile_id = str(core_profile_id)
        self.__core_title = str(core_title)
        self.__core_type = str(core_type)
        self.__core_created = core_created
        self.__core_last_modified = core_last_modified
        self.__core_abstract = str(core_abstract)
        self.__core_source = str(core_source)
        self.__core_year = core_year
        self.__core_authors = core_authors
        self.__core_keywords = core_keywords
        self.__doc_website = str(doc_website)
        self.__conf_website = str(conf_website)
        self.__conf_city = str(conf_city)
        self.__conf_month = conf_month
        self.__conf_pages = str(conf_pages)
        self.__tags = tags

    @property
    def core_id(self) -> str:
        return self.__core_id

    @property
    def core_profile_id(self) -> str:
        return self.__core_profile_id

    @property
    def core_title(self) -> str:
        return self.__core_title

    @property
    def core_type(self) -> str:
        return self.__core_type

    @property
    def core_created(self) -> datetime:
        return self.__core_created

    @property
    def core_last_modified(self) -> datetime:
        return self.__core_last_modified

    @property
    def core_abstract(self) -> str:
        return self.__core_abstract

    @property
    def core_source(self) -> str:
        return self.__core_source

    @property
    def core_year(self) -> int:
        return self.__core_year

    @property
    def core_authors(self) -> [(str, str)]:
        return self.__core_authors

    @property
    def core_keywords(self) -> [str]:
        return self.__core_keywords

    @property
    def doc_website(self) -> str:
        return self.__doc_website

    @property
    def conf_website(self) -> str:
        return self.__conf_website

    @property
    def conf_city(self) -> str:
        return self.__conf_city

    @property
    def conf_month(self) -> int:
        return self.__conf_month

    @property
    def conf_pages(self) -> str:
        return self.__conf_pages

    @property
    def tags(self) -> [str]:
        return self.__tags


class Profile:
    """
    Class that represents a single author profile
    """
    def __init__(self,
                 identifier: str,
                 first_name: str,
                 last_name: str,
                 display_name: str,
                 link: str):
        self.__identifier = identifier
        self.__first_name = first_name
        self.__last_name = last_name
        self.__display_name = display_name
        self.__link = link

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def display_name(self) -> str:
        return self.__display_name

    @property
    def link(self) -> str:
        return self.__link


class CacheField:
    """
    Class that represents a cache field
    """
    def __init__(self, title: str, unified_title: str):
        self.__title = title
        self.__unified_title = unified_title

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def unified_title(self) -> str:
        return self.__unified_title


class CacheDocument:
    """
    Class that represents a cache document
    """
    def __init__(self, title: str, unified_title: str):
        self.__title = title
        self.__unified_title = unified_title

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def unified_title(self) -> str:
        return self.__unified_title


class CacheProfile:
    """
    Class that represents a cache profile
    """
    def __init__(self, name: str, unified_name: str):
        self.__name = name
        self.__unified_name = unified_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def unified_name(self) -> str:
        return self.__unified_name


class CacheUnknownProfile:
    """
    Class that represents an unknown profile
    """
    def __init__(self, name: str, unified_name: str):
        self.__name = name
        self.__unified_name = unified_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def unified_name(self) -> str:
        return self.__unified_name
