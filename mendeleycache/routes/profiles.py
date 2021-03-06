__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.utils.json_encoder import DefaultEncoder
from mendeleycache.data.controller import DataController
from mendeleycache.config import CacheConfiguration
from mendeleycache.logging import log
import re
import json


class ProfilesController:
    def __init__(self, app: Flask, data_controller: DataController, cache_config: CacheConfiguration):
        self._app = app
        self._data_controller = data_controller
        self._cache_config = cache_config

    def register(self):
        self._app.add_url_rule('/profiles/', methods=['GET'], view_func=self.get_profiles)

    def get_profiles(self):
        log.info('The route GET /profiles/ has been triggered')

        # Default parameters
        profile_ids = ''
        field_ids = ''
        slim = False

        # Set passed query parameters if existing
        if 'profile-ids' in request.args:
            profile_ids = request.args['profile-ids'].split(',')
            log.debug('Query parameter "profile-ids" = %s' % profile_ids)
        if 'field-ids' in request.args:
            field_ids = request.args['field-ids'].split(',')
            log.debug('Query parameter "field_ids" = %s' % field_ids)
        if 'slim' in request.args:
            slim = bool(request.args['slim'])
            log.debug('Query parameter "slim" = %s' % slim)

        # Trigger the respective methods
        profiles = []
        if slim:
            profiles = self._data_controller.api_data.get_profiles_slim()
        else:
            profiles = self._data_controller.api_data.get_profiles_by_profile_ids_or_field_ids(
                profile_ids=profile_ids,
                field_ids=field_ids
            )

        # Pattern for cms pages
        page_pattern = self._cache_config.profile_page_pattern

        # Serialize documents
        response = []
        for profile in profiles:
            profile_dict = dict(profile)

            # names
            name = None
            first_name = None
            last_name = None


            # Get names
            if 'first_name' in profile_dict and 'last_name' in profile_dict:
                first_name = profile_dict['first_name']
                last_name = profile_dict['last_name']
            elif 'name' in profile_dict:
                name = profile_dict['name']
                name_parts = [s.lower() for i, s in enumerate(name.split())]
                first_name = name_parts[0]
                last_name = name_parts[1]

            # If the names are available create the page link
            if first_name is not None and last_name is not None:
                page = page_pattern
                page = re.sub(':firstname', first_name, page)
                page = re.sub(':lastname', last_name, page)
                profile_dict["page"] = page

            response.append(profile_dict)
        return json.dumps(response, cls=DefaultEncoder)
