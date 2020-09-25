#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeComponents(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def show_component(self, component):
        """
        Returns a component (file, directory, project, view…) and its ancestors. The ancestors are ordered from the
            parent to the root project. The 'componentId' or 'component' parameter must be provided.

        :param component: Component key
        :return: The component details
        """
        params = {
            'component': component
        }

        resp = self.sonarqube._make_call('get', API_COMPONTENTS_SHOW, **params)

        if not resp:
            return None
        else:
            data = resp.json()
            return data['component']

    def get_components(self, qualifiers, **kwargs):
        """
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified
            qualifiers. Possible values are:
            |  APP - Applications
            |  BRC - Sub-projects
            |  DIR - Directories
            |  FIL - Files
            |  SVW - Portfolios
            |  TRK - Projects
            |  UTS - Test Files
            |  VW - Portfolios
        :param kwargs:
        :return: The list of filtered components.
        """
        params = {'qualifiers': qualifiers}
        if kwargs:
            self.sonarqube.copy_dict(params, kwargs)

        page_num = 1
        page_size = 1
        total = 2

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_COMPONTENTS_SEARCH, **params)
            response = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for component in response['components']:
                yield component

    def get_components_tree(self, component, qualifiers, **kwargs):
        """
        :param component: Base component key. The search is based on this component.
        :param kwargs:
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified qualifiers. Possible values are:
                          BRC - Sub-projects
                          DIR - Directories
                          FIL - Files
                          TRK - Projects
                          UTS - Test Files
        component: Base component key. The search is based on this component.
        :return:
        """
        params = {'component': component, 'qualifiers': qualifiers}
        if kwargs:
            self.sonarqube.copy_dict(params, kwargs)

        page_num = 1
        page_size = 1
        total = 2

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_COMPONTENTS_TREE, **params)
            response = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for component in response['components']:
                yield component
