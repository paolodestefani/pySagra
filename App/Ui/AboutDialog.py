# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(800, 560)
        self.verticalLayout_4 = QVBoxLayout(AboutDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelIcon = QLabel(AboutDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout.addWidget(self.labelIcon)

        self.labelAnimation = QLabel(AboutDialog)
        self.labelAnimation.setObjectName(u"labelAnimation")

        self.verticalLayout.addWidget(self.labelAnimation)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.scrollArea = QScrollArea(AboutDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 726, 492))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.labelAbout = QLabel(self.scrollAreaWidgetContents)
        self.labelAbout.setObjectName(u"labelAbout")
        self.labelAbout.setWordWrap(True)
        self.labelAbout.setOpenExternalLinks(True)

        self.verticalLayout_3.addWidget(self.labelAbout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(AboutDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.button_box.setCenterButtons(True)

        self.verticalLayout_4.addWidget(self.button_box)


        self.retranslateUi(AboutDialog)
        self.button_box.accepted.connect(AboutDialog.accept)
        self.button_box.rejected.connect(AboutDialog.reject)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About", None))
        self.labelIcon.setText(QCoreApplication.translate("AboutDialog", u"ICN", None))
        self.labelAnimation.setText(QCoreApplication.translate("AboutDialog", u"GIF", None))
        self.labelAbout.setText(QCoreApplication.translate("AboutDialog", u"About", None))
    # retranslateUi

