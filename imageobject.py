# Import class lain
import container
import block

# Import library
import numpy as np
import math
import time
import imageio
import tqdm
from PIL import Image


class ImageObject(object):
    def __init__(self):
        print("Nama Image: ", img_name)
        print("Step 1 dari 4: Mengambil data dari gambar")

        self.img_output_dir = output_dir
        self.img_name = img_name
        self.img_data = Image.open(input_path)
        self.img_width, self.img_height = self.img_data.size

        if self.img_data.mode == "RGB":
            self.is_img_rgb = True
            self.img_data = self.img_data.convert("RGB")
            rgb_img = self.img_data.load()
            self.img_bw = self.img_data.convert("L")
            img_bw = self.img_bw.load()

            for koordinat_y in range(0, self.img_height):
                for koordinat_x in range(0, self.img_width):
                    red_pixel, green_pixel, blue_pixel = rgb_img[koordinat_x, koordinat_y]
                    img_bw[koordinat_x, koordinat_y] = int(
                        0.299 * red_pixel + 0.587 * green_pixel + 0.114 * blue_pixel)

        else:
            self.is_img_rgb = False
            self.img_bw = self.img_data.convert("L")

        self.N = self.img_height * self.img_width
        self.block_dimension = block_dimension
        self.countB = self.block_dimension * self.block_dimension
        self.Nb = (self.img_height - self.block_dimension + 1) * \
            (self.img_width - self.block_dimension + 1)
        # Banyak n block yang akan dihitung
        self.Nn = 2
        # Minimum threshold offset frequency
        self.Nf = 188
        # Minimum threshold offset magnitude
        self.Nd = 50

        self.p = (1.80, 1.80, 1.80, 0.0125, 0.0125, 0.0125, 0.125)
        self.t1 = 2.80
        self.t2 = 0.02
        print(self.Nb, self.is_img_rgb)

        self.feature_container = container.Container()
        self.block_pair_container = container.Container()
        self.offset_dict = {}

    def run(self):
        start_time = time.time()
        self.compute()
        time_after_compute = time.time()
        self.sort()
        time_after_sort = time.time()
        self.analyze()
        time_after_analyze = time.time()
        img_result_path = self.reconstruct()
        time_after_reconstruct = time.time()

        print("waktu eksekusi: ", time_after_compute - start_time, "detik")
        print("waktu sorting: ", time_after_sort - time_after_compute, "detik")
        print("waktu analisis: ", time_after_analyze - time_after_sort, "detik")
        print("waktu reconstruction: ", time_after_reconstruct -
              time_after_analyze, "detik")

        total_running_second = time_after_compute - start_time
        total_minutes, total_second = divmod(total_running_second, 60)
        total_hours, total_minutes = divmod(total_minutes, 60)
        print("Total waktu eksekusi: ", total_hours, "jam",
              total_minutes, "menit", total_second, "detik")

        return img_result_path
