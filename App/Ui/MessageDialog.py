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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLayout, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MessageDialog(object):
    def setupUi(self, MessageDialog):
        if not MessageDialog.objectName():
            MessageDialog.setObjectName(u"MessageDialog")
        MessageDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        MessageDialog.setSizeGripEnabled(False)
        self.verticalLayout_5 = QVBoxLayout(MessageDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_5.setContentsMargins(12, 12, 12, 12)
        self.verticalLayoutMain = QVBoxLayout()
        self.verticalLayoutMain.setObjectName(u"verticalLayoutMain")
        self.verticalLayoutMain.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayoutMain.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(MessageDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(20, -1, -1, -1)
        self.labelErrorCode = QLabel(MessageDialog)
        self.labelErrorCode.setObjectName(u"labelErrorCode")
        self.labelErrorCode.setMinimumSize(QSize(300, 30))
        self.labelErrorCode.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_3.addWidget(self.labelErrorCode)

        self.labelMessage = QLabel(MessageDialog)
        self.labelMessage.setObjectName(u"labelMessage")
        self.labelMessage.setMinimumSize(QSize(0, 100))
        self.labelMessage.setMaximumSize(QSize(16777215, 100))
        self.labelMessage.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.labelMessage)

        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayoutMain.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(MessageDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Abort|QDialogButtonBox.StandardButton.Ignore)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayoutMain.addWidget(self.buttonBox)

        self.checkBoxShowDetailMessage = QCheckBox(MessageDialog)
        self.checkBoxShowDetailMessage.setObjectName(u"checkBoxShowDetailMessage")
        self.checkBoxShowDetailMessage.setChecked(False)

        self.verticalLayoutMain.addWidget(self.checkBoxShowDetailMessage)

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
        self.textEditDetailMessage.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.textEditDetailMessage)


        self.verticalLayoutMain.addWidget(self.frameDetails)


        self.verticalLayout_5.addLayout(self.verticalLayoutMain)


        self.retranslateUi(MessageDialog)
        self.buttonBox.accepted.connect(MessageDialog.accept)
        self.buttonBox.rejected.connect(MessageDialog.reject)
        self.checkBoxShowDetailMessage.clicked["bool"].connect(self.frameDetails.setVisible)

        QMetaObject.connectSlotsByName(MessageDialog)
    # setupUi

    def retranslateUi(self, MessageDialog):
        MessageDialog.setWindowTitle(QCoreApplication.translate("MessageDialog", u"Dialog", None))
        self.labelIcon.setText(QCoreApplication.translate("MessageDialog", u"icon", None))
        self.labelErrorCode.setText(QCoreApplication.translate("MessageDialog", u"Error code", None))
        self.labelMessage.setText(QCoreApplication.translate("MessageDialog", u"Message", None))
        self.checkBoxShowDetailMessage.setText(QCoreApplication.translate("MessageDialog", u"Show detail message", None))
    # retranslateUi

