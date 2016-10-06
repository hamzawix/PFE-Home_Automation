import vlc
import sys

class StreamReader(object):
    def __init__(self, url):
        self.URL = url
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.player.set_mrl(self.URL)

    def MultiplatformSupport(self, frame_obj):
        """
        support for GNU/Linux
        """
        if sys.platform.startswith('linux'):
            self.player.set_xwindow(frame_obj.winId())
        """
        support for Apple's OS X
        """
        if sys.platform == 'darwin':
            self.player.set_nsobject(frame_obj.winId())
        """
        support for Microsoft's Windows
        """
        if sys.platform == 'win32':
            self.player.set_hwnd(frame_obj.winId())
