"""Script that implement a way of downloading map tiles and saving them as .png-files.
"""

import os
import sys
import PIL.Image as Image
import pygame as pg
from osmviz.manager import OSMManager, PILImageManager

import config as cf

# Adds this files location to path.
os.environ["PATH"] += os.pathsep + "."


class Map:
    """Make a map that follows the spoofing coordinate.
    """

    def __init__(self, center_y, center_x):
        self.center_x = center_x
        self.center_y = center_y
        min_lat, max_lat, min_lon, max_lon = center_y - \
            cf.BOARDER_Y, center_y + cf.BOARDER_Y, center_x - \
            cf.BOARDER_X, center_x + cf.BOARDER_X
        imgr = PILImageManager('RGB')
        osm = OSMManager(image_manager=imgr)
        # min_lat, max_lat, min_lon, max_lon, OSM-zoom
        image, _ = osm.createOSMImage(
            (min_lat, max_lat, min_lon, max_lon), cf.MAP_ZOOM)
        wh_ratio = float(image.size[0]) / image.size[1]
        image2 = image.resize((int(800 * wh_ratio), 800), Image.ANTIALIAS)
        mode = image2.mode
        size = image2.size
        data = image2.tobytes()
        self.image = pg.image.fromstring(data, size, mode)
        pg.image.save(self.image, 'background.jpg')

    def map_update(self, center_y, center_x):
        """Fetch the map tiles at the current coordinate.

        Arguments:
            center_y {float} -- the latitudinal coordinate
            center_x {float} -- the longitudinal coordinate
        """
        sys.stdout = open(os.devnull, "w")
        min_lat, max_lat, min_lon, max_lon = center_y - \
            cf.BOARDER_Y, center_y + cf.BOARDER_Y, center_x - \
            cf.BOARDER_X, center_x + cf.BOARDER_X
        imgr = PILImageManager('RGB')
        osm = OSMManager(image_manager=imgr)
        # min_lat, max_lat, min_lon, max_lon, OSM-zoom
        image, _ = osm.createOSMImage(
            (min_lat, max_lat, min_lon, max_lon), cf.MAP_ZOOM)
        wh_ratio = float(image.size[0]) / image.size[1]
        image2 = image.resize((int(1000 * wh_ratio), 800),
                              Image.ANTIALIAS)
        mode = image2.mode
        size = image2.size
        data = image2.tobytes()
        self.image = pg.image.fromstring(data, size, mode)
        pg.image.save(self.image, 'background.jpg')
        sys.stdout = sys.__stdout__
