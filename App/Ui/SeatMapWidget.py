# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SeatMapWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_SeatMapWidget(object):
    def setupUi(self, SeatMapWidget):
        if not SeatMapWidget.objectName():
            SeatMapWidget.setObjectName(u"SeatMapWidget")
        SeatMapWidget.resize(890, 442)
        font = QFont()
        font.setKerning(True)
        SeatMapWidget.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(SeatMapWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(SeatMapWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageList = QWidget()
        self.pageList.setObjectName(u"pageList")
        self.verticalLayout = QVBoxLayout(self.pageList)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(self.pageList)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.pageList)
        self.pagePreview = QWidget()
        self.pagePreview.setObjectName(u"pagePreview")
        self.verticalLayout_4 = QVBoxLayout(self.pagePreview)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = QScrollArea(self.pagePreview)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.framePreview = QFrame(self.scrollAreaWidgetContents)
        self.framePreview.setObjectName(u"framePreview")
        self.framePreview.setFrameShape(QFrame.Shape.StyledPanel)
        self.framePreview.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.framePreview)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayoutPreview = QGridLayout()
        self.gridLayoutPreview.setObjectName(u"gridLayoutPreview")
        self.gridLayoutPreview.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.verticalLayout_6.addLayout(self.gridLayoutPreview)


        self.verticalLayout_7.addWidget(self.framePreview)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.pagePreview)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(SeatMapWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonDeleteAll = QPushButton(self.groupBox)
        self.pushButtonDeleteAll.setObjectName(u"pushButtonDeleteAll")
        self.pushButtonDeleteAll.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.pushButtonDeleteAll)

        self.pushButtonGenerate = QPushButton(self.groupBox)
        self.pushButtonGenerate.setObjectName(u"pushButtonGenerate")

        self.horizontalLayout_2.addWidget(self.pushButtonGenerate)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButtonPreview = QPushButton(SeatMapWidget)
        self.pushButtonPreview.setObjectName(u"pushButtonPreview")
        self.pushButtonPreview.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButtonPreview)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.groupBox_2 = QGroupBox(SeatMapWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBoxRows = QSpinBox(self.groupBox_2)
        self.spinBoxRows.setObjectName(u"spinBoxRows")
        self.spinBoxRows.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxRows)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBoxColumns = QSpinBox(self.groupBox_2)
        self.spinBoxColumns.setObjectName(u"spinBoxColumns")
        self.spinBoxColumns.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxColumns)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBoxSpacing = QSpinBox(self.groupBox_2)
        self.spinBoxSpacing.setObjectName(u"spinBoxSpacing")
        self.spinBoxSpacing.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxSpacing)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalSpacer = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.retranslateUi(SeatMapWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SeatMapWidget)
    # setupUi

    def retranslateUi(self, SeatMapWidget):
        SeatMapWidget.setWindowTitle(QCoreApplication.translate("SeatMapWidget", u"Seat Map", None))
        self.groupBox.setTitle(QCoreApplication.translate("SeatMapWidget", u"Massive editing", None))
        self.pushButtonDeleteAll.setText(QCoreApplication.translate("SeatMapWidget", u"Delete All", None))
        self.pushButtonGenerate.setText(QCoreApplication.translate("SeatMapWidget", u"Generate table numbers", None))
        self.pushButtonPreview.setText(QCoreApplication.translate("SeatMapWidget", u"Preview", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SeatMapWidget", u"Base geometry", None))
        self.label.setText(QCoreApplication.translate("SeatMapWidget", u"Rows", None))
        self.label_2.setText(QCoreApplication.translate("SeatMapWidget", u"Columns", None))
        self.label_3.setText(QCoreApplication.translate("SeatMapWidget", u"Spacing", None))
    # retranslateUi

