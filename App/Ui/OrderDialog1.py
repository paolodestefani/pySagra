# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderDialog1.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QDialog, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLCDNumber,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_OrderDialog1(object):
    def setupUi(self, OrderDialog1):
        if not OrderDialog1.objectName():
            OrderDialog1.setObjectName(u"OrderDialog1")
        OrderDialog1.setWindowModality(Qt.WindowModality.NonModal)
        OrderDialog1.resize(1191, 485)
        font = QFont()
        font.setPointSize(10)
        OrderDialog1.setFont(font)
        OrderDialog1.setSizeGripEnabled(True)
        self.verticalLayout_12 = QVBoxLayout(OrderDialog1)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBoxDeliver = QGroupBox(OrderDialog1)
        self.groupBoxDeliver.setObjectName(u"groupBoxDeliver")
        self.verticalLayout_6 = QVBoxLayout(self.groupBoxDeliver)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButtonTable = QRadioButton(self.groupBoxDeliver)
        self.radioButtonTable.setObjectName(u"radioButtonTable")
        self.radioButtonTable.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButtonTable)

        self.radioButtonTakeAway = QRadioButton(self.groupBoxDeliver)
        self.radioButtonTakeAway.setObjectName(u"radioButtonTakeAway")

        self.horizontalLayout_2.addWidget(self.radioButtonTakeAway)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_4.addWidget(self.groupBoxDeliver)

        self.groupBoxTableNum = QGroupBox(OrderDialog1)
        self.groupBoxTableNum.setObjectName(u"groupBoxTableNum")
        self.verticalLayout_11 = QVBoxLayout(self.groupBoxTableNum)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(2, 2, 2, 2)
        self.lineEditTable = QLineEdit(self.groupBoxTableNum)
        self.lineEditTable.setObjectName(u"lineEditTable")

        self.verticalLayout_11.addWidget(self.lineEditTable)


        self.horizontalLayout_4.addWidget(self.groupBoxTableNum)

        self.groupBoxCovers = QGroupBox(OrderDialog1)
        self.groupBoxCovers.setObjectName(u"groupBoxCovers")
        self.verticalLayout_9 = QVBoxLayout(self.groupBoxCovers)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.spinBoxCovers = QSpinBox(self.groupBoxCovers)
        self.spinBoxCovers.setObjectName(u"spinBoxCovers")
        self.spinBoxCovers.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinBoxCovers.setMinimum(0)
        self.spinBoxCovers.setMaximum(999)

        self.verticalLayout_9.addWidget(self.spinBoxCovers)


        self.horizontalLayout_4.addWidget(self.groupBoxCovers)

        self.groupBoxCustomerName = QGroupBox(OrderDialog1)
        self.groupBoxCustomerName.setObjectName(u"groupBoxCustomerName")
        self.verticalLayout_10 = QVBoxLayout(self.groupBoxCustomerName)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(2, 2, 2, 2)
        self.lineEditCustomerName = QLineEdit(self.groupBoxCustomerName)
        self.lineEditCustomerName.setObjectName(u"lineEditCustomerName")

        self.verticalLayout_10.addWidget(self.lineEditCustomerName)


        self.horizontalLayout_4.addWidget(self.groupBoxCustomerName)

        self.groupBoxCustomerContact = QGroupBox(OrderDialog1)
        self.groupBoxCustomerContact.setObjectName(u"groupBoxCustomerContact")
        self.verticalLayout_17 = QVBoxLayout(self.groupBoxCustomerContact)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(2, 2, 2, 2)
        self.lineEditCustomerContact = QLineEdit(self.groupBoxCustomerContact)
        self.lineEditCustomerContact.setObjectName(u"lineEditCustomerContact")

        self.verticalLayout_17.addWidget(self.lineEditCustomerContact)


        self.horizontalLayout_4.addWidget(self.groupBoxCustomerContact)

        self.groupBoxWebOrderInput = QGroupBox(OrderDialog1)
        self.groupBoxWebOrderInput.setObjectName(u"groupBoxWebOrderInput")
        self.verticalLayout_8 = QVBoxLayout(self.groupBoxWebOrderInput)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.lineEditBarCode = QLineEdit(self.groupBoxWebOrderInput)
        self.lineEditBarCode.setObjectName(u"lineEditBarCode")

        self.verticalLayout_8.addWidget(self.lineEditBarCode)


        self.horizontalLayout_4.addWidget(self.groupBoxWebOrderInput)

        self.checkBoxWebOrder = QCheckBox(OrderDialog1)
        self.checkBoxWebOrder.setObjectName(u"checkBoxWebOrder")
        self.checkBoxWebOrder.setEnabled(True)
        self.checkBoxWebOrder.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.checkBoxWebOrder.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_4.addWidget(self.checkBoxWebOrder)

        self.pushButtonTablesSwitch = QPushButton(OrderDialog1)
        self.pushButtonTablesSwitch.setObjectName(u"pushButtonTablesSwitch")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTablesSwitch.sizePolicy().hasHeightForWidth())
        self.pushButtonTablesSwitch.setSizePolicy(sizePolicy)
        self.pushButtonTablesSwitch.setMinimumSize(QSize(120, 0))
        self.pushButtonTablesSwitch.setStyleSheet(u"text-align: left;")
        self.pushButtonTablesSwitch.setIconSize(QSize(48, 48))

        self.horizontalLayout_4.addWidget(self.pushButtonTablesSwitch)

        self.lcdNumberTime = QLCDNumber(OrderDialog1)
        self.lcdNumberTime.setObjectName(u"lcdNumberTime")
        self.lcdNumberTime.setMinimumSize(QSize(310, 0))
        self.lcdNumberTime.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumberTime.setSmallDecimalPoint(False)
        self.lcdNumberTime.setDigitCount(17)
        self.lcdNumberTime.setMode(QLCDNumber.Mode.Dec)
        self.lcdNumberTime.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumberTime.setProperty(u"value", 12345678901234568.000000000000000)

        self.horizontalLayout_4.addWidget(self.lcdNumberTime)


        self.verticalLayout_12.addLayout(self.horizontalLayout_4)

        self.stackedWidgetTableOrder = QStackedWidget(OrderDialog1)
        self.stackedWidgetTableOrder.setObjectName(u"stackedWidgetTableOrder")
        self.Order = QWidget()
        self.Order.setObjectName(u"Order")
        self.horizontalLayout_7 = QHBoxLayout(self.Order)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tabWidgetList = QTabWidget(self.Order)
        self.tabWidgetList.setObjectName(u"tabWidgetList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidgetList.sizePolicy().hasHeightForWidth())
        self.tabWidgetList.setSizePolicy(sizePolicy1)
        self.tabWidgetList.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.tabWidgetList.setFont(font1)
        self.tabWidgetList.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidgetList.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabWidgetList.setTabsClosable(False)

        self.verticalLayout_14.addWidget(self.tabWidgetList)

        self.groupBox_4 = QGroupBox(self.Order)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonVariants = QPushButton(self.groupBox_4)
        self.pushButtonVariants.setObjectName(u"pushButtonVariants")
        self.pushButtonVariants.setIconSize(QSize(32, 32))
        self.pushButtonVariants.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButtonVariants)

        self.pushButtonShowLevel = QPushButton(self.groupBox_4)
        self.pushButtonShowLevel.setObjectName(u"pushButtonShowLevel")
        self.pushButtonShowLevel.setIconSize(QSize(32, 32))
        self.pushButtonShowLevel.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButtonShowLevel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.labelCashDeskDescription = QLabel(self.groupBox_4)
        self.labelCashDeskDescription.setObjectName(u"labelCashDeskDescription")
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        self.labelCashDeskDescription.setFont(font2)
        self.labelCashDeskDescription.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.labelCashDeskDescription)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.groupBox = QGroupBox(self.groupBox_4)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton1 = QRadioButton(self.groupBox)
        self.radioButton1.setObjectName(u"radioButton1")
        self.radioButton1.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton1)

        self.radioButton5 = QRadioButton(self.groupBox)
        self.radioButton5.setObjectName(u"radioButton5")

        self.horizontalLayout.addWidget(self.radioButton5)

        self.radioButton10 = QRadioButton(self.groupBox)
        self.radioButton10.setObjectName(u"radioButton10")

        self.horizontalLayout.addWidget(self.radioButton10)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addWidget(self.groupBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_14.addWidget(self.groupBox_4)


        self.horizontalLayout_7.addLayout(self.verticalLayout_14)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.tabWidgetOrder = QTableWidget(self.Order)
        self.tabWidgetOrder.setObjectName(u"tabWidgetOrder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabWidgetOrder.sizePolicy().hasHeightForWidth())
        self.tabWidgetOrder.setSizePolicy(sizePolicy2)
        self.tabWidgetOrder.setMinimumSize(QSize(478, 0))
        font3 = QFont()
        font3.setPointSize(11)
        self.tabWidgetOrder.setFont(font3)
        self.tabWidgetOrder.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tabWidgetOrder.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tabWidgetOrder.setAutoScroll(False)
        self.tabWidgetOrder.setAutoScrollMargin(16)
        self.tabWidgetOrder.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabWidgetOrder.setAlternatingRowColors(True)
        self.tabWidgetOrder.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabWidgetOrder.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabWidgetOrder.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.tabWidgetOrder.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)
        self.tabWidgetOrder.setRowCount(0)
        self.tabWidgetOrder.setColumnCount(0)
        self.tabWidgetOrder.horizontalHeader().setDefaultSectionSize(150)
        self.tabWidgetOrder.verticalHeader().setVisible(False)

        self.verticalLayout_13.addWidget(self.tabWidgetOrder)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox_2 = QGroupBox(self.Order)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButtonDepartmentNote1 = QPushButton(self.groupBox_2)
        self.pushButtonDepartmentNote1.setObjectName(u"pushButtonDepartmentNote1")
        self.pushButtonDepartmentNote1.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButtonDepartmentNote1.sizePolicy().hasHeightForWidth())
        self.pushButtonDepartmentNote1.setSizePolicy(sizePolicy4)
        self.pushButtonDepartmentNote1.setMinimumSize(QSize(90, 0))

        self.verticalLayout_3.addWidget(self.pushButtonDepartmentNote1)

        self.pushButtonDepartmentNote2 = QPushButton(self.groupBox_2)
        self.pushButtonDepartmentNote2.setObjectName(u"pushButtonDepartmentNote2")
        self.pushButtonDepartmentNote2.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.pushButtonDepartmentNote2.sizePolicy().hasHeightForWidth())
        self.pushButtonDepartmentNote2.setSizePolicy(sizePolicy4)
        self.pushButtonDepartmentNote2.setMinimumSize(QSize(90, 0))

        self.verticalLayout_3.addWidget(self.pushButtonDepartmentNote2)

        self.pushButtonDepartmentNote3 = QPushButton(self.groupBox_2)
        self.pushButtonDepartmentNote3.setObjectName(u"pushButtonDepartmentNote3")
        self.pushButtonDepartmentNote3.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.pushButtonDepartmentNote3.sizePolicy().hasHeightForWidth())
        self.pushButtonDepartmentNote3.setSizePolicy(sizePolicy4)
        self.pushButtonDepartmentNote3.setMinimumSize(QSize(90, 0))

        self.verticalLayout_3.addWidget(self.pushButtonDepartmentNote3)

        self.pushButtonDepartmentNote4 = QPushButton(self.groupBox_2)
        self.pushButtonDepartmentNote4.setObjectName(u"pushButtonDepartmentNote4")
        self.pushButtonDepartmentNote4.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.pushButtonDepartmentNote4.sizePolicy().hasHeightForWidth())
        self.pushButtonDepartmentNote4.setSizePolicy(sizePolicy4)
        self.pushButtonDepartmentNote4.setMinimumSize(QSize(90, 0))

        self.verticalLayout_3.addWidget(self.pushButtonDepartmentNote4)

        self.pushButtonDepartmentNote5 = QPushButton(self.groupBox_2)
        self.pushButtonDepartmentNote5.setObjectName(u"pushButtonDepartmentNote5")
        self.pushButtonDepartmentNote5.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.pushButtonDepartmentNote5.sizePolicy().hasHeightForWidth())
        self.pushButtonDepartmentNote5.setSizePolicy(sizePolicy4)
        self.pushButtonDepartmentNote5.setMinimumSize(QSize(90, 0))

        self.verticalLayout_3.addWidget(self.pushButtonDepartmentNote5)


        self.horizontalLayout_5.addWidget(self.groupBox_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.Order)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_4.setFont(font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.doubleSpinBoxDiscount = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxDiscount.setObjectName(u"doubleSpinBoxDiscount")
        self.doubleSpinBoxDiscount.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxDiscount.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxDiscount.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxDiscount.setMaximum(9999.989999999999782)

        self.gridLayout.addWidget(self.doubleSpinBoxDiscount, 1, 1, 1, 1)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.doubleSpinBoxCash = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxCash.setObjectName(u"doubleSpinBoxCash")
        self.doubleSpinBoxCash.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxCash.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxCash.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxCash.setMaximum(9999.989999999999782)

        self.gridLayout.addWidget(self.doubleSpinBoxCash, 4, 1, 1, 1)

        self.doubleSpinBoxTotal = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxTotal.setObjectName(u"doubleSpinBoxTotal")
        self.doubleSpinBoxTotal.setFont(font1)
        self.doubleSpinBoxTotal.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        self.doubleSpinBoxTotal.setFrame(True)
        self.doubleSpinBoxTotal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxTotal.setReadOnly(True)
        self.doubleSpinBoxTotal.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxTotal.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxTotal.setMaximum(9999.989999999999782)

        self.gridLayout.addWidget(self.doubleSpinBoxTotal, 2, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setFrameShape(QFrame.Shape.NoFrame)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font4)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)

        self.doubleSpinBoxChange = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxChange.setObjectName(u"doubleSpinBoxChange")
        self.doubleSpinBoxChange.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxChange.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxChange.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxChange.setMaximum(9999.989999999999782)

        self.gridLayout.addWidget(self.doubleSpinBoxChange, 5, 1, 1, 1)

        self.doubleSpinBoxSubTotal = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBoxSubTotal.setObjectName(u"doubleSpinBoxSubTotal")
        self.doubleSpinBoxSubTotal.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))
        self.doubleSpinBoxSubTotal.setFrame(True)
        self.doubleSpinBoxSubTotal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBoxSubTotal.setReadOnly(True)
        self.doubleSpinBoxSubTotal.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxSubTotal.setProperty(u"showGroupSeparator", True)
        self.doubleSpinBoxSubTotal.setMaximum(9999.989999999999782)

        self.gridLayout.addWidget(self.doubleSpinBoxSubTotal, 0, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.checkBoxElectronicPayment = QCheckBox(self.groupBox_3)
        self.checkBoxElectronicPayment.setObjectName(u"checkBoxElectronicPayment")
        self.checkBoxElectronicPayment.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxElectronicPayment, 3, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButtonConfirm = QPushButton(self.Order)
        self.pushButtonConfirm.setObjectName(u"pushButtonConfirm")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButtonConfirm.sizePolicy().hasHeightForWidth())
        self.pushButtonConfirm.setSizePolicy(sizePolicy5)
        self.pushButtonConfirm.setMinimumSize(QSize(150, 0))
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        self.pushButtonConfirm.setFont(font5)
        self.pushButtonConfirm.setIconSize(QSize(32, 32))

        self.horizontalLayout_6.addWidget(self.pushButtonConfirm)

        self.pushButtonCancel = QPushButton(self.Order)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        sizePolicy5.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy5)
        self.pushButtonCancel.setMinimumSize(QSize(120, 0))
        font6 = QFont()
        font6.setPointSize(12)
        self.pushButtonCancel.setFont(font6)
        self.pushButtonCancel.setIconSize(QSize(32, 32))

        self.horizontalLayout_6.addWidget(self.pushButtonCancel)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)


        self.verticalLayout_13.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_7.addLayout(self.verticalLayout_13)

        self.stackedWidgetTableOrder.addWidget(self.Order)
        self.Tables = QWidget()
        self.Tables.setObjectName(u"Tables")
        self.verticalLayout_7 = QVBoxLayout(self.Tables)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.scrollArea = QScrollArea(self.Tables)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 28))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frameTables = QFrame(self.scrollAreaWidgetContents)
        self.frameTables.setObjectName(u"frameTables")
        self.frameTables.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameTables.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frameTables)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)
        self.gridLayoutTables = QGridLayout()
        self.gridLayoutTables.setObjectName(u"gridLayoutTables")

        self.verticalLayout_15.addLayout(self.gridLayoutTables)


        self.verticalLayout_16.addWidget(self.frameTables)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)

        self.stackedWidgetTableOrder.addWidget(self.Tables)

        self.verticalLayout_12.addWidget(self.stackedWidgetTableOrder)

        QWidget.setTabOrder(self.radioButtonTable, self.radioButtonTakeAway)
        QWidget.setTabOrder(self.radioButtonTakeAway, self.lineEditTable)
        QWidget.setTabOrder(self.lineEditTable, self.spinBoxCovers)
        QWidget.setTabOrder(self.spinBoxCovers, self.lineEditCustomerName)
        QWidget.setTabOrder(self.lineEditCustomerName, self.tabWidgetList)
        QWidget.setTabOrder(self.tabWidgetList, self.pushButtonVariants)
        QWidget.setTabOrder(self.pushButtonVariants, self.pushButtonShowLevel)
        QWidget.setTabOrder(self.pushButtonShowLevel, self.radioButton1)
        QWidget.setTabOrder(self.radioButton1, self.radioButton5)
        QWidget.setTabOrder(self.radioButton5, self.radioButton10)
        QWidget.setTabOrder(self.radioButton10, self.tabWidgetOrder)
        QWidget.setTabOrder(self.tabWidgetOrder, self.pushButtonDepartmentNote1)
        QWidget.setTabOrder(self.pushButtonDepartmentNote1, self.pushButtonDepartmentNote2)
        QWidget.setTabOrder(self.pushButtonDepartmentNote2, self.pushButtonDepartmentNote3)
        QWidget.setTabOrder(self.pushButtonDepartmentNote3, self.pushButtonDepartmentNote4)
        QWidget.setTabOrder(self.pushButtonDepartmentNote4, self.pushButtonDepartmentNote5)
        QWidget.setTabOrder(self.pushButtonDepartmentNote5, self.doubleSpinBoxSubTotal)
        QWidget.setTabOrder(self.doubleSpinBoxSubTotal, self.doubleSpinBoxDiscount)
        QWidget.setTabOrder(self.doubleSpinBoxDiscount, self.doubleSpinBoxTotal)
        QWidget.setTabOrder(self.doubleSpinBoxTotal, self.doubleSpinBoxCash)
        QWidget.setTabOrder(self.doubleSpinBoxCash, self.doubleSpinBoxChange)
        QWidget.setTabOrder(self.doubleSpinBoxChange, self.pushButtonConfirm)
        QWidget.setTabOrder(self.pushButtonConfirm, self.pushButtonCancel)

        self.retranslateUi(OrderDialog1)

        self.stackedWidgetTableOrder.setCurrentIndex(0)
        self.tabWidgetList.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(OrderDialog1)
    # setupUi

    def retranslateUi(self, OrderDialog1):
        OrderDialog1.setWindowTitle(QCoreApplication.translate("OrderDialog1", u"Order dialog", None))
        self.groupBoxDeliver.setTitle(QCoreApplication.translate("OrderDialog1", u"Deliver to", None))
        self.radioButtonTable.setText(QCoreApplication.translate("OrderDialog1", u"Table", None))
        self.radioButtonTakeAway.setText(QCoreApplication.translate("OrderDialog1", u"Take-away", None))
        self.groupBoxTableNum.setTitle(QCoreApplication.translate("OrderDialog1", u"Table number", None))
        self.lineEditTable.setInputMask("")
        self.groupBoxCovers.setTitle(QCoreApplication.translate("OrderDialog1", u"Covers", None))
        self.groupBoxCustomerName.setTitle(QCoreApplication.translate("OrderDialog1", u"Customer name", None))
        self.groupBoxCustomerContact.setTitle(QCoreApplication.translate("OrderDialog1", u"Customer contact", None))
        self.groupBoxWebOrderInput.setTitle(QCoreApplication.translate("OrderDialog1", u"Web order input", None))
#if QT_CONFIG(tooltip)
        self.lineEditBarCode.setToolTip(QCoreApplication.translate("OrderDialog1", u"Press Ctrl+F11 to set focus here", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBoxWebOrder.setToolTip(QCoreApplication.translate("OrderDialog1", u"Checked if this order was imported from an web order QRC or number", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxWebOrder.setText(QCoreApplication.translate("OrderDialog1", u"WO", None))
#if QT_CONFIG(tooltip)
        self.lcdNumberTime.setToolTip(QCoreApplication.translate("OrderDialog1", u"Press Ctrl+F12 to change date and time", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_4.setTitle("")
        self.pushButtonVariants.setText(QCoreApplication.translate("OrderDialog1", u"Choose variants", None))
        self.pushButtonShowLevel.setText(QCoreApplication.translate("OrderDialog1", u"Show stock", None))
        self.labelCashDeskDescription.setText(QCoreApplication.translate("OrderDialog1", u"Cash description", None))
        self.groupBox.setTitle(QCoreApplication.translate("OrderDialog1", u"Quantity", None))
        self.radioButton1.setText(QCoreApplication.translate("OrderDialog1", u"1", None))
        self.radioButton5.setText(QCoreApplication.translate("OrderDialog1", u"5", None))
        self.radioButton10.setText(QCoreApplication.translate("OrderDialog1", u"10", None))
        self.groupBox_2.setTitle("")
        self.pushButtonDepartmentNote1.setText("")
        self.pushButtonDepartmentNote2.setText("")
        self.pushButtonDepartmentNote3.setText("")
        self.pushButtonDepartmentNote4.setText("")
        self.pushButtonDepartmentNote5.setText("")
        self.groupBox_3.setTitle("")
        self.label_4.setText(QCoreApplication.translate("OrderDialog1", u"Amount", None))
        self.label.setText(QCoreApplication.translate("OrderDialog1", u"Discount", None))
        self.label_7.setText(QCoreApplication.translate("OrderDialog1", u"Total", None))
        self.label_10.setText(QCoreApplication.translate("OrderDialog1", u"Change", None))
        self.label_9.setText(QCoreApplication.translate("OrderDialog1", u"Cash", None))
        self.label_2.setText(QCoreApplication.translate("OrderDialog1", u"Elect.Paym.", None))
        self.checkBoxElectronicPayment.setText("")
        self.pushButtonConfirm.setText(QCoreApplication.translate("OrderDialog1", u"Confirm", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("OrderDialog1", u"Cancel", None))
    # retranslateUi

