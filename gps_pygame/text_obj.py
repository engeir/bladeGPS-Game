"""Script for handling text on the pygame display.
"""

import pygame as pg

import config as cf


class Text:
    """Make an object that show all the text needed for the spoofer.

    Methods 'text_objects' and 'message_display' are copied
    from https://pythonprogramming.net/displaying-text-pygame-screen/.
    Changed a bit to better fit the rest of the code.
    """

    def text_objects(self, msg, font, color):
        """Make a text object ready to be blitted to the screen.

        Arguments:
            msg {str} -- the text you want to present
            font {pygame.font.Font} -- font type and size
            color {tuple} -- tuple that give the RGB color

        Returns:
            pygame surface -- pygame surface object that can be displayed
        """
        text_surface = font.render(msg, True, color)
        return text_surface, text_surface.get_rect()

    def message_display(self, msg, color, posx, posy, size, screen):
        """Display a text object and center it at a given x/y-position.

        Arguments:
            msg {str} -- the text you want to present
            color {tuple} -- tuple that give the RGB color
            posx {int} -- position on the pygame surface x-axis where you want the text box to be centered
            posy {int} -- position on the pygame surface y-axis where you want the text box to be centered
            size {int} -- the font size of the text
            screen {pygame surface} -- the pygame surface you want the text to be blitted to
        """
        text = pg.font.Font('Ovo-Regular.ttf', size)
        TextSurf, TextRect = self.text_objects(msg, text, color)
        TextRect.topleft = (posx, posy)
        screen.blit(TextSurf, TextRect)

    def text_update(self, vel, screen):
        self.message_display(f"Fart: {round(vel * 30 * 3.6, 1)} km/h",
                             cf.TEXT_COLOR, cf.VEL_X, cf.VEL_Y, cf.TEXT_SIZE, screen)
        self.message_display('N',
                             cf.TEXT_COLOR, cf.N_X, cf.N_Y, cf.TEXT_SIZE, screen)
        self.message_display('S',
                             cf.TEXT_COLOR, cf.S_X, cf.S_Y, cf.TEXT_SIZE, screen)
        self.message_display('Ø',
                             cf.TEXT_COLOR, cf.E_X, cf.E_Y, cf.TEXT_SIZE, screen)
        self.message_display('V',
                             cf.TEXT_COLOR, cf.W_X, cf.W_Y, cf.TEXT_SIZE, screen)
