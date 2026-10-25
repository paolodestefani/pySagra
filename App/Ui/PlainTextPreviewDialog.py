# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlainTextPreviewDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_PlainTextPreviewDialog(object):
    def setupUi(self, PlainTextPreviewDialog):
        if not PlainTextPreviewDialog.objectName():
            PlainTextPreviewDialog.setObjectName(u"PlainTextPreviewDialog")
        PlainTextPreviewDialog.resize(603, 403)
        self.verticalLayout = QVBoxLayout(PlainTextPreviewDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plainTextEdit = QPlainTextEdit(PlainTextPreviewDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        font = QFont()
        font.setFamilies([u"Menlo"])
        self.plainTextEdit.setFont(font)

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.buttonBox = QDialogButtonBox(PlainTextPreviewDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PlainTextPreviewDialog)
        self.buttonBox.accepted.connect(PlainTextPreviewDialog.accept)
        self.buttonBox.rejected.connect(PlainTextPreviewDialog.reject)

        QMetaObject.connectSlotsByName(PlainTextPreviewDialog)
    # setupUi

    def retranslateUi(self, PlainTextPreviewDialog):
        PlainTextPreviewDialog.setWindowTitle(QCoreApplication.translate("PlainTextPreviewDialog", u"Dialog", None))
    # retranslateUi

