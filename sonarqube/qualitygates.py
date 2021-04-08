# -*- coding:utf-8 -*-
from .config import *


class SonarQubeQualityGates(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def get_qualitygates_project_status(self, project_key = None, branch = None, analysis_id = None):
        """
        Get the quality gate status of a project or a Compute Engine task.
        Either 'analysis_id', or 'project_id' and 'branch' combination must be provided
        The different statuses returned are: OK, WARN, ERROR, NONE. The NONE status is returned when there is no quality gate associated with the analysis.
        Returns an HTTP code 404 if the analysis associated with the task is not found or does not exist.
        :param project_key:
        :param branch
        :param analysis_id
        :return:
        """
        params = {}
        if analysis_id:
            params['analysisId'] = analysis_id
        elif project_key and branch:
            params['projectKey'] = project_key
            params['branch'] = branch
        else:
            return None
            
        resp = self.sonarqube._make_call('get', API_QUALITYGATES_PROJECT_STATUS, **params)
        data = resp.json()
        return data['projectStatus']

    def get_quality_gates(self):
        """
        Get a list of quality gates
        :return:
        """
        resp = self.sonarqube._make_call('get', API_QUALITYGATES_LIST)
        data = resp.json()
        return data['qualitygates']

    def select_quality_gate_for_project(self, project_key, gate_id):
        """
        Associate a project to a quality gate.
        :param project_key:
        :param gate_id:
        :return:
        """
        params = {'gateId': gate_id, 'projectKey': project_key}
        self.sonarqube._make_call('post', API_QUALITYGATES_SELECT, **params)

    def remove_project_from_quality_gate(self, project_key):
        """
        Remove the association of a project from a quality gate.
        :param project_key:
        :return:
        """
        params = {'projectKey': project_key}
        self.sonarqube._make_call('post', API_QUALITYGATES_DESELECT, **params)

    def show_quality_gate(self, gateId=None, name=None):
        """
        Display the details of a quality gate.
        :param gateId:
        :param name:
        :return:
        """
        params = {}
        if gateId:
            params.update({'id': gateId})
        if name:
            params.update({'name': name})
        resp = self.sonarqube._make_call('get', API_QUALITYGATES_SHOW, **params)
        data = resp.json()
        return data

    def get_quality_gate_of_project(self, project_key):
        """
        Get the quality gate of a project.
        :param project_key:
        :return:
        """
        params = {'project': project_key}
        resp = self.sonarqube._make_call('get', API_QUALITYGATES_GET_BY_PROJECT, **params)
        data = resp.json()
        return data['qualityGate']
