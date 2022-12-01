""" 
Copyright (C) 2022  Nikolai Serafimovich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""

from PIL import Image
import os
import pathlib
import shutil

input_dir = 'input'
output_dir = 'output'
tile_size = 256

org_img = []

class Job:
    def __init__(self, fpath, outputd, tile_size):
        self.im = Image.open(fpath)

        self.folder_name = pathlib.Path(fpath).name.replace('.','_')
        self.working_dir = outputd + '/'+ self.folder_name
        self.tmp_folder = self.working_dir + '/tmp'
        self.file_extention = pathlib.Path(fpath).suffix

        print('Folder name: ' +self.folder_name + '\nCreating folder: ' + self.working_dir + '\nCreating folder: ' + self.tmp_folder)

        os.makedirs(self.tmp_folder)

        # resizing pictures
        it = find_z(tile_size, self.im.size[0])
        print('Levels: ' + str(it))
        p = 1
        for i in range(it):
            resized = self.im.resize((tile_size * p,tile_size * p))
            resized.save(self.tmp_folder +'/'+ str(i) + self.file_extention)
            print(self.tmp_folder +'/'+ str(i) + self.file_extention)
            p = p * 2

        #cropping pictures
        count = 1
        for i in range(it): 
            z = i
            os.makedirs(self.working_dir+'/'+ str(z))
            resized = Image.open(self.tmp_folder +'/'+ str(z)+self.file_extention)

            for x in range(int(resized.size[0] / tile_size)):
                os.makedirs(self.working_dir+'/'+ str(z) +'/'+ str(x))
                #print(int(resized.size[0] / tile_size))
                print('Exporting pictures: ' + str(count))

                for y in range(int(resized.size[1] / tile_size)):
                    tile = Tile(tile_size, x, y)
                    cropped = resized.crop((tile.p1[0], tile.p1[1], tile.p2[0], tile.p2[1]))
                    cropped.save(self.working_dir +'/'+ str(z) +'/'+ str(x) +'/'+ str(y) + self.file_extention)
                    count = count + 1

        #delete /tmp folder after that
        shutil.rmtree(self.tmp_folder)
        print('Done! (' + str(count) + ')')


class Tile:
    def __init__(self, size, x, y):
        self.ur = (x + 1) * size
        self.lr = (y + 1) * size

        self.p1 = (self.ur - size, self.lr - size)
        self.p2 = (self.ur, self.lr)

def find_z(tile_size, org_size):

    counted_size = org_size;
    it = 1

    while(counted_size > tile_size):
        counted_size = counted_size / 2
        it = it + 1

    return it

print("img2maptile  Copyright (C) 2022  Nikolai Serafimovich")

for filename in os.listdir(input_dir):

    con = input_dir +'/' + filename

    if pathlib.Path(con).suffix == '.jpg' or pathlib.Path(con).suffix == '.png':
        print('Found: ' +con)
        job = Job(con, output_dir, tile_size)