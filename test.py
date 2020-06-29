"""
Test SiamFC & DaSiamRPN on GOT-10k
@ fansiqi  2020.4.21
"""
from __future__ import absolute_import

import argparse

from got10k.experiments import *

from DaSiamRPN.tracker import TrackerDaSiamRPN
from SiamFC.tracker import TrackerSiamFC


def test(model_name):
    # setup tracker
    if model_name == 'SiamFC':
        tracker = TrackerSiamFC("./SiamFC/SiamFC.pth") 
    elif model_name == 'DaSiamRPN':
        tracker = TrackerDaSiamRPN("./DaSiamRPN/DaSiamRPN.pth")

    # setup experiments
    experiments = [
        ExperimentGOT10k('data/GOT-10k', subset='test')
    ]

    # run tracking experiments and report performance
    for e in experiments:
        e.run(tracker, visualize=False)
        e.report([tracker.name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-model_id', default=0, help="0---SiamFC, 1---DaSiamRPN")

    args = parser.parse_args()

    model_id = args.model_id
    model_name = "DaSiamRPN" if model_id else "SiamFC"

    print ("-"*30)
    print ("Test {} model".format(model_name))

    test(model_name)
