# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

from App.Widget.Control import PasswordLineEdit
import resources_rc

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(335, 552)
        LoginDialog.setSizeGripEnabled(True)
        LoginDialog.setModal(False)
        self.verticalLayoutDialog = QVBoxLayout(LoginDialog)
        self.verticalLayoutDialog.setObjectName(u"verticalLayoutDialog")
        self.verticalLayoutDialog.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayoutDialog.setContentsMargins(12, 12, 12, 12)
        self.verticalLayoutInsideDialog = QVBoxLayout()
        self.verticalLayoutInsideDialog.setObjectName(u"verticalLayoutInsideDialog")
        self.verticalLayoutInsideDialog.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
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

        self.verticalLayoutInsideDialog.addWidget(self.labelMain)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditPassword = PasswordLineEdit(LoginDialog)
        self.lineEditPassword.setObjectName(u"lineEditPassword")

        self.gridLayout.addWidget(self.lineEditPassword, 1, 1, 1, 1)

        self.labelUser = QLabel(LoginDialog)
        self.labelUser.setObjectName(u"labelUser")
        self.labelUser.setLineWidth(0)

        self.gridLayout.addWidget(self.labelUser, 0, 0, 1, 1)

        self.lineEditUser = QLineEdit(LoginDialog)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setStyleSheet(u"")
        self.lineEditUser.setMaxLength(48)

        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)

        self.labelPassword = QLabel(LoginDialog)
        self.labelPassword.setObjectName(u"labelPassword")

        self.gridLayout.addWidget(self.labelPassword, 1, 0, 1, 1)


        self.verticalLayoutInsideDialog.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(LoginDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayoutInsideDialog.addWidget(self.buttonBox)

        self.checkBoxMore = QCheckBox(LoginDialog)
        self.checkBoxMore.setObjectName(u"checkBoxMore")

        self.verticalLayoutInsideDialog.addWidget(self.checkBoxMore)

        self.frameMore = QFrame(LoginDialog)
        self.frameMore.setObjectName(u"frameMore")
        self.frameMore.setFrameShape(QFrame.Shape.NoFrame)
        self.frameMore.setFrameShadow(QFrame.Shadow.Plain)
        self.frameMore.setLineWidth(0)
        self.verticalLayoutFrameMore = QVBoxLayout(self.frameMore)
        self.verticalLayoutFrameMore.setObjectName(u"verticalLayoutFrameMore")
        self.verticalLayoutFrameMore.setContentsMargins(6, 6, 6, 6)
        self.gridLayoutFrameMore = QGridLayout()
        self.gridLayoutFrameMore.setObjectName(u"gridLayoutFrameMore")
        self.spinBoxPort = QSpinBox(self.frameMore)
        self.spinBoxPort.setObjectName(u"spinBoxPort")
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setValue(5432)
        self.spinBoxPort.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayoutFrameMore.addWidget(self.spinBoxPort, 3, 1, 1, 1)

        self.labelDatabase = QLabel(self.frameMore)
        self.labelDatabase.setObjectName(u"labelDatabase")

        self.gridLayoutFrameMore.addWidget(self.labelDatabase, 4, 0, 1, 1)

        self.lineEditDatabase = QLineEdit(self.frameMore)
        self.lineEditDatabase.setObjectName(u"lineEditDatabase")
        self.lineEditDatabase.setMaxLength(64)
        self.lineEditDatabase.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayoutFrameMore.addWidget(self.lineEditDatabase, 4, 1, 1, 1)

        self.lineEditServer = QLineEdit(self.frameMore)
        self.lineEditServer.setObjectName(u"lineEditServer")
        self.lineEditServer.setMaxLength(64)
        self.lineEditServer.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayoutFrameMore.addWidget(self.lineEditServer, 2, 1, 1, 1)

        self.lineEditDBUser = QLineEdit(self.frameMore)
        self.lineEditDBUser.setObjectName(u"lineEditDBUser")
        self.lineEditDBUser.setMaxLength(48)
        self.lineEditDBUser.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.gridLayoutFrameMore.addWidget(self.lineEditDBUser, 5, 1, 1, 1)

        self.labelDbUser = QLabel(self.frameMore)
        self.labelDbUser.setObjectName(u"labelDbUser")

        self.gridLayoutFrameMore.addWidget(self.labelDbUser, 5, 0, 1, 1)

        self.lineEditDBPassword = QLineEdit(self.frameMore)
        self.lineEditDBPassword.setObjectName(u"lineEditDBPassword")
        self.lineEditDBPassword.setMaxLength(255)
        self.lineEditDBPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditDBPassword.setProperty(u"mandatoryFieldFlag", True)

        self.gridLayoutFrameMore.addWidget(self.lineEditDBPassword, 6, 1, 1, 1)

        self.labelDbPassword = QLabel(self.frameMore)
        self.labelDbPassword.setObjectName(u"labelDbPassword")

        self.gridLayoutFrameMore.addWidget(self.labelDbPassword, 6, 0, 1, 1)

        self.labelServer = QLabel(self.frameMore)
        self.labelServer.setObjectName(u"labelServer")

        self.gridLayoutFrameMore.addWidget(self.labelServer, 2, 0, 1, 1)

        self.labelPort = QLabel(self.frameMore)
        self.labelPort.setObjectName(u"labelPort")

        self.gridLayoutFrameMore.addWidget(self.labelPort, 3, 0, 1, 1)


        self.verticalLayoutFrameMore.addLayout(self.gridLayoutFrameMore)

        self.labelVersion = QLabel(self.frameMore)
        self.labelVersion.setObjectName(u"labelVersion")
        self.labelVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayoutFrameMore.addWidget(self.labelVersion)

        self.pushButtonClearSettings = QPushButton(self.frameMore)
        self.pushButtonClearSettings.setObjectName(u"pushButtonClearSettings")

        self.verticalLayoutFrameMore.addWidget(self.pushButtonClearSettings)


        self.verticalLayoutInsideDialog.addWidget(self.frameMore)


        self.verticalLayoutDialog.addLayout(self.verticalLayoutInsideDialog)

#if QT_CONFIG(shortcut)
        self.labelUser.setBuddy(self.lineEditUser)
        self.labelPassword.setBuddy(self.lineEditPassword)
        self.labelDatabase.setBuddy(self.lineEditDatabase)
        self.labelDbUser.setBuddy(self.lineEditDBUser)
        self.labelDbPassword.setBuddy(self.lineEditDBPassword)
        self.labelServer.setBuddy(self.lineEditServer)
        self.labelPort.setBuddy(self.spinBoxPort)
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
        self.labelUser.setText(QCoreApplication.translate("LoginDialog", u"User", None))
#if QT_CONFIG(tooltip)
        self.lineEditUser.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the application user name", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEditUser.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.lineEditUser.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the application user name", None))
#endif // QT_CONFIG(whatsthis)
        self.labelPassword.setText(QCoreApplication.translate("LoginDialog", u"Password", None))
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
        self.labelDatabase.setText(QCoreApplication.translate("LoginDialog", u"Database", None))
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
        self.labelDbUser.setText(QCoreApplication.translate("LoginDialog", u"DB User", None))
#if QT_CONFIG(tooltip)
        self.lineEditDBPassword.setToolTip(QCoreApplication.translate("LoginDialog", u"Insert the database user password", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEditDBPassword.setWhatsThis(QCoreApplication.translate("LoginDialog", u"Insert the database user password", None))
#endif // QT_CONFIG(whatsthis)
        self.labelDbPassword.setText(QCoreApplication.translate("LoginDialog", u"DB Password", None))
        self.labelServer.setText(QCoreApplication.translate("LoginDialog", u"Server", None))
        self.labelPort.setText(QCoreApplication.translate("LoginDialog", u"Port", None))
        self.labelVersion.setText(QCoreApplication.translate("LoginDialog", u"Current App Version", None))
        self.pushButtonClearSettings.setText(QCoreApplication.translate("LoginDialog", u"Clear local stored settings", None))
    # retranslateUi

