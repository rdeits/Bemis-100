from __future__ import division

import PyQt4
import sys
import lcm
import threading
import numpy as np
from PyQt4 import QtGui ,QtCore
import bemis100LCM


class LCMViewerWindow(QtGui.QMainWindow):
    def __init__(self, win_parent=None):
        QtGui.QMainWindow.__init__(self, win_parent)
        self.color_data = [QtGui.QColor(0,0,0)]*50
        self._setup_widgets()
        self._setup_subscriptions()

    def _setup_widgets(self):
        self.setGeometry(300, 500, 5*50, 20)
        self.show()
        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)
        # label = QtGui.QLabel("hello")
        # h_box = QtGui.QHBoxLayout()
        # h_box.addWidget(label)
        # self.qp = QtGui.QPainter()

        # central_widget.setLayout(h_box)

    def _setup_subscriptions(self):
        self.lc = lcm.LCM()
        self.lc.subscribe("BEMIS_100_DRAW", self.handle_frame_message)
        self.handler_thread = threading.Thread(target=self.run_handler)
        self.handler_thread.daemon = True
        self.handler_thread.start()

    def run_handler(self):
        while True:
            self.lc.handle()

    def paintEvent(self, event):
        self.setMinimumWidth(5*len(self.color_data))
        self.setMaximumWidth(5*len(self.color_data))
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtCore.Qt.black)
        for i, color in enumerate(self.color_data):
            qp.fillRect(i*5,0,5,20,color)
        qp.end()

    def handle_frame_message(self, channel, data):
        msg = bemis100LCM.frame_t.decode(data)
        self.color_data = []
        for i in range(msg.n_pixels):
            self.color_data.append(QtGui.QColor(ord(msg.red[i]), ord(msg.green[i]), ord(msg.blue[i])))
        self.central_widget.update()


class LCMWriter(object):
    def __init__(self):
        self.lc = lcm.LCM()
        self.is_alive = lambda: True

    def draw_frame(self, frame):
        msg = bemis100LCM.frame_t()
        msg.n_pixels = len(frame) // 3
        frame = np.asarray(frame)
        msg.red = frame[range(0, len(frame), 3)]
        msg.green = frame[range(1, len(frame), 3)]
        msg.blue = frame[range(2, len(frame), 3)]
        self.lc.publish('BEMIS_100_DRAW', msg.encode())

    def setup(self, i, o):
        pass

    def start(self):
        pass

    def send_frame(self, frame):
        self.draw_frame(frame)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = LCMViewerWindow()
    sys.exit(app.exec_())

