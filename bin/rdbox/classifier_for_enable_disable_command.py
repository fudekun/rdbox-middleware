#!/usr/bin/env python3
# coding: utf-8

import rdbox.config
import socket

from logging import getLogger
r_logger = getLogger('rdbox_cli')
r_print = getLogger('rdbox_cli').getChild("stdout")


class ClassifierForEnableDisableCommand(object):

    FUNCTYPES = "k8s_external_svc|temporary_cache_registry"
    FUNCTYPES_LIST = FUNCTYPES.split("|")
    HELMTYPES = "onpremise-ingress-controller|temporary-cache-registry"
    HELMTYPES_LIST = HELMTYPES.split("|")
    FUNC_HELM_MAPPING = {}
    for i in range(len(FUNCTYPES_LIST)):
        FUNC_HELM_MAPPING[FUNCTYPES_LIST[i]] = HELMTYPES_LIST[i]

    @classmethod
    def _validation(cls, function_type):
        if function_type not in cls.FUNCTYPES_LIST:
            r_print.error("function_type is invalid.")
            return False
        master_hostname = rdbox.config.get("rdbox", "master_hostname")
        if socket.gethostname() != master_hostname:
            r_print.error(
                "This command can be executed only on the %s" % master_hostname)
            return False
        return True

    @classmethod
    def _map_func_to_helm(cls, function_type):
        return ClassifierForEnableDisableCommand.FUNC_HELM_MAPPING[function_type]
