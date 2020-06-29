# from __future__ import absolute_import, division

import torch
import numpy as np
import cv2
from os.path import realpath, dirname, join

import sys
sys.path.append("..")
from DaSiamRPN.DaSiamRPN import DaSiamRPN
from DaSiamRPN.run_SiamRPN import SiamRPN_init, SiamRPN_track
from DaSiamRPN.utils import get_axis_aligned_bbox, cxy_wh_2_rect

from got10k.trackers import Tracker


class TrackerDaSiamRPN(Tracker):

    def __init__(self, net_path=None, **kargs):
        super(TrackerDaSiamRPN, self).__init__(name='DaSiamRPN', is_deterministic=True)

        # setup GPU device if available
        self.cuda = torch.cuda.is_available()
        self.device = torch.device('cuda:0' if self.cuda else 'cpu')

        # 初始化网络模型
        self.net = DaSiamRPN()  
        # 网络模型参数读取
        if net_path is not None:
            try:
                self.net.load_state_dict(torch.load(net_path, map_location=lambda storage, loc: storage))
                print ("Load model {} -- Done".format(net_path))
            except:
                print ("Could not find model file -- {}".format(net_path))
        # 将其放在GPU上运行
        self.net = self.net.to(self.device)
        # net.eval().cuda() 


    def init(self, image, box):
        image = np.asarray(image)

        # left-top based --> center-based [x,y,w,h]
        self.center = np.array([box[0] + box[2]/2, box[1] + box[3]/2])
        self.target_sz = np.array([box[2], box[3]])

        # Init
        self.state = SiamRPN_init(image, self.center, self.target_sz, self.net)


    def update(self, image):
        image = np.asarray(image)

        # track
        self.state = SiamRPN_track(self.state, image)

        # get box
        box = cxy_wh_2_rect(self.state['target_pos'], self.state['target_sz'])
        box = np.array([i for i in box])

        return box