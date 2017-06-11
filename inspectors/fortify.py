#!/usr/bin/env python

import logging

import utils


def GET(item=None):
    return utils.tpl('listpage', {'world': 'xpto'})

def POST(item=None):
    pass

def DELETE(item=None):
    pass
