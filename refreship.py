#!/usr/bin/env python

import logging
import os
import socket
import time

import requests

from ns1 import NS1

# Logging Setup
LEVEL = os.environ.get("LOG_LEVEL", "info").lower()
LVL = logging.INFO
if LEVEL == "debug":
    LVL = logging.DEBUG
elif LEVEL == "warning":
    LVL = logging.WARNING
elif LEVEL == "error":
    LVL = logging.ERROR

FORMAT = "%(asctime)s - %(levelname)s[%(filename)s:%(lineno)d] %(message)s"
logging.basicConfig(level=LVL, format=FORMAT)
LOG = logging.getLogger(__name__)

NS1_API_KEY = os.environ.get("NS1_API_KEY")
DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
ZONE = os.environ.get("DNS_ZONE")


class NS1Manager(object):
    def __init__(self, api_key):
        self.api = NS1(apiKey=api_key)

    def get_record(self):
        self.record = self.api.loadRecord(DOMAIN_NAME, 'A', ZONE)
        answers = self.record.answers
        if len(answers) != 1:
            raise Exception(
                "Invalid number of answers for record ({}) [{}]".
                format(DOMAIN_NAME, len(answers)))
        return answers[0].get('answer')[0]

    def update_record(self, ip):
        if not self.record:
            self.get_record()
        new_ip = {'answers': [{'answer': [ip]}]}
        self.record.update(callback=None, errback=None, **new_ip)
        self.record.reload()
        assert self.record.answers[0].get('answer')[0] == ip


def update_ip(manager):
    # Get current external IP
    r = requests.get('https://api.ipify.org')
    ip = r.content
    try:
        ip = ip.decode('utf-8')
        socket.inet_aton(ip)
    except Exception:
        LOG.error("Invalid ip address {}".format(ip))
        return
    try:
        current_ip = manager.get_record()
    except Exception as e:
        print(e)
        return
    if current_ip == ip:
        LOG.debug("IP is up-to-date")
        return

    LOG.info("Updating record to {}".format(ip))
    try:
        manager.update_record(ip)
    except Exception as e:
        print(e)
        return
    LOG.info("Record updated successfully")


def main():
    LOG.info("Starting IP updater")
    if not NS1_API_KEY:
        LOG.error("Missing NS1_API_KEY env var")
        exit(1)
    LOG.info("Connecting to NS1")
    manager = NS1Manager(NS1_API_KEY)
    while True:
        update_ip(manager)
        LOG.debug("Going to sleep")
        time.sleep(300)
        LOG.debug("Waking up")


if __name__ == '__main__':
    main()
