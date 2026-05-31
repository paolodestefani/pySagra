# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MessageDialog.ui'
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
    QFrame, QHBoxLayout, QLabel, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MessageDialog(object):
    def setupUi(self, MessageDialog):
        if not MessageDialog.objectName():
            MessageDialog.setObjectName(u"MessageDialog")
        MessageDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        MessageDialog.resize(510, 378)
        MessageDialog.setSizeGripEnabled(False)
        self.verticalLayout_2 = QVBoxLayout(MessageDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelIcon = QLabel(MessageDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.horizontalLayout.addWidget(self.labelIcon)

        self.labelErrorCode = QLabel(MessageDialog)
        self.labelErrorCode.setObjectName(u"labelErrorCode")
        self.labelErrorCode.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.labelErrorCode)

        self.labelMessage = QLabel(MessageDialog)
        self.labelMessage.setObjectName(u"labelMessage")
        font = QFont()
        font.setBold(True)
        self.labelMessage.setFont(font)
        self.labelMessage.setTextFormat(Qt.TextFormat.MarkdownText)
        self.labelMessage.setWordWrap(True)

        self.horizontalLayout.addWidget(self.labelMessage)

        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.frameDetails = QFrame(MessageDialog)
        self.frameDetails.setObjectName(u"frameDetails")
        self.frameDetails.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameDetails.setFrameShadow(QFrame.Shadow.Raised)
        self.frameDetails.setLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.frameDetails)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEditDetailMessage = QTextEdit(self.frameDetails)
        self.textEditDetailMessage.setObjectName(u"textEditDetailMessage")
        self.textEditDetailMessage.setMinimumSize(QSize(300, 200))
        self.textEditDetailMessage.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.textEditDetailMessage.setReadOnly(True)
        self.textEditDetailMessage.setAcceptRichText(False)
        self.textEditDetailMessage.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.textEditDetailMessage)


        self.verticalLayout_2.addWidget(self.frameDetails)

        self.buttonBox = QDialogButtonBox(MessageDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Abort|QDialogButtonBox.StandardButton.Ignore)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(MessageDialog)
        self.buttonBox.accepted.connect(MessageDialog.accept)
        self.buttonBox.rejected.connect(MessageDialog.reject)

        QMetaObject.connectSlotsByName(MessageDialog)
    # setupUi

    def retranslateUi(self, MessageDialog):
        MessageDialog.setWindowTitle(QCoreApplication.translate("MessageDialog", u"Dialog", None))
        self.labelIcon.setText(QCoreApplication.translate("MessageDialog", u"icon", None))
        self.labelErrorCode.setText(QCoreApplication.translate("MessageDialog", u"Error code", None))
        self.labelMessage.setText(QCoreApplication.translate("MessageDialog", u"Message", None))
        self.textEditDetailMessage.setHtml(QCoreApplication.translate("MessageDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

