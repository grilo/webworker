#!/usr/bin/env python

import logging
import json
import multiprocessing as mp

import bottle

import utils
import task
import mail


def run_inspection(files):
    logging.info('Starting inspection task...')

    sca = '/opt/fortify/bin/sourceanalyzer'
    scandir = '/tmp'/

    clean = """{sca} -b {scandir} -clean""".format(sca=sca, scandir=scandir)
    task.Task(clean).wait()

    gen = """{sca} -b {scandir} -jdk 1.5 -exclude REPORTING/* -classpath""".format(sca=sca, scandir=scandir)
    task.Task(gen).wait()

    scan = """{sca} -b {scandir} -scan  -f {report}""".format(sca=sca, scandir=scandir, report='report')
    task.Task(scan).wait()

    upload = """/opt/fortify/bin/fortifyclient downloadFPR -file""""
    task.Task(upload).wait()

    m = mail.Message('jenkins-no-reply@ingdirect.es', 'joao.grilo@gmail.com', 'subject', 'body', 'localhost', 25)
    print m.build_mail()


@bottle.get('/fortify')
@bottle.get('/fortify/<item>')
def get(item=None):
    tasks = ""
    for p in pool._pool:
        tasks += "<li>"
        tasks += "({pid}) {cmd}".format(pid=p.pid, cmd=p.name)
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
    files = bottle.request.json
    mp.Process(target=run_inspection, args=(files,)).start()
    return None
