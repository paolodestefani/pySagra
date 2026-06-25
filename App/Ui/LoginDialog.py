# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginDialog.ui'
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
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLayout, QLineEdit, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

from App.Widget.Control import PasswordLineEdit
import resources_rc

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(335, 552)
        LoginDialog.setSizeGripEnabled(True)
        LoginDialog.setModal(False)
        self.verticalLayout_3 = QVBoxLayout(LoginDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.labelMain = QLabel(LoginDialog)
        self.labelMain.setObjectName(u"labelMain")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMain.sizePolicy().hasHeightForWidth())
        self.labelMain.setSizePolicy(sizePolicy)
        self.labelMain.setMinimumSize(QSize(300, 0))
        palette = QPalette()
        brush = QBrush(QColor(192, 192, 192, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(48, 47, 47, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(61, 142, 201, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, brush2)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, brush3)
        brush4 = QBrush(QColor(192, 192, 192, 128))
        brush4.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush4)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, brush3)
        brush5 = QBrush(QColor(192, 192, 192, 128))
        brush5.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush5)
#endif
        brush6 = QBrush(QColor(64, 64, 64, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, brush3)
        brush7 = QBrush(QColor(192, 192, 192, 128))
        brush7.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush7)
#endif
        self.labelMain.setPalette(palette)
        self.labelMain.setAutoFillBackground(False)
        self.labelMain.setLocale(QLocale(QLocale.C, QLocale.AnyTerritory))
        self.labelMain.setFrameShape(QFrame.Shape.NoFrame)
        self.labelMain.setFrameShadow(QFrame.Shadow.Plain)
        self.labelMain.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.labelMain)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditPassword = PasswordLineEdit(LoginDialog)
        self.lineEditPassword.setObjectName(u"lineEditPassword")

        self.gridLayout.addWidget(self.lineEditPassword, 1, 1, 1, 1)

        self.label_5 = QLabel(LoginDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setLineWidth(0)

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.lineEditUser = QLineEdit(LoginDialog)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setStyleSheet(u"")
        self.lineEditUser.setMaxLength(48)

        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)

        self.label_6 = QLabel(LoginDialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(LoginDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.checkBoxMore = QCheckBox(LoginDialog)
        self.checkBoxMore.setObjectName(u"checkBoxMore")

        self.verticalLayout_2.addWidget(self.checkBoxMore)

        self.frameMore = QFrame(LoginDialog)
        self.frameMore.setObjectName(u"frameMore")
        self.frameMore.setFrameShape(QFrame.Shape.NoFrame)
        self.frameMore.setFrameShadow(QFrame.Shadow.Plain)
        self.frameMore.setLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.frameMore)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spinBoxPort = QSpinBox(self.frameMore)
        self.spinBoxPort.setObjectName(u"spinBoxPort")
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setValue(5432)
        self.spinBoxPort.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayout_2.addWidget(self.spinBoxPort, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frameMore)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)

        self.lineEditDatabase = QLineEdit(self.frameMore)
        self.lineEditDatabase.setObjectName(u"lineEditDatabase")
        self.lineEditDatabase.setMaxLength(64)
        self.lineEditDatabase.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayout_2.addWidget(self.lineEditDatabase, 4, 1, 1, 1)

        self.lineEditServer = QLineEdit(self.frameMore)
        self.lineEditServer.setObjectName(u"lineEditServer")
        self.lineEditServer.setMaxLength(64)
        self.lineEditServer.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayout_2.addWidget(self.lineEditServer, 2, 1, 1, 1)

        self.lineEditDBUser = QLineEdit(self.frameMore)
        self.lineEditDBUser.setObjectName(u"lineEditDBUser")
        self.lineEditDBUser.setMaxLength(48)
        self.lineEditDBUser.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.gridLayout_2.addWidget(self.lineEditDBUser, 5, 1, 1, 1)

        self.label_8 = QLabel(self.frameMore)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)

        self.lineEditDBPassword = QLineEdit(self.frameMore)
        self.lineEditDBPassword.setObjectName(u"lineEditDBPassword")
        self.lineEditDBPassword.setMaxLength(255)
        self.lineEditDBPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditDBPassword.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayout_2.addWidget(self.lineEditDBPassword, 6, 1, 1, 1)

        self.label_9 = QLabel(self.frameMore)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 6, 0, 1, 1)

        self.label_2 = QLabel(self.frameMore)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_3 = QLabel(self.frameMore)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.labelVersion = QLabel(self.frameMore)
        self.labelVersion.setObjectName(u"labelVersion")
        self.labelVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelVersion)


        self.verticalLayout_2.addWidget(self.frameMore)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

#if QT_CONFIG(shortcut)
        self.label_5.setBuddy(self.lineEditUser)
        self.label_6.setBuddy(self.lineEditPassword)
        self.label_4.setBuddy(self.lineEditDatabase)
        self.label_8.setBuddy(self.lineEditDBUser)
        self.label_9.setBuddy(self.lineEditDBPassword)
        self.label_2.setBuddy(self.lineEditServer)
        self.label_3.setBuddy(self.spinBoxPort)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEditUser, self.lineEditPassword)
        QWidget.setTabOrder(self.lineEditPassword, self.checkBoxMore)
        QWidget.setTabOrder(self.checkBoxMore, self.lineEditServer)
        QWidget.setTabOrder(self.lineEditServer, self.spinBoxPort)
        QWidget.setTabOrder(self.spinBoxPort, self.lineEditDatabase)
        QWidget.setTabOrder(self.lineEditDatabase, self.lineEditDBUser)
        QWidget.setTabOrder(self.lineEditDBUser, self.lineEditDBPassword)

        self.retranslateUi(LoginDialog)
        self.checkBoxMore.clicked["bool"].connect(self.frameMore.setVisible)
        self.buttonBox.accepted.connect(LoginDialog.accept)
        self.buttonBox.rejected.connect(LoginDialog.reject)

        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"Login", None))
#if QT_CONFIG(tooltip)
        self.lineEditPassword.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the password for application user", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEditPassword.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.lineEditPassword.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the password for application user", None))
#endif // QT_CONFIG(whatsthis)
        self.label_5.setText(QCoreApplication.translate("LoginDialog", u"User", None))
#if QT_CONFIG(tooltip)
        self.lineEditUser.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the application user name", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEditUser.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.lineEditUser.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the application user name", None))
#endif // QT_CONFIG(whatsthis)
        self.label_6.setText(QCoreApplication.translate("LoginDialog", u"Password", None))
#if QT_CONFIG(tooltip)
        self.checkBoxMore.setToolTip(QCoreApplication.translate("LoginDialog", u"Show/hide the connection parameters", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.checkBoxMore.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Show/hide the connection parameters", None))
#endif // QT_CONFIG(whatsthis)
        self.checkBoxMore.setText(QCoreApplication.translate("LoginDialog", u"Connection details", None))
#if QT_CONFIG(tooltip)
        self.spinBoxPort.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the db server IP port", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.spinBoxPort.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the db server IP port", None))
#endif // QT_CONFIG(whatsthis)
        self.label_4.setText(QCoreApplication.translate("LoginDialog", u"Database", None))
#if QT_CONFIG(tooltip)
        self.lineEditDatabase.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the database name", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEditDatabase.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the database name", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(tooltip)
        self.lineEditServer.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the database server name or IP address", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEditServer.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the database server name or IP address", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(tooltip)
        self.lineEditDBUser.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the database user name", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEditDBUser.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the database user name", None))
#endif // QT_CONFIG(whatsthis)
        self.label_8.setText(QCoreApplication.translate("LoginDialog", u"DB User", None))
#if QT_CONFIG(tooltip)
        self.lineEditDBPassword.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the database user password", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEditDBPassword.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the database user password", None))
#endif // QT_CONFIG(whatsthis)
        self.label_9.setText(QCoreApplication.translate("LoginDialog", u"DB Password", None))
        self.label_2.setText(QCoreApplication.translate("LoginDialog", u"Server", None))
        self.label_3.setText(QCoreApplication.translate("LoginDialog", u"Port", None))
        self.labelVersion.setText(QCoreApplication.translate("LoginDialog", u"Current App Version", None))
    # retranslateUi

