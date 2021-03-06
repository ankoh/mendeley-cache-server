__author__ = 'kohn'

from flask import Flask, request

from mendeleycache.utils.json_encoder import DefaultEncoder
from mendeleycache.data.controller import DataController
from mendeleycache.logging import log
import json


class DocumentsController:
    def __init__(self, app: Flask, data_controller: DataController):
        self._app = app
        self._data_controller = data_controller

    def register(self):
        self._app.add_url_rule('/documents/', methods=['GET'], view_func=self.get_documents)

    def get_documents(self):
        log.info('The route GET /documents/ has been triggered')

        # Default parameters
        profile_ids = ''
        field_ids = ''
        limit = 0
        offset = 0
        order_dir = ""
        order_attr = ""
        only_count = False

        # Set passed query parameters if existing
        if 'profile-ids' in request.args:
            profile_ids = request.args['profile-ids'].split(',')
            log.debug('Query parameter "profile-ids" = %s' % profile_ids)
        if 'field-ids' in request.args:
            field_ids = request.args['field-ids'].split(',')
            log.debug('Query parameter "field-ids" = %s' % field_ids)
        if 'limit' in request.args:
            limit = int(request.args['limit'])
            log.debug('Query parameter "limit" = %s' % limit)
        if 'offset' in request.args:
            offset = int(request.args['offset'])
            log.debug('Query parameter "offset" = %s' % offset)
        if 'order-dir' in request.args:
            order_dir = request.args['order-dir']
            log.debug('Query parameter "order-dir" = %s' % order_dir)
        if 'order-attr' in request.args:
            order_attr = request.args['order-attr']
            log.debug('Query parameter "order-attr" = %s' % order_attr)
        if 'only-count' in request.args:
            only_count = bool(request.args['only-count'])
            log.debug('Query parameter "only-count" = %s' % only_count)

        # Trigger the respective methods
        data = self._data_controller.api_data.get_documents_by_profile_ids_and_field_ids(
            profile_ids=profile_ids,
            field_ids=field_ids,
            order_attr=order_attr,
            order_dir=order_dir,
            offset=offset,
            limit=limit,
            only_count=only_count
        )

        if only_count:
            # Extract count
            response = []
            for document in data:
                document_dict = dict(document.items())
                response.append(document_dict)

            if len(response) > 0:
                return json.dumps(response[0], cls=DefaultEncoder)
            else:
                return json.dumps({"cnt": 0}, cls=DefaultEncoder)
        else:
            # Serialize documents
            response = []
            for document in data:
                document_dict = dict(document.items())
                response.append(document_dict)
            return json.dumps(response, cls=DefaultEncoder)
