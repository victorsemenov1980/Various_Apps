#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:44:40 2020

@author: user
"""


import sys
from PySide2.QtWidgets import QApplication, QWidget


class read(QWidget):
    def __init__(self):
        QWidget.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    window = read()
    window.show()
    sys.exit(app.exec_())