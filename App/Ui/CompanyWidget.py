# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompanyWidget.ui'
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
    QHeaderView, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QVBoxLayout,
    QWidget)

from App.Widget.Control import LabelImage
from App.Widget.View import EnhancedTableView

class Ui_CompanyWidget(object):
    def setupUi(self, CompanyWidget):
        if not CompanyWidget.objectName():
            CompanyWidget.setObjectName(u"CompanyWidget")
        CompanyWidget.resize(799, 592)
        self.verticalLayout_7 = QVBoxLayout(CompanyWidget)
#ifndef Q_OS_MAC
        self.verticalLayout_7.setSpacing(-1)
#endif
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.stackedWidget = QStackedWidget(CompanyWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_10 = QVBoxLayout(self.page1)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_2 = QGroupBox(self.page1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.spinBoxId = QSpinBox(self.groupBox_2)
        self.spinBoxId.setObjectName(u"spinBoxId")
        self.spinBoxId.setEnabled(False)
        self.spinBoxId.setMinimum(1)
        self.spinBoxId.setMaximum(99999)

        self.horizontalLayout_2.addWidget(self.spinBoxId)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.page1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditDescription = QLineEdit(self.groupBox_4)
        self.lineEditDescription.setObjectName(u"lineEditDescription")
        self.lineEditDescription.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_3.addWidget(self.lineEditDescription)


        self.horizontalLayout_4.addWidget(self.groupBox_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.checkBoxSystem = QCheckBox(self.page1)
        self.checkBoxSystem.setObjectName(u"checkBoxSystem")
        self.checkBoxSystem.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxSystem.sizePolicy().hasHeightForWidth())
        self.checkBoxSystem.setSizePolicy(sizePolicy)
        self.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.checkBoxSystem.setCheckable(True)

        self.verticalLayout_8.addWidget(self.checkBoxSystem)

        self.groupBox = QGroupBox(self.page1)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.userTableView = EnhancedTableView(self.groupBox)
        self.userTableView.setObjectName(u"userTableView")
        self.userTableView.setEnabled(True)

        self.verticalLayout.addWidget(self.userTableView)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButtonAdd = QPushButton(self.groupBox)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_6.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.groupBox)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_6.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.verticalLayout_8.addWidget(self.groupBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.groupBoxImage = QGroupBox(self.page1)
        self.groupBoxImage.setObjectName(u"groupBoxImage")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxImage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelCompanyImage = LabelImage(self.groupBoxImage)
        self.labelCompanyImage.setObjectName(u"labelCompanyImage")
        self.labelCompanyImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelCompanyImage.setProperty(u"hasImage", True)

        self.verticalLayout_2.addWidget(self.labelCompanyImage)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonUpload = QPushButton(self.groupBoxImage)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout.addWidget(self.pushButtonUpload)

        self.pushButtonDownload = QPushButton(self.groupBoxImage)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonDelete = QPushButton(self.groupBoxImage)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout.addWidget(self.pushButtonDelete)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout_9.addWidget(self.groupBoxImage)


        self.horizontalLayout_5.addLayout(self.verticalLayout_9)

        self.horizontalLayout_5.setStretch(0, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_5 = QVBoxLayout(self.page2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_5.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout_7.addWidget(self.stackedWidget)

        QWidget.setTabOrder(self.spinBoxId, self.lineEditDescription)
        QWidget.setTabOrder(self.lineEditDescription, self.pushButtonUpload)
        QWidget.setTabOrder(self.pushButtonUpload, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonDelete)
        QWidget.setTabOrder(self.pushButtonDelete, self.userTableView)
        QWidget.setTabOrder(self.userTableView, self.tableView)

        self.retranslateUi(CompanyWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CompanyWidget)
    # setupUi

    def retranslateUi(self, CompanyWidget):
        CompanyWidget.setWindowTitle(QCoreApplication.translate("CompanyWidget", u"Company", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("CompanyWidget", u"Code", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("CompanyWidget", u"Description", None))
        self.checkBoxSystem.setText(QCoreApplication.translate("CompanyWidget", u"System company", None))
        self.groupBox.setTitle(QCoreApplication.translate("CompanyWidget", u"User / Profiles / Menu / Toolbar", None))
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
        self.groupBoxImage.setTitle(QCoreApplication.translate("CompanyWidget", u"Company image", None))
        self.labelCompanyImage.setText(QCoreApplication.translate("CompanyWidget", u"NO IMAGE", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("CompanyWidget", u"Upload ...", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("CompanyWidget", u"Download ...", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("CompanyWidget", u"Delete", None))
    # retranslateUi

