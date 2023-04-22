import random
import numpy as np
import torch.utils.data as data
import utils.utils_image as util
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
import csv

class DatasetSR(data.Dataset):
    '''
    # -----------------------------------------
    # Get L/H for SISR.
    # If only "paths_H" is provided, sythesize bicubicly downsampled L on-the-fly.
    # -----------------------------------------
    # e.g., SRResNet
    # -----------------------------------------
    '''

    def __init__(self, opt):
        super(DatasetSR, self).__init__()
        self.opt = opt
        self.n_channels = opt['n_channels'] if opt['n_channels'] else 3
        self.sf = opt['scale'] if opt['scale'] else 4
        self.patch_size = self.opt['H_size'] if self.opt['H_size'] else 96
        self.L_size = self.patch_size // self.sf

        # ------------------------------------
        # get paths of L/H
        # ------------------------------------
        assert opt['dataroot'] != None, 'NO DATAROOT SET'
        with open(opt['dataroot']) as f:
            reader = csv.reader(f)
            paths = list(tuple(line) for line in reader)

        self.paths = np.array(paths)
        np.random.shuffle(self.paths)
        self.paths_H = self.paths[:, 0].tolist()
        self.paths_L = self.paths[:, 1].tolist()
        print("Number of HDR photos: ",len(self.paths_H))
        print("Number of SDR photos: ",len(self.paths_L))

        assert self.paths_H, 'Error: H path is empty.'
        if self.paths_L and self.paths_H:
            assert len(self.paths_L) == len(self.paths_H), 'L/H mismatch - {}, {}.'.format(len(self.paths_L), len(self.paths_H))
            # \
            #                                                            '\n self.paths_L = {} ' \
            #                                                            '\n self.paths_H = {}
            # self.paths_L, self.paths_H

    def __getitem__(self, index):

        L_path = None
        # ------------------------------------
        # get H image
        # ------------------------------------
        H_path = self.paths_H[index]
        # img_H = util.imread_uint(H_path, self.n_channels)
        img_H = cv2.imread(H_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)   # ADDED THIS LINE
        # img_H = util.uint2single(img_H)   # This converts from 0-255 to 0-1.0
        
        # I WROTE THIS PART
        # Gets rid of the full black images
        while (os.path.getsize(H_path)<500000):
            del self.paths_H[index]
            del self.paths_L[index]
            try:
                H_path = self.paths_H[index]
                print("Not using this img (too small):",self.paths_H[index])
            except IndexError:
                H_path = self.paths_H[index-1]
                break

        # ------------------------------------
        # modcrop
        # ------------------------------------
        #img_H = util.modcrop(img_H, self.sf)

        # ------------------------------------
        # get L image
        # ------------------------------------
        if self.paths_L:
            # --------------------------------
            # directly load L image
            # --------------------------------
            try:
                L_path = self.paths_L[index]
            except IndexError:
                L_path = self.paths_L[index-1]
            
                
            # L_path = self.paths_L[index]
            # img_L = util.imread_uint(L_path, self.n_channels)
            img_L = cv2.imread(L_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)     # ADDED THIS LINE
            # img_L = util.uint2single(img_L)     # This converts from 0-255 to 0-1.0

        else:
            # --------------------------------
            # sythesize L image via matlab's bicubic
            # --------------------------------
            H, W = img_H.shape[:2]
            #img_L = util.imresize_np(img_H, 1 / self.sf, True)

        # ------------------------------------
        # if train, get L/H patch pair
        # ------------------------------------
        if True: #self.opt['phase'] == 'train':

            H, W, C = img_L.shape

            # --------------------------------
            # randomly crop the L patch
            # --------------------------------
            rnd_h = random.randint(0, max(0, H - self.L_size))
            rnd_w = random.randint(0, max(0, W - self.L_size))
            img_L = img_L[rnd_h:rnd_h + self.L_size, rnd_w:rnd_w + self.L_size, :]

            # --------------------------------
            # crop corresponding H patch
            # --------------------------------
            rnd_h_H, rnd_w_H = int(rnd_h * self.sf), int(rnd_w * self.sf)
            img_H = img_H[rnd_h_H:rnd_h_H + self.patch_size, rnd_w_H:rnd_w_H + self.patch_size, :]

            # --------------------------------
            # augmentation - flip and/or rotate
            # --------------------------------
            mode = random.randint(0, 7)
            img_L, img_H = util.augment_img(img_L, mode=mode), util.augment_img(img_H, mode=mode)
        

        # ------------------------------------
        # L/H pairs, HWC to CHW, numpy to tensor
        # ------------------------------------
        img_H, img_L = util.single2tensor3(img_H), util.single2tensor3(img_L)

        if L_path is None:
            L_path = H_path

        return {'L': img_L, 'H': img_H, 'L_path': L_path, 'H_path': H_path}

    def __len__(self):
        return len(self.paths_H)
