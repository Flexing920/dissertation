#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2014-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Michael Behrisch
# @date    2014-03-14
# @version $Id$

from __future__ import absolute_import

import os
import subprocess
import sys
import time
import socket
import difflib
toolDir = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '..', "tools")
if 'SUMO_HOME' in os.environ:
    toolDir = os.path.join(os.environ['SUMO_HOME'], "tools")
sys.path.append(toolDir)
import sumolib  # noqa


def connect(inPort, outPort, numTries=10):
    for wait in range(1, numTries + 1):
        try:
            i = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            i.connect(("localhost", inPort))
            break
        except socket.error:
            if wait == numTries:
                raise
            time.sleep(wait)
    for wait in range(1, numTries + 1):
        try:
            o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            o.connect(("localhost", outPort))
            break
        except socket.error:
            if wait == numTries:
                raise
            time.sleep(wait)
    while 1:
        data = i.recv(1024)
        if not data:
            break
        o.sendall(data)
    o.close()
    i.close()

SUMO_PORT = sumolib.miscutils.getFreeSocketPort()
IN_PORT = sumolib.miscutils.getFreeSocketPort()
OUT_PORT = sumolib.miscutils.getFreeSocketPort()
sumoBinary = sumolib.checkBinary('sumo')
xmlProtoPy = os.path.join(toolDir, 'xml', 'xml2protobuf.py')
protoXmlPy = os.path.join(toolDir, 'xml', 'protobuf2xml.py')
schema = os.path.join(
    toolDir, '..', 'data', 'xsd', 'amitran', 'trajectories.xsd')

# file output direct
subprocess.call(
    [sumoBinary, "-c", "sumo.sumocfg", "--amitran-output", "direct.xml"])

# protobuf roundtrip
xPro = subprocess.Popen(
    ['python', xmlProtoPy, '-x', schema, '-o', str(IN_PORT), str(SUMO_PORT)])
pPro = subprocess.Popen(['python', protoXmlPy, '-x', schema, str(OUT_PORT)])
sumoPro = subprocess.Popen(
    [sumoBinary, "-c", "sumo.sumocfg", "--amitran-output", "localhost:%s" % SUMO_PORT])
try:
    connect(IN_PORT, OUT_PORT)
    sumoPro.wait()
    pPro.wait()
    xPro.wait()
except:
    sumoPro.kill()
    pPro.kill()
    xPro.kill()
    raise

for line in difflib.unified_diff(open('direct.xml').readlines(), open('%s.xml' % OUT_PORT).readlines(), n=0):
    sys.stdout.write(line)
