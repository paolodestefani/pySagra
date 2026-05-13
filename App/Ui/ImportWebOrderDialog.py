# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImportWebOrderDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ImporWebOrderDialog(object):
    def setupUi(self, ImporWebOrderDialog):
        if not ImporWebOrderDialog.objectName():
            ImporWebOrderDialog.setObjectName(u"ImporWebOrderDialog")
        ImporWebOrderDialog.resize(368, 153)
        self.verticalLayout_3 = QVBoxLayout(ImporWebOrderDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(ImporWebOrderDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEditBarCode = QLineEdit(self.groupBox)
        self.lineEditBarCode.setObjectName(u"lineEditBarCode")

        self.verticalLayout.addWidget(self.lineEditBarCode)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.labelMessage = QLabel(ImporWebOrderDialog)
        self.labelMessage.setObjectName(u"labelMessage")
        font = QFont()
        font.setBold(True)
        self.labelMessage.setFont(font)
        self.labelMessage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.labelMessage)

        self.verticalSpacer = QSpacerItem(344, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ImporWebOrderDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(ImporWebOrderDialog)
        self.buttonBox.accepted.connect(ImporWebOrderDialog.accept)
        self.buttonBox.rejected.connect(ImporWebOrderDialog.reject)

        QMetaObject.connectSlotsByName(ImporWebOrderDialog)
    # setupUi

    def retranslateUi(self, ImporWebOrderDialog):
        ImporWebOrderDialog.setWindowTitle(QCoreApplication.translate("ImporWebOrderDialog", u"Import Web Order", None))
        self.groupBox.setTitle(QCoreApplication.translate("ImporWebOrderDialog", u"Bar code search", None))
        self.labelMessage.setText("")
    # retranslateUi

