# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SelectImageDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SelectImageDialog(object):
    def setupUi(self, SelectImageDialog):
        if not SelectImageDialog.objectName():
            SelectImageDialog.setObjectName(u"SelectImageDialog")
        SelectImageDialog.resize(380, 292)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SelectImageDialog.sizePolicy().hasHeightForWidth())
        SelectImageDialog.setSizePolicy(sizePolicy)
        SelectImageDialog.setMinimumSize(QSize(380, 292))
        SelectImageDialog.setMaximumSize(QSize(380, 292))
        SelectImageDialog.setLocale(QLocale(QLocale.C, QLocale.AnyCountry))
        self.verticalLayout_7 = QVBoxLayout(SelectImageDialog)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(SelectImageDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.labelImage = QLabel(self.groupBox)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setMinimumSize(QSize(200, 200))
        self.labelImage.setFrameShape(QFrame.NoFrame)
        self.labelImage.setScaledContents(False)
        self.labelImage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.labelImage)


        self.horizontalLayout.addWidget(self.groupBox)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_2 = QGroupBox(SelectImageDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.lineEditWidth = QLineEdit(self.groupBox_2)
        self.lineEditWidth.setObjectName(u"lineEditWidth")
        self.lineEditWidth.setEnabled(False)
        self.lineEditWidth.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEditWidth.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditWidth, 0, 1, 1, 1)

        self.lineEditHeight = QLineEdit(self.groupBox_2)
        self.lineEditHeight.setObjectName(u"lineEditHeight")
        self.lineEditHeight.setEnabled(False)
        self.lineEditHeight.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEditHeight.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditHeight, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(SelectImageDialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditImageFormat = QLineEdit(self.groupBox_3)
        self.lineEditImageFormat.setObjectName(u"lineEditImageFormat")
        self.lineEditImageFormat.setEnabled(False)
        self.lineEditImageFormat.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.lineEditImageFormat)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(SelectImageDialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.spinBoxPixmapSize = QDoubleSpinBox(self.groupBox_4)
        self.spinBoxPixmapSize.setObjectName(u"spinBoxPixmapSize")
        self.spinBoxPixmapSize.setEnabled(False)
        self.spinBoxPixmapSize.setReadOnly(True)
        self.spinBoxPixmapSize.setDecimals(3)
        self.spinBoxPixmapSize.setMaximum(9999999.990000000223517)

        self.verticalLayout_4.addWidget(self.spinBoxPixmapSize)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.verticalSpacer_2 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonUpload = QPushButton(SelectImageDialog)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout_2.addWidget(self.pushButtonUpload)

        self.pushButtonDownload = QPushButton(SelectImageDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")
        self.pushButtonDownload.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(SelectImageDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.retranslateUi(SelectImageDialog)
        self.buttonBox.accepted.connect(SelectImageDialog.accept)
        self.buttonBox.rejected.connect(SelectImageDialog.reject)

        QMetaObject.connectSlotsByName(SelectImageDialog)
    # setupUi

    def retranslateUi(self, SelectImageDialog):
        SelectImageDialog.setWindowTitle(QCoreApplication.translate("SelectImageDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("SelectImageDialog", u"Image preview (200x200)", None))
        self.labelImage.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("SelectImageDialog", u"Image size", None))
        self.label_4.setText(QCoreApplication.translate("SelectImageDialog", u"Width", None))
        self.label_5.setText(QCoreApplication.translate("SelectImageDialog", u"Height", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SelectImageDialog", u"File format", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SelectImageDialog", u"Pixmap size (Kb)", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("SelectImageDialog", u"Load...", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("SelectImageDialog", u"Save...", None))
    # retranslateUi

