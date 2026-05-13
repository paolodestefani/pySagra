# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GoToDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_GoToDialog(object):
    def setupUi(self, GoToDialog):
        if not GoToDialog.objectName():
            GoToDialog.setObjectName(u"GoToDialog")
        GoToDialog.resize(371, 129)
        GoToDialog.setModal(True)
        self.verticalLayout_3 = QVBoxLayout(GoToDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GoToDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBoxActions = QComboBox(self.groupBox)
        self.comboBoxActions.setObjectName(u"comboBoxActions")
        self.comboBoxActions.setEditable(True)
        self.comboBoxActions.setMaxVisibleItems(15)

        self.verticalLayout.addWidget(self.comboBoxActions)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(GoToDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(GoToDialog)
        self.buttonBox.accepted.connect(GoToDialog.accept)
        self.buttonBox.rejected.connect(GoToDialog.reject)

        QMetaObject.connectSlotsByName(GoToDialog)
    # setupUi

    def retranslateUi(self, GoToDialog):
        GoToDialog.setWindowTitle(QCoreApplication.translate("GoToDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("GoToDialog", u"Actions", None))
    # retranslateUi

