# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UserWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QVBoxLayout, QWidget)

from App.Widget.Control import (DateTimeEdit, LabelImage, RelationalComboBox)
from App.Widget.View import EnhancedTableView

class Ui_UserWidget(object):
    def setupUi(self, UserWidget):
        if not UserWidget.objectName():
            UserWidget.setObjectName(u"UserWidget")
        UserWidget.resize(1229, 545)
        self.verticalLayout_4 = QVBoxLayout(UserWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.stackedWidget = QStackedWidget(UserWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_13 = QVBoxLayout(self.page)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEditUser = QLineEdit(self.groupBox)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setEnabled(False)
        self.lineEditUser.setReadOnly(False)

        self.verticalLayout_3.addWidget(self.lineEditUser)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.page)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.lineEditUserDescription = QLineEdit(self.groupBox_5)
        self.lineEditUserDescription.setObjectName(u"lineEditUserDescription")
        self.lineEditUserDescription.setClearButtonEnabled(True)

        self.verticalLayout_10.addWidget(self.lineEditUserDescription)


        self.horizontalLayout.addWidget(self.groupBox_5)

        self.groupBox_2 = QGroupBox(self.page)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBoxL10n = RelationalComboBox(self.groupBox_2)
        self.comboBoxL10n.setObjectName(u"comboBoxL10n")
        self.comboBoxL10n.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.comboBoxL10n.setEditable(False)

        self.verticalLayout_5.addWidget(self.comboBoxL10n)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBoxSystem = QCheckBox(self.page)
        self.checkBoxSystem.setObjectName(u"checkBoxSystem")
        self.checkBoxSystem.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.checkBoxSystem)

        self.checkBoxIsAdmin = QCheckBox(self.page)
        self.checkBoxIsAdmin.setObjectName(u"checkBoxIsAdmin")
        self.checkBoxIsAdmin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_2.addWidget(self.checkBoxIsAdmin)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.checkBoxCanEditViews = QCheckBox(self.page)
        self.checkBoxCanEditViews.setObjectName(u"checkBoxCanEditViews")
        self.checkBoxCanEditViews.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_2.addWidget(self.checkBoxCanEditViews)

        self.checkBoxCanEditSortFilters = QCheckBox(self.page)
        self.checkBoxCanEditSortFilters.setObjectName(u"checkBoxCanEditSortFilters")
        self.checkBoxCanEditSortFilters.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_2.addWidget(self.checkBoxCanEditSortFilters)

        self.checkBoxCanEditReports = QCheckBox(self.page)
        self.checkBoxCanEditReports.setObjectName(u"checkBoxCanEditReports")
        self.checkBoxCanEditReports.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_2.addWidget(self.checkBoxCanEditReports)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        self.verticalLayout_11 = QVBoxLayout(self.tab1)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.tableViewUserCompany = EnhancedTableView(self.tab1)
        self.tableViewUserCompany.setObjectName(u"tableViewUserCompany")

        self.verticalLayout_11.addWidget(self.tableViewUserCompany)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonAdd = QPushButton(self.tab1)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_5.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.tab1)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_5.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_11.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab1, "")

        self.verticalLayout_7.addWidget(self.tabWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_7 = QGroupBox(self.page)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.labelImage = LabelImage(self.groupBox_7)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelImage.setProperty(u"hasImage", True)

        self.verticalLayout_8.addWidget(self.labelImage)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonUpload = QPushButton(self.groupBox_7)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout_3.addWidget(self.pushButtonUpload)

        self.pushButtonDownload = QPushButton(self.groupBox_7)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout_3.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButtonDelete = QPushButton(self.groupBox_7)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout_3.addWidget(self.pushButtonDelete)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)


        self.verticalLayout_12.addLayout(self.verticalLayout_8)


        self.verticalLayout_6.addWidget(self.groupBox_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.groupBox_3 = QGroupBox(self.page)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.lineEditLastCompany = QLineEdit(self.groupBox_3)
        self.lineEditLastCompany.setObjectName(u"lineEditLastCompany")
        self.lineEditLastCompany.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLastCompany.sizePolicy().hasHeightForWidth())
        self.lineEditLastCompany.setSizePolicy(sizePolicy)
        self.lineEditLastCompany.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEditLastCompany)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.dateTimeEditLastLogin = DateTimeEdit(self.groupBox_3)
        self.dateTimeEditLastLogin.setObjectName(u"dateTimeEditLastLogin")
        sizePolicy.setHeightForWidth(self.dateTimeEditLastLogin.sizePolicy().hasHeightForWidth())
        self.dateTimeEditLastLogin.setSizePolicy(sizePolicy)
        self.dateTimeEditLastLogin.setReadOnly(True)
        self.dateTimeEditLastLogin.setDateTime(QDateTime(QDate(1800, 1, 1), QTime(0, 0, 0)))
        self.dateTimeEditLastLogin.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.dateTimeEditLastLogin)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout.addWidget(self.label_12)

        self.dateTimeEditPasswordDate = DateTimeEdit(self.groupBox_3)
        self.dateTimeEditPasswordDate.setObjectName(u"dateTimeEditPasswordDate")
        self.dateTimeEditPasswordDate.setReadOnly(True)
        self.dateTimeEditPasswordDate.setDate(QDate(1800, 1, 1))
        self.dateTimeEditPasswordDate.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.dateTimeEditPasswordDate)

        self.checkBoxForcePasswordChange = QCheckBox(self.groupBox_3)
        self.checkBoxForcePasswordChange.setObjectName(u"checkBoxForcePasswordChange")
        self.checkBoxForcePasswordChange.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.verticalLayout.addWidget(self.checkBoxForcePasswordChange)

        self.pushButtonSetTemporaryPassword = QPushButton(self.groupBox_3)
        self.pushButtonSetTemporaryPassword.setObjectName(u"pushButtonSetTemporaryPassword")

        self.verticalLayout.addWidget(self.pushButtonSetTemporaryPassword)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_6.addWidget(self.groupBox_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout_13.addLayout(self.horizontalLayout_4)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_9 = QVBoxLayout(self.page_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.tableView = EnhancedTableView(self.page_2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_9.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_4.addWidget(self.stackedWidget)

#if QT_CONFIG(shortcut)
        self.label_7.setBuddy(self.dateTimeEditLastLogin)
        self.label_12.setBuddy(self.dateTimeEditPasswordDate)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEditUser, self.lineEditUserDescription)
        QWidget.setTabOrder(self.lineEditUserDescription, self.comboBoxL10n)
        QWidget.setTabOrder(self.comboBoxL10n, self.checkBoxSystem)
        QWidget.setTabOrder(self.checkBoxSystem, self.checkBoxIsAdmin)
        QWidget.setTabOrder(self.checkBoxIsAdmin, self.checkBoxCanEditViews)
        QWidget.setTabOrder(self.checkBoxCanEditViews, self.checkBoxCanEditSortFilters)
        QWidget.setTabOrder(self.checkBoxCanEditSortFilters, self.checkBoxCanEditReports)
        QWidget.setTabOrder(self.checkBoxCanEditReports, self.pushButtonUpload)
        QWidget.setTabOrder(self.pushButtonUpload, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonDelete)
        QWidget.setTabOrder(self.pushButtonDelete, self.lineEditLastCompany)
        QWidget.setTabOrder(self.lineEditLastCompany, self.dateTimeEditLastLogin)
        QWidget.setTabOrder(self.dateTimeEditLastLogin, self.dateTimeEditPasswordDate)
        QWidget.setTabOrder(self.dateTimeEditPasswordDate, self.tableView)

        self.retranslateUi(UserWidget)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(UserWidget)
    # setupUi

    def retranslateUi(self, UserWidget):
        UserWidget.setWindowTitle(QCoreApplication.translate("UserWidget", u"User", None))
        self.groupBox.setTitle(QCoreApplication.translate("UserWidget", u"Code", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("UserWidget", u"Description", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("UserWidget", u"Language / Country", None))
        self.checkBoxSystem.setText(QCoreApplication.translate("UserWidget", u"System user", None))
        self.checkBoxIsAdmin.setText(QCoreApplication.translate("UserWidget", u"Administrator", None))
        self.checkBoxCanEditViews.setText(QCoreApplication.translate("UserWidget", u"Can edit views", None))
        self.checkBoxCanEditSortFilters.setText(QCoreApplication.translate("UserWidget", u"Can edit sort/filters", None))
        self.checkBoxCanEditReports.setText(QCoreApplication.translate("UserWidget", u"Can edit reports", None))
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("UserWidget", u"Company / Profile / Menu / Toolbar", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("UserWidget", u"User Image", None))
        self.labelImage.setText(QCoreApplication.translate("UserWidget", u"NO IMAGE", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("UserWidget", u"Upload ...", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("UserWidget", u"Download ...", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("UserWidget", u"Delete", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("UserWidget", u"Security", None))
        self.label_5.setText(QCoreApplication.translate("UserWidget", u"Last used company", None))
        self.label_7.setText(QCoreApplication.translate("UserWidget", u"Last login", None))
        self.label_12.setText(QCoreApplication.translate("UserWidget", u"Last password change", None))
        self.checkBoxForcePasswordChange.setText(QCoreApplication.translate("UserWidget", u"Force password change", None))
        self.pushButtonSetTemporaryPassword.setText(QCoreApplication.translate("UserWidget", u"Set temporary password", None))
    # retranslateUi

