#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .config import *


class SonarQubeRules(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def get_rules(self, active_only=False, profile=None, languages=None,
                  custom_only=False):
        """
        Yield rules in status ready, that are not template rules.
        :param active_only: filter only active rules
        :param profile: key of profile to filter rules
        :param languages: key of languages to filter rules
        :param custom_only: filter only custom rules
        :return: generator that yields rule data dicts
        """
        # Build the queryset
        qs = {'is_template': 'no', 'statuses': 'READY'}

        # Add profile and activity params
        if profile:
            qs.update({'activation': 'true', 'qprofile': profile})
        elif active_only:
            qs['activation'] = 'true'

        # Add language param
        # Note: we handle comma-separated string or list-like iterable)
        if languages:
            if not isinstance(languages, str):
                languages = ','.join(languages)
            qs['languages'] = languages.lower()

        # Filter by tech debt for custom only (custom have no tech debt)
        if custom_only:
            qs['has_debt_characteristic'] = 'false'

        # Page counters
        page_num = 1
        page_size = 1
        n_rules = 2

        # Cycle through rules
        while page_num * page_size < n_rules:
            # Update paging information for calculation
            res = self.sonarqube._make_call('get', API_LIST, **qs).json()
            page_num = res['p']
            page_size = res['ps']
            n_rules = res['total']

            # Update page number (next) in queryset
            qs['p'] = page_num + 1

            # Yield rules
            for rule in res['rules']:
                yield rule

    def create_rule(self, key, name, description, message, xpath, severity,
                    status, template_key, type):
        """
        Create a a custom rule.
        :param key: key of the rule to create
        :param name: name of the rule
        :param description: markdown description of the rule
        :param message: issue message (title) for the rule
        :param xpath: xpath query to select the violation code
        :param severity: default severity for the rule
        :param status: status of the rule
        :param template_key: key of the template from which rule is created
        :param type: Rule type
        :return: request response
        """
        # Build data to post
        data = {
            'custom_key': key,
            'name': name,
            'markdown_description': description,
            'params': 'message={};xpathQuery={}'.format(message, xpath),
            'severity': severity.upper(),
            'status': status.upper(),
            'template_key': template_key,
            'type': type
        }

        self.sonarqube._make_call('post', API_CREATE, **data)

    def update_rule(self, key, name, description, markdown_note, message, xpath,
                    remediation_fn_base_effort, remediation_fn_type, remediation_fy_gap_multiplier, severity, status, tags):
        """
        Update an existing rule.
        :param key:
        :param name:
        :param description:
        :param markdown_note:
        :param message:
        :param xpath:
        :param remediation_fn_base_effort:
        :param remediation_fn_type:
        :param remediation_fy_gap_multiplier:
        :param severity:
        :param status:
        :param tags:
        :return:
        """
        data = {
            'key': key,
            'markdown_description': description,
            'markdown_note': markdown_note,
            'name': name,
            'params': 'message={};xpathQuery={}'.format(message, xpath),
            'remediation_fn_base_effort': remediation_fn_base_effort,
            'remediation_fn_type': remediation_fn_type,
            'remediation_fy_gap_multiplier': remediation_fy_gap_multiplier,
            'severity': severity.upper(),
            'status': status.upper(),
            'tags': tags
        }

        self.sonarqube._make_call('post', API_UPDATE, **data)

    def delete_rule(self, rule_key):
        """
        Delete custom rule.
        :param rule_key:
        :return:
        """
        params = {
            'key': rule_key
        }
        self.sonarqube._make_call('post', API_DELETE, **params)

    def get_rule(self, rule_key, actives=None):
        """
        Get detailed information about a rule
        :param rule_key:
        :param actives:
        :return:
        """
        params = {'key': rule_key}

        if actives:
            params['actives'] = actives

        res = self.sonarqube._make_call('post', API_SHOW, **params)
        return res.json()['rule']

    def get_rule_repositories(self, **kwargs):
        """
        List available rule repositories
        :param kwargs:
        language: A language key; if provided, only repositories for the given language will be returned
        :return:
        """
        resp = self.sonarqube._make_call('post', API_REPOSITORIES, **kwargs)
        return resp.json()

