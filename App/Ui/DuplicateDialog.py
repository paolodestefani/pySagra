# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DuplicateDialog.ui'
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
    QGroupBox, QHBoxLayout, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DuplicateDialog(object):
    def setupUi(self, DuplicateDialog):
        if not DuplicateDialog.objectName():
            DuplicateDialog.setObjectName(u"DuplicateDialog")
        DuplicateDialog.resize(537, 144)
        self.verticalLayout = QVBoxLayout(DuplicateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(DuplicateDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditCode = QLineEdit(self.groupBox)
        self.lineEditCode.setObjectName(u"lineEditCode")

        self.horizontalLayout.addWidget(self.lineEditCode)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(DuplicateDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditDescription = QLineEdit(self.groupBox_2)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.horizontalLayout_2.addWidget(self.lineEditDescription)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(DuplicateDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DuplicateDialog)
        self.buttonBox.accepted.connect(DuplicateDialog.accept)
        self.buttonBox.rejected.connect(DuplicateDialog.reject)

        QMetaObject.connectSlotsByName(DuplicateDialog)
    # setupUi

    def retranslateUi(self, DuplicateDialog):
        DuplicateDialog.setWindowTitle(QCoreApplication.translate("DuplicateDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("DuplicateDialog", u"New code", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DuplicateDialog", u"New dscription", None))
    # retranslateUi

