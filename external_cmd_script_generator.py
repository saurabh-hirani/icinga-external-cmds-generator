#!/usr/bin/env python

"""
Usage:
  external_cmd_script_generator.py [-h|--help] --external-cmd <cmd> --tmpl-vars-generator <func_name> [--func-args <func_args>] [--output-file <output_file>]

Options:
  -h --help                     show this help text
  --external-cmd <cmd>          external command from http://docs.icinga.org/latest/en/extcommands2.html - corresponding template should exist in templates/ dir
  --tmpl-vars-generator <func>  function in tmpl_vars_generator.py which will return the template variables for this command's template
  --func-args <func_args>       json string or a json file path - contents will be passed to <func>. [default: {}]
  --output-file <output_file>   dump the output in this file. [default: stdout]
"""

import os
import sys
import json
import string

import imp
from docopt import docopt

PROG_DIR = os.path.dirname(os.path.realpath(__file__))
TMPL_DIR = os.path.join(PROG_DIR, 'templates')
TMPL_VARS_FUNC_FILE = os.path.join(PROG_DIR, 'template_vars_generators.py')

def generate_external_cmds_script(external_cmds, output_file):
  external_cmds_str = '\n'.join(external_cmds)
  if output_file != 'stdout':
    mode = 'w'
    if os.path.exists(output_file):
      mode = 'a'
    with open(output_file, mode) as f:
      f.write(external_cmds_str)
  return external_cmds_str

def generate_external_cmds(tmpl_path, tmpl_vars_list):
  tmpl_obj = string.Template(open(tmpl_path).read())
  external_cmds = []
  for tmpl_vars in tmpl_vars_list:
    external_cmds.append(tmpl_obj.safe_substitute(tmpl_vars).strip())
  return external_cmds

def _get_tmpl_vars_generator_args(args):
  try:
    return json.loads(args)
  except ValueError as e:
    # couldn't load args - maybe it is a file
    if not os.path.exists(args):
      print 'ERROR: args %s neither json str nor file' % args
      sys.exit(1)
    return json.loads(open(args).read())

def _get_tmpl_vars_generator(funcname):
  if not os.path.exists(TMPL_VARS_FUNC_FILE):
    print 'ERROR: path %s does not exist' % TMPL_VARS_FUNC_FILE
    sys.exit(1)
  mod = imp.load_source('callback', TMPL_VARS_FUNC_FILE)
  return getattr(mod, funcname)

def _get_tmpl_path(cmd):
  external_cmd = cmd
  tmpl_path = os.path.join(TMPL_DIR, external_cmd.lower() + '.tmpl')
  if not os.path.exists(tmpl_path):
    print 'ERROR: path %s does not exist' % tmpl_path
    sys.exit(1)
  return tmpl_path

def main(opts):
  tmpl_path = _get_tmpl_path(opts['--external-cmd'])
  tmpl_vars_generator = _get_tmpl_vars_generator(opts['--tmpl-vars-generator'])
  func_args = _get_tmpl_vars_generator_args(opts['--func-args'])
  tmpl_vars_list = tmpl_vars_generator(func_args)
  external_cmds = generate_external_cmds(tmpl_path, tmpl_vars_list)
  return generate_external_cmds_script(external_cmds, opts['--output-file'])

def parse_cmdline():
  return docopt(__doc__)

if __name__ == '__main__':
  print main(parse_cmdline())
