# Import library
import numpy as np
import math
from sklearn.decomposition import PCA


class block(object):
    def __init__(self, bw_image_block, rgb_image_block, koordinat_x, koordinat_y, dimensi_block):
        self.img_bw = bw_image_block
        self.img_bw_pixel = self.img_bw.load()

        if img_rgb_block != None:
            self.img_rgb = img_rgb_block
            self.img_rgb_pixel = self.img_rgb.load()
            self.is_img_rgb = True
        else:
            self.is_img_rgb = False

    def compute_block(self):
        block_list = []
        block_list.append(self.coordinate)
        block_list.append(self.feature_characteristic(precision=4))
        block_list.append(self.hitung_pca(precision=6))

        return block_list

    def hitung_pca(self, precision):
        modul_pca = PCA(n=1)
        if self.is_img_rgb:
            img_array = np.array(self.img_rgb)
            red = img_array[:, :, 0]
            green = img_array[:, :, 1]
            blue = img_array[:, :, 2]

            concate_array = np.concatenate(
                (red, np.concatenate((green, blue), axis=0)), axis=0)
            modul_pca.fit_transform(concate_array)
            principal_components = modul_pca.components_
            result = [round(element, precision)
                      for element in principal_components[0]]

            return result

        else:
            img_array = np.array(self.img_bw)
            modul_pca.fit_transform(img_array)
            principal_components = modul_pca.components_
            result = [round(element, precision)
                      for element in principal_components[0]]

            return result

    def feature_characteristic(self, precision):
        characteristic_list = []

        c4_1 = 0
        c4_2 = 0
        c5_1 = 0
        c5_2 = 0
        c6_1 = 0
        c6_2 = 0
        c7_1 = 0
        c7_2 = 0

        if self.is_img_rgb:
            sum_red = 0
            sum_green = 0
            sum_blue = 0
            for koordinat_y in range(0, self.dimension_block):
                for koordinat_x in range(0, self.dimension_block):
                    sum_red += self.img_rgb_pixel[koordinat_x, koordinat_y][0]
                    sum_green += self.img_rgb_pixel[koordinat_x,
                                                    koordinat_y][1]
                    sum_blue += self.img_rgb_pixel[koordinat_x, koordinat_y][2]

            sum_pixel = math.pow(self.dimension_block, 2)
            sum_red = sum_red / sum_pixel
            sum_green = sum_green / sum_pixel
            sum_blue = sum_blue / sum_pixel

            characteristic_list.append(sum_red)
            characteristic_list.append(sum_green)
            characteristic_list.append(sum_blue)

        else:
            characteristic_list.append(0)
            characteristic_list.append(0)
            characteristic_list.append(0)

        for koordinat_y in range(0, self.dimension_block):
            for koordinat_x in range(0, self.dimension_block):
                if koordinat_y in range(0, self.dimension_block):
                    if koordinat_y <= self.dimension_block / 2:
                        c4_1 += self.img_bw_pixel[koordinat_x, koordinat_y]
                    else:
                        c4_2 += self.img_bw_pixel[koordinat_x, koordinat_y]

                if koordinat_x in range(0, self.dimension_block):
                    if koordinat_x <= self.dimension_block / 2:
                        c5_1 += self.img_bw_pixel[koordinat_x, koordinat_y]
                    else:
                        c5_2 += self.img_bw_pixel[koordinat_x, koordinat_y]

                if koordinat_x - koordinat_y >= 0:
                    c6_1 += self.img_bw_pixel[koordinat_x, koordinat_y]
                else:
                    c6_2 += self.img_bw_pixel[koordinat_x, koordinat_y]

                if koordinat_x + koordinat_y <= self.dimension_block:
                    c7_1 += self.img_bw_pixel[koordinat_x, koordinat_y]
                else:
                    c7_2 += self.img_bw_pixel[koordinat_x, koordinat_y]

        characteristic_list.append(float(c4_1) / float(c4_1 + c4_2))
        characteristic_list.append(float(c5_1) / float(c5_1 + c5_2))
        characteristic_list.append(float(c6_1) / float(c6_1 + c6_2))
        characteristic_list.append(float(c7_1) / float(c7_1 + c7_2))

        result = [round(element, precision) for element in characteristic_list]
        return result
