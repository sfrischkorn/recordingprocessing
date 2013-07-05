# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:11:00 2013

@author: shanef

Library to interface with handbrake to encode video files
"""

import logging
import subprocess

HANDBRAKECOMMAND = ['HandBrakeCLI', '--verbose', '-i', 
                    "SUBSTITUTE WITH INPUT FILE", '-o', 
                    "SUBSTITUDE WITH OUTPUT FILE", '-f', 'mkv', '-e', 'x264', 
                    '-x264-preset', 'slower', '-x264-tune', 'animation', '-q', 
                    '20', '--loose-anamorphic', '--decomb', '--detelecine', 
                    '--denoise="2:1:2:3"', '--deblock']

class Encoder:
    def Encode(input, output, waitForCompletion=True, logger=None): 
        HANDBRAKECOMMAND[3] = input
        HANDBRAKECOMMAND[5] = output

        logger.debug("Handbrake command is: {0}".format(HANDBRAKECOMMAND))
        process = subprocess.Popen(HANDBRAKECOMMAND)
        
        if waitForCompletion:
            process.wait()
            
            if logger is not None:
                logger.info("Handbrake completed with return code {0}".format(process.returncode))
            return process.returncode
            
        return None
    