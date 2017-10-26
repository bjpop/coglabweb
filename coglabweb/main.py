'''
Module      : Main 
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 2017 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX

Generate the COG website
'''

from argparse import ArgumentParser
import sys
import logging
import pkg_resources
import os
from jinja2 import Environment, FileSystemLoader
import yaml


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
DEFAULT_VERBOSE = False
DEFAULT_TEMPLATES_DIR = 'templates' 
DEFAULT_OUTPUT_DIR = 'docs' 
PROGRAM_NAME = "coglabweb"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    parser = ArgumentParser(description='Generate the COG website')
    parser.add_argument('--version',
        action='version',
        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
        metavar='LOG_FILE',
        type=str,
        help='record program progress in LOG_FILE')
    parser.add_argument('--templates',
        metavar='TEMPLATES_DIR',
        type=str,
        help='path to the templates directory',
        default=DEFAULT_TEMPLATES_DIR)
    parser.add_argument('--outdir',
        metavar='OUTPUT_DIR',
        type=str,
        help='path to write output HTML files',
        default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
            level=logging.DEBUG,
            filemode='w',
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: {0}'.format(' '.join(sys.argv)))


def init_jinja(options):
    return Environment(
        autoescape=False,
        loader=FileSystemLoader(options.templates),
        trim_blocks=True)
 
def render_team(options, jinja_env):
    template = "team.html"
    contents = "team.yaml"
    contents_filename = os.path.join(options.templates, contents)
    with open(contents_filename) as contents_file:
        contents = yaml.load(contents_file)
        html = jinja_env.get_template(template).render(people=contents)
        output_filename = os.path.join(options.outdir, template)
        with open(output_filename, 'w') as output_file:
            output_file.write(html)


def render_pages(options, jinja_env):
    # Assume: each template generates an output file of the same name
    templates = [
            ("index.html", {}),
            ("projects.html", {}),
            ("funding.html", {}),
            ("contact.html", {}),
            ("publications.html", {}),
            ("partners.html", {}),
            ]
    for template, context in templates:
        output_filename = os.path.join(options.outdir, template)
        with open(output_filename, 'w') as file:
            #html = render_template(jinja_env, template, context)
            html = jinja_env.get_template(template).render(context) 
            file.write(html)


def make_output_dir(options):
    if not os.path.exists(options.outdir):
        os.makedirs(options.outdir)


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    jinja_env = init_jinja(options)
    make_output_dir(options)
    render_pages(options, jinja_env)
    render_team(options, jinja_env)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
