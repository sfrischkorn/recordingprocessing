# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:11:00 2013

@author: shanef

Library to interface with handbrake to encode video files
"""

import subprocess


def encode(handbrakecommand, inputfile, outputfile, waitforcompletion=True,
           logger=None):
    """
    Encode inputfile and save the result to outputfile. handbrakecommand is
    a list of strings containing the arguments to handbrakecli.
    """

    handbrakecommand[3] = inputfile
    handbrakecommand[5] = outputfile

    if logger:
        logger.debug("Handbrake command is: {0}".format(handbrakecommand))

    process = subprocess.Popen(handbrakecommand)

    if waitforcompletion:
        process.wait()

        if logger is not None:
            logger.info("Handbrake completed with return code {0}".format(
                process.returncode))
        return process.returncode

    return None
