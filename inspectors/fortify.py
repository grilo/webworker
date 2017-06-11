#!/usr/bin/env python

import logging

import utils
import task


manager = task.Manager()

def GET(item=None):

    tasks = ""
    for t in manager.running_tasks():
        tasks += "<li>"
        tasks += "{cmd} ({pid})".format(cmd=t.command, pid=t.pid)
        tasks += "</li>\n"

    return utils.tpl('listfortifytasks', {'tasks': tasks})

def POST(item=None):
    pass

def DELETE(item=None):
    pass
