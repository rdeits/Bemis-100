from __future__ import division

import PyQt4
import sys
import lcm
import threading
from PyQt4 import QtGui ,QtCore
import bemis100LCM


class LCMViewerWindow(QtGui.QMainWindow):
    def __init__(self, win_parent=None):
        QtGui.QMainWindow.__init__(self, win_parent)
        self.color_data = [QtGui.QColor(0,0,0)]*50
        self._setup_widgets()
        self._setup_subscriptions()

    def _setup_widgets(self):
        self.setGeometry(300, 500, 5*50, 30)
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
        self.handler_thread = threading.Thread(target=self.lc.handle)
        self.handler_thread.daemon = True
        self.handler_thread.start()

    def paintEvent(self, event):
        self.setGeometry(300,500, 5*len(self.color_data), 30)
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtCore.Qt.black)
        for i, color in enumerate(self.color_data):
            qp.fillRect(i*5,0,5,20,color)
        qp.end()

    def handle_frame_message(self, channel, data):
        msg = bemis100LCM.frame_t.decode(data)
        print msg.n_pixels
        self.color_data = []
        for i in range(msg.n_pixels):
            self.color_data.append(QtGui.QColor(ord(msg.red[i]), ord(msg.green[i]), ord(msg.blue[i])))
        self.central_widget.update()


class LCMWriter(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = LCMViewerWindow()
    sys.exit(app.exec_())

