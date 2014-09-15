from __future__ import division

import PyQt4
import threading
import sys
import time
from PyQt4 import QtGui


class QT4WriterWindow(QtGui.QMainWindow):
    def __init__(self, win_parent=None):
        QtGui.QMainWindow.__init__(self, win_parent)
        self._setup_widgets()

    def _setup_widgets(self):
        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)
        label = QtGui.QLabel("hello")
        h_box = QtGui.QHBoxLayout()
        h_box.addWidget(label)
        central_widget.setLayout(h_box)


class QT4Writer(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = QT4WriterWindow()
    main_window.show()
    print "built app"
    t = threading.Thread(target=app.exec_)
    t.daemon = True
    t.start()
    # app.exec_()
    print "here"
    time.sleep(5)
    t.join()

