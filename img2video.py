"""
Convert images to video
@ fansiqi  2020.4.22
"""
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

import os
import fnmatch

from tqdm import tqdm

def find_files(directory, pattern):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path list
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                file_list.append(filename)
    file_list = sorted(file_list)
    
    return file_list

def img2video(path, img_type="jpg"):
    """
    Convert images to video
    Parameter:
        path: path to images
        img_type: image files' type. e.g. "jpg", "png"....
    """
    # Get img info
    img = cv2.imread(path+"/00000001.jpg")
    h, w = img.shape[:2]

    # Init video
    video = cv2.VideoWriter(path+".avi", cv2.VideoWriter_fourcc(*'MJPG'), 10, (w, h))

    # img2video
    for file_path in tqdm(find_files(path+"/", '*.'+img_type)):
        img = cv2.imread(file_path)
        video.write(img)
    video.release()
    print('Videos saved at', path[-6:]+".avi")


if __name__ == "__main__":
    path = "/home/leofansq/Class&Homework/视频处理与分析/hw/2/siamfc/data/GOT-10k/test/GOT-10k_Test_{:06d}"
    img_type = "jpg"

    for i in range(1):
        img2video(path.format(i+1), img_type)