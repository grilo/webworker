#!/usr/bin/env python

import logging
import json
import multiprocessing as mp

import bottle

import utils
import task
import mail


manager = task.Manager()

@bottle.get('/fortify')
@bottle.get('/fortify/<item>')
def get(item=None):
    tasks = ""
    for t in manager.running_tasks():
        tasks += "<li>"
        tasks += "({pid}) {cmd}".format(pid=t.pid, cmd=t.command)
        tasks += "</li>\n"

    return utils.tpl('listfortifytasks', {'tasks': tasks})

@bottle.delete('/fortify/<pid>')
def delete(pid=None):
    bottle.response.content_type = 'application/json'

    if pid and pid in manager.tasks.keys():
        logging.debug('Found task in the task manager.')
        t = manager.tasks[pid]
        logging.debug('Killing running task with PID: %s', pid)
        t.stop()
        bottle.response.status = 200
        return json.dumps({'message': 'Task with PID (%s) was halted.' % (pid)})
    else:
        bottle.response.status = 404
        bottle.response.content_type = 'application/json'
        return json.dumps({'error': 'No running task with PID (%s) was found.' % (pid)})

@bottle.post('/fortify')
def post():
    bottle.response.content_type = 'application/json'
    bottle.response.status = 200
    p = mp.Process(target=f, args=(files,))
    return None

def run_inspection(files):
    task = Task('sleep 30')
    task.wait()
    mail.Message('jenkins-no-reply@ingdirect.es', 'joao.grilo@gmail.com', 'subject', 'body', 'localhost', 25)
    print mail.build_mail()
