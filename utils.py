#!/usr/bin/env python

import os
import sys
import re
import logging
import subprocess
import shlex

def load_module(path):
    """Load a python module."""
    if not path.endswith('.py'):
        path += '.py'
    if not os.path.isfile(path):
        raise ImportError('Path must be a file: %s', path)
    path = re.sub('\.py$', '', path)
    directory = os.path.dirname(path)
    if not directory in sys.path:
        sys.path.insert(0, directory)
    try:
        return __import__(os.path.basename(path), globals(), locals(), [], -1)
    except SyntaxError as exception:
        raise exception
    except ImportError as exception:
        print exception
        raise NotImplementedError("Unable to find requested module in path: %s" % (path))

def load_inspectors(path='inspectors'):
    inspector_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    for module_file in os.listdir(inspector_path):
        if module_file.startswith('__'):
            continue
        if module_file.startswith('.'):
            continue
        if module_file.endswith('.pyc'):
            continue
        module_path = os.path.join(inspector_path, module_file)
        try:
            module = load_module(module_path)
            logging.info('Loaded inspector: %s', module.__name__)
            yield module
        except ImportError:
            logging.debug('Invalid inspector file: %s', module_path)
            continue

def tpl(template, options):
    tpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', template + '.tpl')
    if not os.path.isfile(tpl_path):
        raise ImportError("Template file doesn't exist: %s" % (tpl_path))

    with open(tpl_path, 'r') as tpl:
        return tpl.read().format(**options)

def cmd(command):
    proc = subprocess.Popen(shlex.shlex(command), \
                stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)

    out, err = proc.communicate()
    rc = proc.returncode

    return rc, out, err
