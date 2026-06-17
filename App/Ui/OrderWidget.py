# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateEdit, QGroupBox,
    QHBoxLayout, QHeaderView, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QTabWidget, QTimeEdit, QTreeView, QVBoxLayout,
    QWidget)

from App.Widget.Control import (DateTimeEdit, RelationalComboBox, SpinBoxDecimal)
from App.Widget.View import EnhancedTableView

class Ui_OrderWidget(object):
    def setupUi(self, OrderWidget):
        if not OrderWidget.objectName():
            OrderWidget.setObjectName(u"OrderWidget")
        OrderWidget.resize(1184, 552)
        self.verticalLayout_19 = QVBoxLayout(OrderWidget)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.stackedWidget = QStackedWidget(OrderWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_24 = QVBoxLayout(self.page1)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.page1)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.spinBoxNumber = QSpinBox(self.groupBox)
        self.spinBoxNumber.setObjectName(u"spinBoxNumber")
        self.spinBoxNumber.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxNumber.setMinimum(0)
        self.spinBoxNumber.setMaximum(99999)
        self.spinBoxNumber.setValue(0)

        self.verticalLayout_5.addWidget(self.spinBoxNumber)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.page1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.dateEditDate = QDateEdit(self.groupBox_2)
        self.dateEditDate.setObjectName(u"dateEditDate")

        self.verticalLayout_6.addWidget(self.dateEditDate)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.timeEditTime = QTimeEdit(self.groupBox_3)
        self.timeEditTime.setObjectName(u"timeEditTime")

        self.verticalLayout_8.addWidget(self.timeEditTime)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.page1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.comboBoxDelivery = RelationalComboBox(self.groupBox_4)
        self.comboBoxDelivery.setObjectName(u"comboBoxDelivery")

        self.verticalLayout_9.addWidget(self.comboBoxDelivery)


        self.horizontalLayout.addWidget(self.groupBox_4)

        self.groupBox_15 = QGroupBox(self.page1)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.checkBoxElectronicPayment = QCheckBox(self.groupBox_15)
        self.checkBoxElectronicPayment.setObjectName(u"checkBoxElectronicPayment")
        self.checkBoxElectronicPayment.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.verticalLayout_22.addWidget(self.checkBoxElectronicPayment, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout.addWidget(self.groupBox_15)

        self.groupBox_16 = QGroupBox(self.page1)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_16)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.checkBoxWebOrder = QCheckBox(self.groupBox_16)
        self.checkBoxWebOrder.setObjectName(u"checkBoxWebOrder")
        self.checkBoxWebOrder.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.verticalLayout_23.addWidget(self.checkBoxWebOrder)


        self.horizontalLayout.addWidget(self.groupBox_16)

        self.groupBox_7 = QGroupBox(self.page1)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.doubleSpinBoxTotalAmount = SpinBoxDecimal(self.groupBox_7)
        self.doubleSpinBoxTotalAmount.setObjectName(u"doubleSpinBoxTotalAmount")
        self.doubleSpinBoxTotalAmount.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxTotalAmount.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxTotalAmount.setMaximum(9999.989999999999782)

        self.verticalLayout_12.addWidget(self.doubleSpinBoxTotalAmount)


        self.horizontalLayout.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.page1)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.doubleSpinBoxDiscount = SpinBoxDecimal(self.groupBox_8)
        self.doubleSpinBoxDiscount.setObjectName(u"doubleSpinBoxDiscount")
        self.doubleSpinBoxDiscount.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxDiscount.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxDiscount.setMaximum(9999.989999999999782)

        self.verticalLayout_13.addWidget(self.doubleSpinBoxDiscount)


        self.horizontalLayout.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.page1)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.doubleSpinBoxCash = SpinBoxDecimal(self.groupBox_9)
        self.doubleSpinBoxCash.setObjectName(u"doubleSpinBoxCash")
        self.doubleSpinBoxCash.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxCash.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxCash.setMaximum(9999.989999999999782)

        self.verticalLayout_14.addWidget(self.doubleSpinBoxCash)


        self.horizontalLayout.addWidget(self.groupBox_9)

        self.groupBox_10 = QGroupBox(self.page1)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout = QVBoxLayout(self.groupBox_10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.doubleSpinBoxChange = SpinBoxDecimal(self.groupBox_10)
        self.doubleSpinBoxChange.setObjectName(u"doubleSpinBoxChange")
        self.doubleSpinBoxChange.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxChange.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxChange.setMaximum(9999.989999999999782)

        self.verticalLayout.addWidget(self.doubleSpinBoxChange)


        self.horizontalLayout.addWidget(self.groupBox_10)


        self.verticalLayout_17.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_14 = QGroupBox(self.page1)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_14)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.lineEditCashDesk = QLineEdit(self.groupBox_14)
        self.lineEditCashDesk.setObjectName(u"lineEditCashDesk")

        self.verticalLayout_15.addWidget(self.lineEditCashDesk)


        self.horizontalLayout_4.addWidget(self.groupBox_14)

        self.groupBox_5 = QGroupBox(self.page1)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.lineEditTableNumber = QLineEdit(self.groupBox_5)
        self.lineEditTableNumber.setObjectName(u"lineEditTableNumber")

        self.verticalLayout_10.addWidget(self.lineEditTableNumber)


        self.horizontalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.page1)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.spinBoxCovers = QSpinBox(self.groupBox_6)
        self.spinBoxCovers.setObjectName(u"spinBoxCovers")
        self.spinBoxCovers.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_11.addWidget(self.spinBoxCovers)


        self.horizontalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_11 = QGroupBox(self.page1)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.lineEditCustomerName = QLineEdit(self.groupBox_11)
        self.lineEditCustomerName.setObjectName(u"lineEditCustomerName")

        self.verticalLayout_16.addWidget(self.lineEditCustomerName)


        self.horizontalLayout_4.addWidget(self.groupBox_11)

        self.groupBox_17 = QGroupBox(self.page1)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.verticalLayout_21 = QVBoxLayout(self.groupBox_17)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.lineEditCustomerContact = QLineEdit(self.groupBox_17)
        self.lineEditCustomerContact.setObjectName(u"lineEditCustomerContact")

        self.verticalLayout_21.addWidget(self.lineEditCustomerContact)


        self.horizontalLayout_4.addWidget(self.groupBox_17)

        self.groupBox_12 = QGroupBox(self.page1)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.comboBoxStatus = RelationalComboBox(self.groupBox_12)
        self.comboBoxStatus.setObjectName(u"comboBoxStatus")

        self.verticalLayout_18.addWidget(self.comboBoxStatus)


        self.horizontalLayout_4.addWidget(self.groupBox_12)

        self.groupBox_13 = QGroupBox(self.page1)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.dateTimeEditFullfillment = DateTimeEdit(self.groupBox_13)
        self.dateTimeEditFullfillment.setObjectName(u"dateTimeEditFullfillment")
        self.dateTimeEditFullfillment.setReadOnly(True)

        self.verticalLayout_20.addWidget(self.dateTimeEditFullfillment)


        self.horizontalLayout_4.addWidget(self.groupBox_13)


        self.verticalLayout_17.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_17)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_24.addLayout(self.horizontalLayout_5)

        self.tabWidget = QTabWidget(self.page1)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.tableViewDetails = EnhancedTableView(self.tab)
        self.tableViewDetails.setObjectName(u"tableViewDetails")

        self.verticalLayout_2.addWidget(self.tableViewDetails)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.treeViewDepartmentDetails = QTreeView(self.tab_2)
        self.treeViewDepartmentDetails.setObjectName(u"treeViewDepartmentDetails")
        self.treeViewDepartmentDetails.setDragEnabled(True)
        self.treeViewDepartmentDetails.setSortingEnabled(True)
        self.treeViewDepartmentDetails.setAnimated(True)
        self.treeViewDepartmentDetails.header().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.treeViewDepartmentDetails)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(3, 3, 3, 3)
        self.tableViewDepartmentHeader = EnhancedTableView(self.tab_3)
        self.tableViewDepartmentHeader.setObjectName(u"tableViewDepartmentHeader")

        self.verticalLayout_4.addWidget(self.tableViewDepartmentHeader)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_24.addWidget(self.tabWidget)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_7 = QVBoxLayout(self.page2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_7.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout_19.addWidget(self.stackedWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBoxReprint = QGroupBox(OrderWidget)
        self.groupBoxReprint.setObjectName(u"groupBoxReprint")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBoxReprint)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonPrint = QPushButton(self.groupBoxReprint)
        self.pushButtonPrint.setObjectName(u"pushButtonPrint")

        self.horizontalLayout_3.addWidget(self.pushButtonPrint)

        self.checkBoxPrintCustomerCopy = QCheckBox(self.groupBoxReprint)
        self.checkBoxPrintCustomerCopy.setObjectName(u"checkBoxPrintCustomerCopy")

        self.horizontalLayout_3.addWidget(self.checkBoxPrintCustomerCopy)

        self.checkBoxPrintCoverCopy = QCheckBox(self.groupBoxReprint)
        self.checkBoxPrintCoverCopy.setObjectName(u"checkBoxPrintCoverCopy")

        self.horizontalLayout_3.addWidget(self.checkBoxPrintCoverCopy)


        self.horizontalLayout_2.addWidget(self.groupBoxReprint)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_19.addLayout(self.horizontalLayout_2)


        self.retranslateUi(OrderWidget)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(OrderWidget)
    # setupUi

    def retranslateUi(self, OrderWidget):
        OrderWidget.setWindowTitle(QCoreApplication.translate("OrderWidget", u"Order widget", None))
        self.groupBox.setTitle(QCoreApplication.translate("OrderWidget", u"Number", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OrderWidget", u"Date", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("OrderWidget", u"Time", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OrderWidget", u"Delivery", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("OrderWidget", u"EP", None))
        self.checkBoxElectronicPayment.setText("")
        self.groupBox_16.setTitle(QCoreApplication.translate("OrderWidget", u"Web", None))
        self.checkBoxWebOrder.setText("")
        self.groupBox_7.setTitle(QCoreApplication.translate("OrderWidget", u"Total amount", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("OrderWidget", u"Discount", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("OrderWidget", u"Cash", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("OrderWidget", u"Change", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("OrderWidget", u"Cash desk", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("OrderWidget", u"Table", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("OrderWidget", u"Covers", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("OrderWidget", u"Customer name", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("OrderWidget", u"Customer contact", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("OrderWidget", u"Order status", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("OrderWidget", u"Fulfillment date", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("OrderWidget", u"Order details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("OrderWidget", u"Departments details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("OrderWidget", u"Department notes and status", None))
        self.groupBoxReprint.setTitle(QCoreApplication.translate("OrderWidget", u"Current order reprint", None))
        self.pushButtonPrint.setText(QCoreApplication.translate("OrderWidget", u"Print", None))
        self.checkBoxPrintCustomerCopy.setText(QCoreApplication.translate("OrderWidget", u"Customer", None))
        self.checkBoxPrintCoverCopy.setText(QCoreApplication.translate("OrderWidget", u"Cover", None))
    # retranslateUi

