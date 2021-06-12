#!/usr/bin/python
# - *- coding: utf- 8 - *-

from checker import Checker
from logger import Logger
import sys
import subprocess
from lxml import etree as ET


# FIRST PART - CLI SETUP

def check_arguments(args=[]):
    if len(sys.argv) > 2:
        print("You just need to indicate source code path.")
    elif len(sys.argv) == 0:
        print("Please depict your source code path as an argument.")
    else:
        print("Starting srcML tool to convert source code.")
        return True  # srcML e gönder


def call_srcml_with_args(args=[]):
    subprocess.call(['srcml', args[0], "-o", "cmk_xml_output.xml"])


def main():
    args = sys.argv
    args.pop(0)  # To keep source code path, remove .py arg
    # print("Number of arguments: " + str(len(sys.argv)) + " arguments")
    # print("Argument List: " + str(sys.argv))
    valid_argument = check_arguments(args)
    loggerObj = Logger()
    if valid_argument == True:
        call_srcml_with_args(args)
        loggerObj.log_process(
            "Source file successfully converted to XML file.")
        loggerObj.log_process(
            "***********************************************")
        checkerObj = Checker()
        checkerObj.StartChecker()

    else:
        loggerObj.log_error("Invalid arguments")


main()  # Start app life cycle
