"""Script that starts PyGame and that the user interacts with.

Author: Eirik Rolland Enger
"""

import os
import sys
import time
import subprocess
import multiprocessing as mp
import pygame as pg
from geographiclib.geodesic import Geodesic
import serial

import config as cf
from arrow import Arrow
from mapper import Map
from text_obj import Text

try:
    gps = serial.Serial('/dev/ttyACM0', baudrate=9600)
except Exception:
    print("The port cannot be opened. Check that your unit is connected to the port you're opening.")
    exit()


class TheGame:
    """Make an object that runs the simulation.
    """

    def __init__(self):
        """Initiate all instances of the classes that are needed for the simulation, and start PyGame.

        Raises:
            Exception: If you fail to choose a valid simulation setting, an Exception is raised.
        """
        while True:
            try:
                string = str(
                    input('Do you want to take in live GNSS-signals? (y/n)\t'))
                if string in ('y', 'yes'):
                    self.test_mode_on = False
                elif string in ('n', 'no'):
                    self.test_mode_on = True
                else:
                    raise Exception
            except Exception:
                print('Please type "y" or "n".')
            else:
                break
        self.clock = pg.time.Clock()
        self.the_arrow = Arrow()
        self.map = Map(60.75, 11.99)
        self.the_text = Text()
        self.earth = Geodesic(cf.R_E, 0)
        self.out_q = mp.Manager().Value('i', [0.0, 0.0])
        self.NS = self.map.center_y
        self.EW = self.map.center_x
        self.the_background = pg.image.load('background.jpg')
        self.process = False
        self.background = False
        self.dot_x, self.dot_y = self.the_arrow.two_d_pos.x, self.the_arrow.two_d_pos.y
        self.pastNS, self.pastEW = self.NS, self.EW
        try:
            self.g_earth = subprocess.Popen('google-earth-pro')
        except Exception:
            pass
        # Wait for Google Earth Pro to open so that the PyGame window opens as the top layer.
        time.sleep(5)
        pg.init()
        pg.display.set_caption("Real time spoofer")
        self.screen = pg.display.set_mode(
            (cf.SCREEN_WIDTH, cf.SCREEN_HEIGHT))
        with open("log.txt", "w") as log:
            log.write("")

    def events(self):
        """Event handling.
        """
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT]:
            # LEFT rotates 'dir' to the left, one degree at the time.
            self.the_arrow.dir = self.the_arrow.dir.rotate(-1).normalized()
        if pressed[pg.K_RIGHT]:
            # RIGHT rotates 'dir' to the right, one degree at the time.
            self.the_arrow.dir = self.the_arrow.dir.rotate(1).normalized()
        if pressed[pg.K_UP] and self.the_arrow.vel < cf.MAX_VEL:
            # UP increases the speed.
            self.the_arrow.vel += cf.AXELERATION
        if pressed[pg.K_DOWN] and self.the_arrow.vel > - cf.MAX_VEL:
            # DOWN decreases the speed and let you move backwards.
            self.the_arrow.vel -= cf.AXELERATION
        if not pressed[pg.K_UP] and self.the_arrow.vel >= 0.0:
            # When you release the "throttle" (UP), you slowly go to a stop,
            # but as long as you have some speed, 'two_d_pos' should be updated.
            self.the_arrow.vel -= cf.GLIDING
        if not pressed[pg.K_DOWN] and self.the_arrow.vel <= 0.0:
            self.the_arrow.vel += cf.GLIDING

    def test_mode(self):
        """With test mode, you do not check with the receiver what
        coordinates its got, you just move from the static starting position.
        """
        with open("position.txt", "w") as pos:
            pos.write("%s\n%s\n" % (str(self.NS), str(self.EW)))
        with open("position.kml", "w") as kml:
            kml.write("""<?xml version="1.0" encoding="UTF-8"?>
                <kml xmlns="http://www.opengis.net/kml/2.2">
                <Placemark>
                <name>Spoofer Position</name>
                <description>Track a spoofed GNSS-position</description>
                <Point>
                    <coordinates>%s,%s,0</coordinates>
                </Point>
                </Placemark>
                </kml>
            """ % (str(self.EW), str(self.NS)))
        with open("log.txt", "a") as log:
            log.write("%s\t%s\n" % (str(self.NS), str(self.EW)))

    def check_coordinates(self, out_q):
        """Check GPS/GLONASS-coordinates from the receiver, add the off-set and write it to a file.
        """
        line = gps.readline().decode("utf-8")
        data = line.split(',')
        if data[0] == "$GNRMC":
            if data[2] == "A":
                print("3D fix.", end='\r')
                with open("position.txt", "w") as pos:
                    # Convert from XXYY.YY... (X: degree, Y: decimal minute) to decimal degree (XX.XX...).
                    DDM_NS = float(data[3]) / 100
                    DDM_EW = float(data[5]) / 100
                    DD_NS = DDM_NS - DDM_NS % 1 + \
                        (DDM_NS % 1) / 60 * 100
                    DD_EW = DDM_EW - DDM_EW % 1 + \
                        (DDM_EW % 1) / 60 * 100
                    # North in the negative y-direction.
                    NS, EW = DD_NS - self.the_arrow.two_d_pos.y, \
                        DD_EW + self.the_arrow.two_d_pos.x
                    pos.write("%s\n%s\n" % (str(NS), str(EW)))
                    out_q.value = [NS, EW]
                # Write a kml-file with the spoofing position.
                with open("position.kml", "w") as kml:
                    kml.write("""<?xml version="1.0" encoding="UTF-8"?>
                        <kml xmlns="http://www.opengis.net/kml/2.2">
                        <Placemark>
                        <name>Spoofer Position</name>
                        <description>Track a spoofed GNSS-position</description>
                        <Point>
                            <coordinates>%s,%s,0</coordinates>
                        </Point>
                        </Placemark>
                        </kml>
                    """ % (str(EW), str(NS)))
                with open("log.txt", "a") as log:
                    log.write("%s\t%s\n" % (str(NS), str(EW)))
            elif data[2] == "V":
                print("No fix.", end='\r')

    def parallel_coordinates(self):
        """Allow check of coordinates to be done in parallel with the controlling of the arrow,
        such that updating the coordinates does not interfere and stop the rest of the program.
        """
        if not self.process:
            # If no process exists, make one and start it off.
            self.process = mp.Process(
                target=self.check_coordinates, args=(self.out_q,))
            self.process.start()
        else:
            try:
                self.process.start()
            except Exception:
                pass
        if not self.process.is_alive():
            # If the process is done, it can be closed/joined to allow a
            # new one to be opened in the next round of the loop.
            # Before it is closed, the values returned by 'check_coordinates()' are captured.
            a = self.out_q
            self.NS = a.value[0]
            self.EW = a.value[1]
            self.process.join()
            self.process = False

    def parallel_background(self):
        """Allow the background that is blitted to the PyGame surface to be
        updated without interfering and stopping the rest of the program.
        """
        # Make the background update only when you approach the edge of the canvas.
        if (self.pastNS + cf.BOARDER_Y * 0.8) < self.NS or self.NS < (self.pastNS - cf.BOARDER_Y * 0.8) or \
           (self.pastEW + cf.BOARDER_X * 0.8) < self.EW or self.EW < (self.pastEW - cf.BOARDER_X * 0.8):
            if not self.background:
                self.background = mp.Process(
                    target=self.map.map_update, args=(self.NS, self.EW))
                self.background.start()
            else:
                try:
                    self.background.start()
                except Exception:
                    pass
        try:
            if not self.background.is_alive():
                # When the canvas is updated, reset the dot to the center.
                self.background.join()
                self.background = False
                self.dot_x = self.dot_y = 0
                self.pastNS = self.NS
                self.pastEW = self.EW
        except Exception:
            pass

    def draw_dot(self):
        """Draw a dot representing the spoofing signal.
        """
        x_ratio = 2 * cf.BOARDER_X / cf.SCREEN_WIDTH
        y_ratio = 2 * cf.BOARDER_Y / cf.SCREEN_HEIGHT
        x = int(self.dot_x / x_ratio + cf.SCREEN_WIDTH / 2)
        y = int(self.dot_y / y_ratio + cf.SCREEN_HEIGHT / 2)
        pg.draw.circle(self.screen, cf.DOT_COLOR, (x, y), cf.DOT_SIZE, cf.DOT_FILLED)

    def game_loop(self):
        """Loop that runs the simulation and calls all methods.
        """
        while 1:
            self.events()
            self.NS, self.EW, self.dot_y, self.dot_x = self.the_arrow.globe_motion(
                self.earth, self.NS, self.EW, self.dot_y, self.dot_x)
            if self.test_mode_on:
                self.test_mode()
            else:
                self.parallel_coordinates()
            self.parallel_background()
            # Prevent irrelevant error from printing to bash.
            sys.stdout = open(os.devnull, "w")
            if os.path.exists('background.jpg'):
                try:
                    self.the_background = pg.image.load('background.jpg')
                except Exception:
                    pass
            # Redirect printing back to bash.
            sys.stdout = sys.__stdout__
            self.screen.fill(cf.BLACK)
            self.screen.blit(self.the_background, (0, 0))
            self.the_arrow.draw(self.screen)
            self.the_text.text_update(self.the_arrow.vel, self.screen)
            self.draw_dot()
            pg.display.update()
            self.clock.tick(cf.FPS)


if __name__ == "__main__":
    TheGame().game_loop()
