#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeMeasure(object):
    """Get components or children with specified measures.

    Available values for:
        metricKeys: code_smells,bugs,vulnerabilities,new_bugs,new_vulnerabilities,new_code_smells,coverage,
            new_reliability_rating,reliability_rating,new_security_rating,security_rating,new_maintainability_rating,
            sqale_rating,tests,test_failures,test_errors,skipped_tests,test_success_density,ncloc,
            duplicated_lines_density,comment_lines_density

        additionalFields: metrics,periods

        metrics: code_smells,bugs,vulnerabilities,new_bugs,new_vulnerabilities,new_code_smells,coverage,new_coverage
    """
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def get_measures_component(self, component: str, metric_keys: str, additional_fields: str = None):
        """
        Return component with specified measures. The componentId or the component parameter must be provided.

        :param component: Component key
        :param metric_keys: Comma-separated list of metric keys
        :param additional_fields: Comma-separated list of additional fields that can be returned in the response.
            Possible values are
            | metrics
            | periods
        :return: The measures for the metricKeys provided for the specified component
        """
        params = {
            'additionalFields': additional_fields,
            'metricKeys': metric_keys,
            'component': component
        }
        resp = self.sonarqube._make_call('get', API_MEASURES_COMPONENT, **params)
        data = resp.json()
        return data

    def get_measures_component_tree(self,
                                    component: str,
                                    metric_keys: str,
                                    additional_fields: str = None,
                                    qualifiers: str = None,
                                    strategy: str = 'all'):
        """
        Navigate through components based on the chosen strategy with specified measures. The baseComponentId or the
        component parameter must be provided.

        :param component: Component key
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified
            qualifiers. Possible values are:
            | APP - Applications
            | BRC - Sub-projects
            | DIR - Directories
            | FIL - Files
            | SVW - Portfolios
            | TRK - Projects
            | UTS - Test Files
            | VW - Portfolios
        :param metric_keys: Comma-separated list of metric keys (Maximum allowed values: 15)
        :param additional_fields: Comma-separated list of additional fields that can be returned in the response.
            Possible values are
            | metrics
            | periods
        :param strategy: Strategy to search for base component descendants:
            | children: return the children components of the base component. Grandchildren components are not returned
            | all: return all the descendants components of the base component. Grandchildren are returned.
            | leaves: return all the descendant components (files, in general) which don't have other children.
                They are the leaves of the component tree.

        :return: The
        """
        params = {
            'additionalFields': additional_fields,
            'metricKeys': metric_keys,
            'component': component,
            'qualifiers': qualifiers,
            'strategy': strategy
        }
        page_num = 1
        page_size = 1
        total = 2

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_MEASURES_COMPONENT_TREE, **params)
            response: dict = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for component in response['components']:
                yield component

    def get_measures_history(self, component, metrics):
        """
        Search measures history of a component. Measures are ordered chronologically. Pagination applies to the number
        of measures for each metric.

        :param component: Component key
        :param metrics: Comma-separated list of metric keys
        :return: The measures hisotry for the metrics provided for the specified component
        """
        params = {
            'metrics': metrics,
            'component': component
        }

        page_num = 1
        page_size = 1
        total = 2

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_MEASURES_SEARCH_HISTORY, **params)
            response = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for measure in response['measures']:
                yield measure
