# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ItemWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QTabWidget, QVBoxLayout, QWidget)

from App.Widget.Control import (ColorComboBox, RelationalComboBox)
from App.Widget.View import EnhancedTableView

class Ui_ItemWidget(object):
    def setupUi(self, ItemWidget):
        if not ItemWidget.objectName():
            ItemWidget.setObjectName(u"ItemWidget")
        ItemWidget.resize(1034, 720)
        self.verticalLayout_4 = QVBoxLayout(ItemWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.stackedWidget = QStackedWidget(ItemWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_16 = QVBoxLayout(self.page)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBoxType = RelationalComboBox(self.groupBox)
        self.comboBoxType.setObjectName(u"comboBoxType")

        self.verticalLayout.addWidget(self.comboBoxType)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.page)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditDescription = QLineEdit(self.groupBox_2)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.verticalLayout_2.addWidget(self.lineEditDescription)

        self.lineEditCustomerDescription = QLineEdit(self.groupBox_2)
        self.lineEditCustomerDescription.setObjectName(u"lineEditCustomerDescription")

        self.verticalLayout_2.addWidget(self.lineEditCustomerDescription)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.page)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBoxDepartment = RelationalComboBox(self.groupBox_3)
        self.comboBoxDepartment.setObjectName(u"comboBoxDepartment")

        self.verticalLayout_8.addWidget(self.comboBoxDepartment)


        self.horizontalLayout.addWidget(self.groupBox_3)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxKitPart = QCheckBox(self.page)
        self.checkBoxKitPart.setObjectName(u"checkBoxKitPart")
        self.checkBoxKitPart.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxKitPart, 1, 0, 1, 1)

        self.checkBoxInventoryControl = QCheckBox(self.page)
        self.checkBoxInventoryControl.setObjectName(u"checkBoxInventoryControl")
        self.checkBoxInventoryControl.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxInventoryControl, 0, 0, 1, 1)

        self.checkBoxMenuPart = QCheckBox(self.page)
        self.checkBoxMenuPart.setObjectName(u"checkBoxMenuPart")
        self.checkBoxMenuPart.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxMenuPart, 1, 1, 1, 1)

        self.checkBoxDeliveredControl = QCheckBox(self.page)
        self.checkBoxDeliveredControl.setObjectName(u"checkBoxDeliveredControl")
        self.checkBoxDeliveredControl.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxDeliveredControl, 0, 1, 1, 1)

        self.checkBoxObsolete = QCheckBox(self.page)
        self.checkBoxObsolete.setObjectName(u"checkBoxObsolete")
        self.checkBoxObsolete.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.gridLayout.addWidget(self.checkBoxObsolete, 0, 2, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_16.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxSalable = QCheckBox(self.page)
        self.checkBoxSalable.setObjectName(u"checkBoxSalable")
        self.checkBoxSalable.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_3.addWidget(self.checkBoxSalable)

        self.groupBox_4 = QGroupBox(self.page)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.spinBoxRow = QSpinBox(self.groupBox_4)
        self.spinBoxRow.setObjectName(u"spinBoxRow")
        self.spinBoxRow.setEnabled(False)
        self.spinBoxRow.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_9.addWidget(self.spinBoxRow)


        self.horizontalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.page)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.spinBoxColumn = QSpinBox(self.groupBox_5)
        self.spinBoxColumn.setObjectName(u"spinBoxColumn")
        self.spinBoxColumn.setEnabled(False)
        self.spinBoxColumn.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_10.addWidget(self.spinBoxColumn)


        self.horizontalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.page)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.spinBoxSorting = QSpinBox(self.groupBox_6)
        self.spinBoxSorting.setObjectName(u"spinBoxSorting")
        self.spinBoxSorting.setEnabled(False)
        self.spinBoxSorting.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxSorting.setMaximum(999)

        self.verticalLayout_11.addWidget(self.spinBoxSorting)


        self.horizontalLayout_3.addWidget(self.groupBox_6)

        self.groupBox_9 = QGroupBox(self.page)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.comboBoxNormalBackgroundColor = ColorComboBox(self.groupBox_9)
        self.comboBoxNormalBackgroundColor.setObjectName(u"comboBoxNormalBackgroundColor")

        self.verticalLayout_15.addWidget(self.comboBoxNormalBackgroundColor)


        self.horizontalLayout_3.addWidget(self.groupBox_9)

        self.groupBox_8 = QGroupBox(self.page)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.comboBoxNormalTextColor = ColorComboBox(self.groupBox_8)
        self.comboBoxNormalTextColor.setObjectName(u"comboBoxNormalTextColor")

        self.verticalLayout_14.addWidget(self.comboBoxNormalTextColor)


        self.horizontalLayout_3.addWidget(self.groupBox_8)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.checkBoxWebAvailable = QCheckBox(self.page)
        self.checkBoxWebAvailable.setObjectName(u"checkBoxWebAvailable")
        self.checkBoxWebAvailable.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_3.addWidget(self.checkBoxWebAvailable)

        self.groupBox_10 = QGroupBox(self.page)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.spinBoxWebSorting = QSpinBox(self.groupBox_10)
        self.spinBoxWebSorting.setObjectName(u"spinBoxWebSorting")
        self.spinBoxWebSorting.setEnabled(False)
        self.spinBoxWebSorting.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_13.addWidget(self.spinBoxWebSorting)


        self.horizontalLayout_3.addWidget(self.groupBox_10)


        self.verticalLayout_16.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.checkBoxVariants = QCheckBox(self.page)
        self.checkBoxVariants.setObjectName(u"checkBoxVariants")
        self.checkBoxVariants.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout_5.addWidget(self.checkBoxVariants)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout_16.addLayout(self.horizontalLayout_5)

        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabVariants = QWidget()
        self.tabVariants.setObjectName(u"tabVariants")
        self.verticalLayout_3 = QVBoxLayout(self.tabVariants)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableViewVariants = EnhancedTableView(self.tabVariants)
        self.tableViewVariants.setObjectName(u"tableViewVariants")
        self.tableViewVariants.setEnabled(True)

        self.verticalLayout_3.addWidget(self.tableViewVariants)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButtonAddVar = QPushButton(self.tabVariants)
        self.pushButtonAddVar.setObjectName(u"pushButtonAddVar")

        self.horizontalLayout_6.addWidget(self.pushButtonAddVar)

        self.pushButtonRemoveVar = QPushButton(self.tabVariants)
        self.pushButtonRemoveVar.setObjectName(u"pushButtonRemoveVar")

        self.horizontalLayout_6.addWidget(self.pushButtonRemoveVar)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.tabWidget.addTab(self.tabVariants, "")
        self.tabComponents = QWidget()
        self.tabComponents.setObjectName(u"tabComponents")
        self.verticalLayout_6 = QVBoxLayout(self.tabComponents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tableViewComponents = EnhancedTableView(self.tabComponents)
        self.tableViewComponents.setObjectName(u"tableViewComponents")
        self.tableViewComponents.setEnabled(False)

        self.verticalLayout_6.addWidget(self.tableViewComponents)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButtonAddKit = QPushButton(self.tabComponents)
        self.pushButtonAddKit.setObjectName(u"pushButtonAddKit")

        self.horizontalLayout_7.addWidget(self.pushButtonAddKit)

        self.pushButtonRemoveKit = QPushButton(self.tabComponents)
        self.pushButtonRemoveKit.setObjectName(u"pushButtonRemoveKit")

        self.horizontalLayout_7.addWidget(self.pushButtonRemoveKit)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.tabWidget.addTab(self.tabComponents, "")
        self.tabMenuItems = QWidget()
        self.tabMenuItems.setObjectName(u"tabMenuItems")
        self.verticalLayout_7 = QVBoxLayout(self.tabMenuItems)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableViewMenuItems = EnhancedTableView(self.tabMenuItems)
        self.tableViewMenuItems.setObjectName(u"tableViewMenuItems")
        self.tableViewMenuItems.setEnabled(False)

        self.verticalLayout_7.addWidget(self.tableViewMenuItems)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButtonAddMen = QPushButton(self.tabMenuItems)
        self.pushButtonAddMen.setObjectName(u"pushButtonAddMen")

        self.horizontalLayout_8.addWidget(self.pushButtonAddMen)

        self.pushButtonRemoveMen = QPushButton(self.tabMenuItems)
        self.pushButtonRemoveMen.setObjectName(u"pushButtonRemoveMen")

        self.horizontalLayout_8.addWidget(self.pushButtonRemoveMen)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.tabWidget.addTab(self.tabMenuItems, "")
        self.tabPrices = QWidget()
        self.tabPrices.setObjectName(u"tabPrices")
        self.verticalLayout_12 = QVBoxLayout(self.tabPrices)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tableViewPrices = EnhancedTableView(self.tabPrices)
        self.tableViewPrices.setObjectName(u"tableViewPrices")
        self.tableViewPrices.setEnabled(True)

        self.verticalLayout_12.addWidget(self.tableViewPrices)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButtonAddPri = QPushButton(self.tabPrices)
        self.pushButtonAddPri.setObjectName(u"pushButtonAddPri")

        self.horizontalLayout_9.addWidget(self.pushButtonAddPri)

        self.pushButtonRemovePri = QPushButton(self.tabPrices)
        self.pushButtonRemovePri.setObjectName(u"pushButtonRemovePri")

        self.horizontalLayout_9.addWidget(self.pushButtonRemovePri)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)


        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.tabWidget.addTab(self.tabPrices, "")

        self.verticalLayout_16.addWidget(self.tabWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonCopyVariants = QPushButton(self.page)
        self.pushButtonCopyVariants.setObjectName(u"pushButtonCopyVariants")
        self.pushButtonCopyVariants.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCopyVariants)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_16.addLayout(self.horizontalLayout_4)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableView = EnhancedTableView(self.page_2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_5.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_4.addWidget(self.stackedWidget)

        QWidget.setTabOrder(self.comboBoxType, self.lineEditDescription)
        QWidget.setTabOrder(self.lineEditDescription, self.lineEditCustomerDescription)
        QWidget.setTabOrder(self.lineEditCustomerDescription, self.comboBoxDepartment)
        QWidget.setTabOrder(self.comboBoxDepartment, self.checkBoxInventoryControl)
        QWidget.setTabOrder(self.checkBoxInventoryControl, self.checkBoxKitPart)
        QWidget.setTabOrder(self.checkBoxKitPart, self.checkBoxMenuPart)
        QWidget.setTabOrder(self.checkBoxMenuPart, self.checkBoxSalable)
        QWidget.setTabOrder(self.checkBoxSalable, self.spinBoxRow)
        QWidget.setTabOrder(self.spinBoxRow, self.spinBoxColumn)
        QWidget.setTabOrder(self.spinBoxColumn, self.spinBoxSorting)
        QWidget.setTabOrder(self.spinBoxSorting, self.comboBoxNormalBackgroundColor)
        QWidget.setTabOrder(self.comboBoxNormalBackgroundColor, self.comboBoxNormalTextColor)
        QWidget.setTabOrder(self.comboBoxNormalTextColor, self.checkBoxWebAvailable)
        QWidget.setTabOrder(self.checkBoxWebAvailable, self.spinBoxWebSorting)
        QWidget.setTabOrder(self.spinBoxWebSorting, self.checkBoxVariants)
        QWidget.setTabOrder(self.checkBoxVariants, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.tableViewPrices)
        QWidget.setTabOrder(self.tableViewPrices, self.pushButtonCopyVariants)
        QWidget.setTabOrder(self.pushButtonCopyVariants, self.tableViewVariants)
        QWidget.setTabOrder(self.tableViewVariants, self.tableView)
        QWidget.setTabOrder(self.tableView, self.tableViewComponents)
        QWidget.setTabOrder(self.tableViewComponents, self.tableViewMenuItems)

        self.retranslateUi(ItemWidget)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ItemWidget)
    # setupUi

    def retranslateUi(self, ItemWidget):
        ItemWidget.setWindowTitle(QCoreApplication.translate("ItemWidget", u"Item", None))
        self.groupBox.setTitle(QCoreApplication.translate("ItemWidget", u"Item type", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ItemWidget", u"Item description / customer description", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ItemWidget", u"Department", None))
        self.checkBoxKitPart.setText(QCoreApplication.translate("ItemWidget", u"Kit part", None))
        self.checkBoxInventoryControl.setText(QCoreApplication.translate("ItemWidget", u"Inventory control", None))
        self.checkBoxMenuPart.setText(QCoreApplication.translate("ItemWidget", u"Menu part", None))
        self.checkBoxDeliveredControl.setText(QCoreApplication.translate("ItemWidget", u"Delivered control", None))
        self.checkBoxObsolete.setText(QCoreApplication.translate("ItemWidget", u"Obsolete", None))
        self.checkBoxSalable.setText(QCoreApplication.translate("ItemWidget", u"Salable", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ItemWidget", u"Row", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("ItemWidget", u"Column", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("ItemWidget", u"Sorting", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("ItemWidget", u"Normal background color", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("ItemWidget", u"Normal text color", None))
        self.checkBoxWebAvailable.setText(QCoreApplication.translate("ItemWidget", u"Web available", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("ItemWidget", u"Web sorting", None))
        self.checkBoxVariants.setText(QCoreApplication.translate("ItemWidget", u"Has variants", None))
        self.pushButtonAddVar.setText("")
        self.pushButtonRemoveVar.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVariants), QCoreApplication.translate("ItemWidget", u"Variants", None))
        self.pushButtonAddKit.setText("")
        self.pushButtonRemoveKit.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabComponents), QCoreApplication.translate("ItemWidget", u"Components", None))
        self.pushButtonAddMen.setText("")
        self.pushButtonRemoveMen.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMenuItems), QCoreApplication.translate("ItemWidget", u"Menu items", None))
        self.pushButtonAddPri.setText("")
        self.pushButtonRemovePri.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPrices), QCoreApplication.translate("ItemWidget", u"Prices", None))
        self.pushButtonCopyVariants.setText(QCoreApplication.translate("ItemWidget", u"Copy variants from ...", None))
    # retranslateUi

