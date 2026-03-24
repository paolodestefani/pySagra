# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DepartmentNoteDialog.ui'
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
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_DepartmentNoteDialog(object):
    def setupUi(self, DepartmentNoteDialog):
        if not DepartmentNoteDialog.objectName():
            DepartmentNoteDialog.setObjectName(u"DepartmentNoteDialog")
        DepartmentNoteDialog.resize(500, 100)
        self.verticalLayout_2 = QVBoxLayout(DepartmentNoteDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_department = QLabel(DepartmentNoteDialog)
        self.lb_department.setObjectName(u"lb_department")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.lb_department.setFont(font)

        self.verticalLayout.addWidget(self.lb_department)

        self.le_note = QLineEdit(DepartmentNoteDialog)
        self.le_note.setObjectName(u"le_note")

        self.verticalLayout.addWidget(self.le_note)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(DepartmentNoteDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(DepartmentNoteDialog)
        self.buttonBox.accepted.connect(DepartmentNoteDialog.accept)
        self.buttonBox.rejected.connect(DepartmentNoteDialog.reject)

        QMetaObject.connectSlotsByName(DepartmentNoteDialog)
    # setupUi

    def retranslateUi(self, DepartmentNoteDialog):
        DepartmentNoteDialog.setWindowTitle(QCoreApplication.translate("DepartmentNoteDialog", u"Gestione note per reparto", None))
        self.lb_department.setText(QCoreApplication.translate("DepartmentNoteDialog", u"Reparto:", None))
    # retranslateUi

