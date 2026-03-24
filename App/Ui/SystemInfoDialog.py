# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SystemInfoDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_SystemInfoDialog(object):
    def setupUi(self, SystemInfoDialog):
        if not SystemInfoDialog.objectName():
            SystemInfoDialog.setObjectName(u"SystemInfoDialog")
        SystemInfoDialog.resize(640, 512)
        self.verticalLayout_3 = QVBoxLayout(SystemInfoDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(SystemInfoDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelCompany = QLabel(SystemInfoDialog)
        self.labelCompany.setObjectName(u"labelCompany")
        font = QFont()
        font.setBold(True)
        self.labelCompany.setFont(font)

        self.gridLayout.addWidget(self.labelCompany, 1, 0, 1, 1)

        self.lineEditProfile = QLineEdit(SystemInfoDialog)
        self.lineEditProfile.setObjectName(u"lineEditProfile")
        font1 = QFont()
        font1.setBold(False)
        self.lineEditProfile.setFont(font1)
        self.lineEditProfile.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditProfile, 2, 3, 1, 1)

        self.labelServer = QLabel(SystemInfoDialog)
        self.labelServer.setObjectName(u"labelServer")
        self.labelServer.setFont(font)

        self.gridLayout.addWidget(self.labelServer, 0, 0, 1, 1)

        self.labelUser = QLabel(SystemInfoDialog)
        self.labelUser.setObjectName(u"labelUser")
        self.labelUser.setFont(font)

        self.gridLayout.addWidget(self.labelUser, 2, 0, 1, 1)

        self.lineEditDatabase = QLineEdit(SystemInfoDialog)
        self.lineEditDatabase.setObjectName(u"lineEditDatabase")
        self.lineEditDatabase.setFont(font1)
        self.lineEditDatabase.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditDatabase, 0, 3, 1, 1)

        self.lineEditUser = QLineEdit(SystemInfoDialog)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setFont(font1)
        self.lineEditUser.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditUser, 2, 1, 1, 1)

        self.labelDatabase = QLabel(SystemInfoDialog)
        self.labelDatabase.setObjectName(u"labelDatabase")
        self.labelDatabase.setFont(font)

        self.gridLayout.addWidget(self.labelDatabase, 0, 2, 1, 1)

        self.labelProfile = QLabel(SystemInfoDialog)
        self.labelProfile.setObjectName(u"labelProfile")
        self.labelProfile.setFont(font)

        self.gridLayout.addWidget(self.labelProfile, 2, 2, 1, 1)

        self.lineEditServer = QLineEdit(SystemInfoDialog)
        self.lineEditServer.setObjectName(u"lineEditServer")
        self.lineEditServer.setFont(font1)
        self.lineEditServer.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditServer, 0, 1, 1, 1)

        self.lineEditCompany = QLineEdit(SystemInfoDialog)
        self.lineEditCompany.setObjectName(u"lineEditCompany")
        self.lineEditCompany.setFont(font1)
        self.lineEditCompany.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditCompany, 1, 1, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        self.textEditInfo = QTextEdit(SystemInfoDialog)
        self.textEditInfo.setObjectName(u"textEditInfo")
        self.textEditInfo.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEditInfo)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(SystemInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.retranslateUi(SystemInfoDialog)
        self.buttonBox.accepted.connect(SystemInfoDialog.accept)
        self.buttonBox.rejected.connect(SystemInfoDialog.reject)

        QMetaObject.connectSlotsByName(SystemInfoDialog)
    # setupUi

    def retranslateUi(self, SystemInfoDialog):
        SystemInfoDialog.setWindowTitle(QCoreApplication.translate("SystemInfoDialog", u"System Info", None))
        self.labelIcon.setText("")
        self.labelCompany.setText(QCoreApplication.translate("SystemInfoDialog", u"Company", None))
        self.labelServer.setText(QCoreApplication.translate("SystemInfoDialog", u"Server", None))
        self.labelUser.setText(QCoreApplication.translate("SystemInfoDialog", u"User", None))
        self.labelDatabase.setText(QCoreApplication.translate("SystemInfoDialog", u"Database", None))
        self.labelProfile.setText(QCoreApplication.translate("SystemInfoDialog", u"Profile", None))
        self.lineEditServer.setText("")
    # retranslateUi

