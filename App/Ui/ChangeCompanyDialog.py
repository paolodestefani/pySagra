# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChangeCompanyDialog.ui'
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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from App.Widget.Control import RelationalComboBox
import resources_rc

class Ui_ChangeCompanyDialog(object):
    def setupUi(self, ChangeCompanyDialog):
        if not ChangeCompanyDialog.objectName():
            ChangeCompanyDialog.setObjectName(u"ChangeCompanyDialog")
        ChangeCompanyDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        ChangeCompanyDialog.resize(512, 256)
        ChangeCompanyDialog.setLocale(QLocale(QLocale.C, QLocale.AnyTerritory))
        ChangeCompanyDialog.setSizeGripEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(ChangeCompanyDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.labelIcon = QLabel(ChangeCompanyDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_3.addWidget(self.labelIcon)

        self.verticalSpacer = QSpacerItem(17, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxInformation = QGroupBox(ChangeCompanyDialog)
        self.groupBoxInformation.setObjectName(u"groupBoxInformation")
        self.verticalLayout = QVBoxLayout(self.groupBoxInformation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelMessage = QLabel(self.groupBoxInformation)
        self.labelMessage.setObjectName(u"labelMessage")

        self.verticalLayout.addWidget(self.labelMessage)


        self.verticalLayout_2.addWidget(self.groupBoxInformation)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(ChangeCompanyDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label = QLabel(ChangeCompanyDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(ChangeCompanyDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditUser = QLineEdit(ChangeCompanyDialog)
        self.lineEditUser.setObjectName(u"lineEditUser")
        font = QFont()
        font.setBold(True)
        self.lineEditUser.setFont(font)
        self.lineEditUser.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEditUser.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)

        self.lineEditCompany = QLineEdit(ChangeCompanyDialog)
        self.lineEditCompany.setObjectName(u"lineEditCompany")
        self.lineEditCompany.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEditCompany.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditCompany, 1, 1, 1, 1)

        self.comboBoxCompanies = RelationalComboBox(ChangeCompanyDialog)
        self.comboBoxCompanies.setObjectName(u"comboBoxCompanies")
        self.comboBoxCompanies.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.comboBoxCompanies.setMaxVisibleItems(100)
        self.comboBoxCompanies.setIconSize(QSize(0, 0))
        self.comboBoxCompanies.setModelColumn(0)

        self.gridLayout.addWidget(self.comboBoxCompanies, 2, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(ChangeCompanyDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.retranslateUi(ChangeCompanyDialog)
        self.buttonBox.accepted.connect(ChangeCompanyDialog.accept)
        self.buttonBox.rejected.connect(ChangeCompanyDialog.reject)

        QMetaObject.connectSlotsByName(ChangeCompanyDialog)
    # setupUi

    def retranslateUi(self, ChangeCompanyDialog):
        ChangeCompanyDialog.setWindowTitle(QCoreApplication.translate("ChangeCompanyDialog", u"Choose the working company", None))
        self.labelIcon.setText(QCoreApplication.translate("ChangeCompanyDialog", u"icon", None))
        self.groupBoxInformation.setTitle(QCoreApplication.translate("ChangeCompanyDialog", u"Information", None))
        self.labelMessage.setText(QCoreApplication.translate("ChangeCompanyDialog", u"Message", None))
        self.label_3.setText(QCoreApplication.translate("ChangeCompanyDialog", u"Select company", None))
        self.label.setText(QCoreApplication.translate("ChangeCompanyDialog", u"User", None))
        self.label_2.setText(QCoreApplication.translate("ChangeCompanyDialog", u"Company", None))
#if QT_CONFIG(whatsthis)
        self.lineEditUser.setWhatsThis(QCoreApplication.translate("ChangeCompanyDialog", u"Shows the currently logged user", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.lineEditCompany.setWhatsThis(QCoreApplication.translate("ChangeCompanyDialog", u"Shows the current working company", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEditCompany.setText("")
#if QT_CONFIG(whatsthis)
        self.comboBoxCompanies.setWhatsThis(QCoreApplication.translate("ChangeCompanyDialog", u"Select the new working company from this list", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

