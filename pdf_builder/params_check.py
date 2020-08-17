# ============================================================================#
# =============================== LIBRAIRIES =================================#
# ============================================================================#

import os
import re

from .utils import error, sub_run


# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


def check_bootcamp_title(title: str):
    if not title or len(title) < 3 or len(title) > 20:
        error("invalid bootcamp title length ! (length must be between\
             3 and 20)")
    if re.match(r'![A-Za-z ]', title):
        error("invalid bootcamp title chars ([A-Za-z ] allowed)")
    return (True)


def check_input_dir(directory: str):
    # check directory is in the format dayXX
    while directory[-1] == '/':
        directory = directory[:-1]
    dir = directory.split('/')[-1]
    regex = re.compile(r'^day[0-9]{2}$')
    if not regex.search(dir):
        error("'{}' invalid day directory (dayXX allowed)".format(directory))

    # check if it is a directory
    if not os.path.isdir(directory):
        error("'{}' is not a directory !".format(directory))

    # check directory has a dayXX.md
    ls_day = sub_run("ls {}/day*.md".format(directory))
    if ls_day.stderr:
        error("markdown for day missing")

    # check directory has exXX.md files
    ls_ex = sub_run("ls {}/ex*/ex*.md".format(directory))
    if ls_ex.stderr:
        error("markdown for exercices missing")


def check_input_file(input_file: str):
    if not os.path.isfile(input_file):
        error("'{}' is not a file !".format(input_file))
    if input_file.split('.')[-1] != "md":
        error("'{}' is not a markdown file".format(input_file))


def check_day_title(title: str):
    if not title or len(title) < 11 or len(title) > 40:
        error("invalid day title length ! (length must be between\
             11 and 40)")
    if re.match(r'![A-Za-z -]', title):
        error("invalid day title chars ([A-Za-z -] allowed)")
    if re.match(r'!(^Day[0-9]{2} - .*)', title):
        error("invalid day title ! (it must be formatted as follows\
             \"DayXX - ...\")")
    return (True)


def check_file_dir(args):
    if args.input_dir and args.input_file:
        error("you provided a file AND a folder, please\
               provide a file OR a folder !")
