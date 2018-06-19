#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Jakob Erdmann
# @date    2017-01-23
# @version $Id$


from __future__ import print_function
from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci
import sumolib  # noqa

def ppStages(comment, stages):
    print("%s\n  %s\n" % (comment, "\n  ".join(map(str, stages))))

sumoBinary = os.environ["SUMO_BINARY"]

cmd = [sumoBinary,
        '-n', 'input_net.net.xml',
        '-a', 'input_additional.add.xml',
        '--no-step-log',
        ]

traci.start(cmd)
ppStages("shortcut via trainStop:", traci.simulation.findIntermodalRoute("beg2left", "beg2left2"))
ppStages("train ride", traci.simulation.findIntermodalRoute("beg2left", "left2end", modes="public"))
traci.close()
