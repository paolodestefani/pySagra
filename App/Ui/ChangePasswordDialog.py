# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChangePasswordDialog.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_ChangePasswordDialog(object):
    def setupUi(self, ChangePasswordDialog):
        if not ChangePasswordDialog.objectName():
            ChangePasswordDialog.setObjectName(u"ChangePasswordDialog")
        ChangePasswordDialog.setWindowModality(Qt.ApplicationModal)
        ChangePasswordDialog.resize(500, 140)
        ChangePasswordDialog.setLocale(QLocale(QLocale.C, QLocale.AnyCountry))
        ChangePasswordDialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(ChangePasswordDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelIcon = QLabel(ChangePasswordDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.horizontalLayout.addWidget(self.labelIcon)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(ChangePasswordDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditUser = QLineEdit(ChangePasswordDialog)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setEnabled(True)
        font = QFont()
        font.setBold(True)
        self.lineEditUser.setFont(font)
        self.lineEditUser.setFocusPolicy(Qt.NoFocus)
        self.lineEditUser.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)

        self.label_2 = QLabel(ChangePasswordDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditNewPassword = QLineEdit(ChangePasswordDialog)
        self.lineEditNewPassword.setObjectName(u"lineEditNewPassword")
        self.lineEditNewPassword.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEditNewPassword, 1, 1, 1, 1)

        self.label_3 = QLabel(ChangePasswordDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEditConfirmPassword = QLineEdit(ChangePasswordDialog)
        self.lineEditConfirmPassword.setObjectName(u"lineEditConfirmPassword")
        self.lineEditConfirmPassword.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEditConfirmPassword, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 9, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ChangePasswordDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ChangePasswordDialog)
        self.buttonBox.accepted.connect(ChangePasswordDialog.accept)
        self.buttonBox.rejected.connect(ChangePasswordDialog.reject)

        QMetaObject.connectSlotsByName(ChangePasswordDialog)
    # setupUi

    def retranslateUi(self, ChangePasswordDialog):
        ChangePasswordDialog.setWindowTitle(QCoreApplication.translate("ChangePasswordDialog", u"Change password", None))
        self.labelIcon.setText(QCoreApplication.translate("ChangePasswordDialog", u"icon", None))
        self.label.setText(QCoreApplication.translate("ChangePasswordDialog", u"User", None))
#if QT_CONFIG(whatsthis)
        self.lineEditUser.setWhatsThis(QCoreApplication.translate("ChangePasswordDialog", u"Shows the user who require the password change", None))
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("ChangePasswordDialog", u"New password", None))
#if QT_CONFIG(whatsthis)
        self.lineEditNewPassword.setWhatsThis(QCoreApplication.translate("ChangePasswordDialog", u"Type in the new password", None))
#endif // QT_CONFIG(whatsthis)
        self.label_3.setText(QCoreApplication.translate("ChangePasswordDialog", u"Confirm password", None))
#if QT_CONFIG(whatsthis)
        self.lineEditConfirmPassword.setWhatsThis(QCoreApplication.translate("ChangePasswordDialog", u"Retype the password, must match the previous typed password", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

