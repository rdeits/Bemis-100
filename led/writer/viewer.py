from __future__ import division

import PyQt4
import sys
import json
import threading
from PyQt4 import QtGui ,QtCore
from led.ledctl import WriterNode


class LCMViewerWindow(QtGui.QMainWindow, WriterNode):
    def __init__(self, win_parent=None, **kwargs):
        WriterNode.__init__(self, **kwargs)
        QtGui.QMainWindow.__init__(self, win_parent)
        self.color_data = [QtGui.QColor(0,0,0)]*50
        self.frame_draw_lock = threading.Lock()
        self._setup_widgets()
        self.handler_thread = threading.Thread(target=self.start)
        self.handler_thread.daemon = True
        self.handler_thread.start()
        self._width = 0

    def _setup_widgets(self):
        self.setGeometry(300, 500, 5*50, 20)
        self.show()
        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)

    def set_width(self, width):
        if width != self._width:
            self.setMinimumWidth(width)
            self.setMaximumWidth(width)
            self._width = width

    # TODO:
    # it looks like a race condition. paintEvent is happening while
    # the color data is still being updated, which causes the size to
    # go crazy

    def paintEvent(self, event):
        with self.frame_draw_lock:
            self.set_width(5 * len(self.color_data))
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setPen(QtCore.Qt.black)
            for i, color in enumerate(self.color_data):
                qp.fillRect(i*5,0,5,20,color)
            qp.end()

    def draw_frame(self, frame):
        with self.frame_draw_lock:
            self.color_data = []
            for pixel in frame:
                self.color_data.append(QtGui.QColor(*pixel))
            self.central_widget.update()

if __name__ == '__main__':
    app = QtGui.QApplication([sys.argv[0]])
    main_window = LCMViewerWindow(**json.loads(sys.argv[1]))
    sys.exit(app.exec_())

