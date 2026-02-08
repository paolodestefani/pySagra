# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UpdateWebOrderServerDialog.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from App.Widget.Control import RelationalComboBox

class Ui_UpdateWebOrderServerDialog(object):
    def setupUi(self, UpdateWebOrderServerDialog):
        if not UpdateWebOrderServerDialog.objectName():
            UpdateWebOrderServerDialog.setObjectName(u"UpdateWebOrderServerDialog")
        UpdateWebOrderServerDialog.resize(512, 480)
        self.verticalLayout_8 = QVBoxLayout(UpdateWebOrderServerDialog)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(UpdateWebOrderServerDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox = QGroupBox(UpdateWebOrderServerDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.comboBoxEvent = RelationalComboBox(self.groupBox)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout_4.addWidget(self.comboBoxEvent)


        self.verticalLayout_7.addWidget(self.groupBox)

        self.groupBox_7 = QGroupBox(UpdateWebOrderServerDialog)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditServer = QLineEdit(self.groupBox_7)
        self.lineEditServer.setObjectName(u"lineEditServer")

        self.horizontalLayout_3.addWidget(self.lineEditServer)

        self.spinBoxPort = QSpinBox(self.groupBox_7)
        self.spinBoxPort.setObjectName(u"spinBoxPort")
        self.spinBoxPort.setMinimum(1)
        self.spinBoxPort.setMaximum(65536)
        self.spinBoxPort.setValue(21)

        self.horizontalLayout_3.addWidget(self.spinBoxPort)

        self.lineEditEncoding = QLineEdit(self.groupBox_7)
        self.lineEditEncoding.setObjectName(u"lineEditEncoding")

        self.horizontalLayout_3.addWidget(self.lineEditEncoding)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_7.addWidget(self.groupBox_7)

        self.groupBox_11 = QGroupBox(UpdateWebOrderServerDialog)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout = QVBoxLayout(self.groupBox_11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEditFileName = QLineEdit(self.groupBox_11)
        self.lineEditFileName.setObjectName(u"lineEditFileName")

        self.verticalLayout.addWidget(self.lineEditFileName)


        self.verticalLayout_7.addWidget(self.groupBox_11)

        self.groupBox_8 = QGroupBox(UpdateWebOrderServerDialog)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineEditUser = QLineEdit(self.groupBox_8)
        self.lineEditUser.setObjectName(u"lineEditUser")

        self.verticalLayout_5.addWidget(self.lineEditUser)


        self.verticalLayout_7.addWidget(self.groupBox_8)

        self.groupBox_2 = QGroupBox(UpdateWebOrderServerDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lineEditPassword = QLineEdit(self.groupBox_2)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_6.addWidget(self.lineEditPassword)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(UpdateWebOrderServerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_8.addWidget(self.buttonBox)


        self.retranslateUi(UpdateWebOrderServerDialog)
        self.buttonBox.accepted.connect(UpdateWebOrderServerDialog.accept)
        self.buttonBox.rejected.connect(UpdateWebOrderServerDialog.reject)

        QMetaObject.connectSlotsByName(UpdateWebOrderServerDialog)
    # setupUi

    def retranslateUi(self, UpdateWebOrderServerDialog):
        UpdateWebOrderServerDialog.setWindowTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"Update web order server dialog", None))
        self.labelIcon.setText(QCoreApplication.translate("UpdateWebOrderServerDialog", u"Icon", None))
        self.groupBox.setTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"Event", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"Server, port and encoding", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"File name", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"User", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("UpdateWebOrderServerDialog", u"Password", None))
    # retranslateUi

