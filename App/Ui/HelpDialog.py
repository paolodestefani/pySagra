# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HelpDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSlider, QSpacerItem,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)
import resources_rc

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.setWindowModality(Qt.NonModal)
        HelpDialog.resize(1042, 549)
        HelpDialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(HelpDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButtonBack = QToolButton(HelpDialog)
        self.toolButtonBack.setObjectName(u"toolButtonBack")
        self.toolButtonBack.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonBack)

        self.toolButtonHome = QToolButton(HelpDialog)
        self.toolButtonHome.setObjectName(u"toolButtonHome")
        self.toolButtonHome.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonHome)

        self.toolButtonForward = QToolButton(HelpDialog)
        self.toolButtonForward.setObjectName(u"toolButtonForward")
        self.toolButtonForward.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonForward)

        self.toolButtonPrint = QToolButton(HelpDialog)
        self.toolButtonPrint.setObjectName(u"toolButtonPrint")
        self.toolButtonPrint.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonPrint)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label1 = QLabel(HelpDialog)
        self.label1.setObjectName(u"label1")
        self.label1.setWordWrap(False)
        self.label1.setMargin(2)

        self.horizontalLayout.addWidget(self.label1)

        self.horizontalSliderZoom = QSlider(HelpDialog)
        self.horizontalSliderZoom.setObjectName(u"horizontalSliderZoom")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSliderZoom.sizePolicy().hasHeightForWidth())
        self.horizontalSliderZoom.setSizePolicy(sizePolicy)
        self.horizontalSliderZoom.setMinimumSize(QSize(150, 0))
        self.horizontalSliderZoom.setMaximumSize(QSize(150, 16777215))
        self.horizontalSliderZoom.setMinimum(1)
        self.horizontalSliderZoom.setMaximum(7)
        self.horizontalSliderZoom.setPageStep(1)
        self.horizontalSliderZoom.setOrientation(Qt.Horizontal)
        self.horizontalSliderZoom.setTickPosition(QSlider.NoTicks)

        self.horizontalLayout.addWidget(self.horizontalSliderZoom)

        self.label2 = QLabel(HelpDialog)
        self.label2.setObjectName(u"label2")

        self.horizontalLayout.addWidget(self.label2)

        self.lineEditFind = QLineEdit(HelpDialog)
        self.lineEditFind.setObjectName(u"lineEditFind")
        self.lineEditFind.setMaxLength(64)

        self.horizontalLayout.addWidget(self.lineEditFind)

        self.toolButtonFind = QToolButton(HelpDialog)
        self.toolButtonFind.setObjectName(u"toolButtonFind")
        self.toolButtonFind.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonFind)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textBrowserContent = QTextBrowser(HelpDialog)
        self.textBrowserContent.setObjectName(u"textBrowserContent")
        self.textBrowserContent.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowserContent)

        QWidget.setTabOrder(self.toolButtonHome, self.toolButtonBack)
        QWidget.setTabOrder(self.toolButtonBack, self.toolButtonForward)
        QWidget.setTabOrder(self.toolButtonForward, self.horizontalSliderZoom)
        QWidget.setTabOrder(self.horizontalSliderZoom, self.lineEditFind)
        QWidget.setTabOrder(self.lineEditFind, self.toolButtonFind)
        QWidget.setTabOrder(self.toolButtonFind, self.textBrowserContent)

        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Help Dialog", None))
        self.toolButtonBack.setText(QCoreApplication.translate("HelpDialog", u"Back", None))
        self.toolButtonHome.setText(QCoreApplication.translate("HelpDialog", u"Home", None))
        self.toolButtonForward.setText(QCoreApplication.translate("HelpDialog", u"Forward", None))
        self.toolButtonPrint.setText(QCoreApplication.translate("HelpDialog", u"Print", None))
        self.label1.setText(QCoreApplication.translate("HelpDialog", u"Zoom:", None))
        self.label2.setText(QCoreApplication.translate("HelpDialog", u"Find text:", None))
        self.toolButtonFind.setText(QCoreApplication.translate("HelpDialog", u"Find", None))
    # retranslateUi

