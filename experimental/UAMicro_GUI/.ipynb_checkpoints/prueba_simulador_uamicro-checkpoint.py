#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Adriano / Oscar
"""
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QGraphicsPathItem

from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QPoint

import sys
import math

class Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.color = Qt.green
        self.ui = loadUi('UAMicro_GUI/prueba_dialog_uamicro.ui', self)
        self.ui.opPushButton.clicked.connect(self.op)

    def op(self):
        self.color = Qt.red if self.color == Qt.green else Qt.green
        self.update()
                
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        my_pen = QPen()
        my_pen.setWidth(1)
        my_pen.setCosmetic(False)
        my_pen.setColor(QColor(255, 0, 0, 100))
        painter.setPen(my_pen)
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))

        #arrow = Arrow(QPointF(200, 120), QPointF(425, 120), 10, 10, 5)
        width = self.width()
        height = self.height()
        
        start = QPointF(width * 0.35, height / 1.8)
        end = QPointF(width * 0.65, height / 1.8)
        
        arrow = Arrow(start, end, 10, 10, 5)
        arrow_polygon = arrow.arrowCalc()
        if arrow_polygon is not None:
            #self.painter.drawPolyline(arrow_polygon)
            painter.drawPolygon(arrow_polygon)

class Arrow(QGraphicsPathItem):

    def __init__(self, source: QPointF, destination: QPointF, arrow_height, arrow_width, length_width, *args, **kwargs):
        super(Arrow, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination

        self._arrow_height = arrow_height
        self._arrow_width = arrow_width
        self._length_width = length_width

    def arrowCalc(self, start_point=None, end_point=None):

        try:
            startPoint, endPoint = start_point, end_point

            if start_point is None:
                startPoint = self._sourcePoint

            if endPoint is None:
                endPoint = self._destinationPoint

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng
            
            perpX = -normY
            perpY = normX
            
            
            #           p2
            #           |\
            #    p4____p5 \
            #     |        \ endpoint
            #    p7____p6  /
            #           | /
            #           |/
            #          p3
            
            point2 = endPoint + QPointF(normX, normY) * self._arrow_height + QPointF(perpX, perpY) * self._arrow_width
            point3 = endPoint + QPointF(normX, normY) * self._arrow_height - QPointF(perpX, perpY) * self._arrow_width

            point4 = startPoint + QPointF(perpX, perpY) * self._length_width
            point5 = endPoint + QPointF(normX, normY) * self._arrow_height + QPointF(perpX, perpY) * self._length_width
            point6 = endPoint + QPointF(normX, normY) * self._arrow_height - QPointF(perpX, perpY) * self._length_width
            point7 = startPoint - QPointF(perpX, perpY) * self._length_width

            return QPolygonF([point4, point5, point2, endPoint, point3, point6, point7])

        except (ZeroDivisionError, Exception):
            return None

        
App = QApplication(sys.argv)
dialog = Dialog()
dialog.show()
sys.exit(App.exec())
