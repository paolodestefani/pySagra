# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFontComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

from App.Widget.Control import (ButtonItemExample, ColorComboBox, RelationalComboBox)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        SettingsDialog.resize(760, 588)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsDialog.sizePolicy().hasHeightForWidth())
        SettingsDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_17 = QVBoxLayout(SettingsDialog)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.labelIcon = QLabel(SettingsDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_13.addWidget(self.labelIcon)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_13)

        self.tabWidget = QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        self.verticalLayout_27 = QVBoxLayout(self.tab1)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.groupBox_14 = QGroupBox(self.tab1)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.verticalLayout_28 = QVBoxLayout(self.groupBox_14)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_24 = QLabel(self.groupBox_14)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_7.addWidget(self.label_24, 0, 0, 1, 1)

        self.spinBoxQuantityDecimals = QSpinBox(self.groupBox_14)
        self.spinBoxQuantityDecimals.setObjectName(u"spinBoxQuantityDecimals")
        self.spinBoxQuantityDecimals.setMaximum(4)

        self.gridLayout_7.addWidget(self.spinBoxQuantityDecimals, 0, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_14)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_7.addWidget(self.label_9, 1, 0, 1, 1)

        self.spinBoxPriceDecimals = QSpinBox(self.groupBox_14)
        self.spinBoxPriceDecimals.setObjectName(u"spinBoxPriceDecimals")
        self.spinBoxPriceDecimals.setMaximum(6)

        self.gridLayout_7.addWidget(self.spinBoxPriceDecimals, 1, 1, 1, 1)

        self.label_30 = QLabel(self.groupBox_14)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_7.addWidget(self.label_30, 2, 0, 1, 1)

        self.spinBoxAmountDecimals = QSpinBox(self.groupBox_14)
        self.spinBoxAmountDecimals.setObjectName(u"spinBoxAmountDecimals")
        self.spinBoxAmountDecimals.setMaximum(4)

        self.gridLayout_7.addWidget(self.spinBoxAmountDecimals, 2, 1, 1, 1)


        self.horizontalLayout_17.addLayout(self.gridLayout_7)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.spacer = QSpacerItem(13, 13, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.spacer)

        self.label_25 = QLabel(self.groupBox_14)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_16.addWidget(self.label_25)

        self.lineEditCurrencySymbol = QLineEdit(self.groupBox_14)
        self.lineEditCurrencySymbol.setObjectName(u"lineEditCurrencySymbol")
        self.lineEditCurrencySymbol.setMaximumSize(QSize(80, 16777215))
        self.lineEditCurrencySymbol.setMaxLength(3)

        self.horizontalLayout_16.addWidget(self.lineEditCurrencySymbol)


        self.verticalLayout_21.addLayout(self.horizontalLayout_16)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_21.addItem(self.verticalSpacer_8)


        self.horizontalLayout_17.addLayout(self.verticalLayout_21)


        self.verticalLayout_28.addLayout(self.horizontalLayout_17)


        self.verticalLayout_27.addWidget(self.groupBox_14)

        self.groupBox_10 = QGroupBox(self.tab1)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.labelYellow_12 = QLabel(self.groupBox_10)
        self.labelYellow_12.setObjectName(u"labelYellow_12")
        font = QFont()
        font.setBold(False)
        self.labelYellow_12.setFont(font)
        self.labelYellow_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.labelYellow_12, 0, 0, 1, 1)

        self.labelRed_9 = QLabel(self.groupBox_10)
        self.labelRed_9.setObjectName(u"labelRed_9")
        self.labelRed_9.setFont(font)
        self.labelRed_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.labelRed_9, 0, 1, 1, 1)

        self.labelRed_8 = QLabel(self.groupBox_10)
        self.labelRed_8.setObjectName(u"labelRed_8")
        self.labelRed_8.setFont(font)
        self.labelRed_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.labelRed_8, 0, 2, 1, 1)

        self.colorComboBoxBackground = ColorComboBox(self.groupBox_10)
        self.colorComboBoxBackground.setObjectName(u"colorComboBoxBackground")

        self.gridLayout_8.addWidget(self.colorComboBoxBackground, 1, 0, 1, 1)

        self.colorComboBoxText = ColorComboBox(self.groupBox_10)
        self.colorComboBoxText.setObjectName(u"colorComboBoxText")

        self.gridLayout_8.addWidget(self.colorComboBoxText, 1, 1, 1, 1)

        self.pushButtonExampleNL = ButtonItemExample(self.groupBox_10)
        self.pushButtonExampleNL.setObjectName(u"pushButtonExampleNL")

        self.gridLayout_8.addWidget(self.pushButtonExampleNL, 1, 2, 1, 1)


        self.verticalLayout_20.addLayout(self.gridLayout_8)


        self.verticalLayout_27.addWidget(self.groupBox_10)

        self.groupBox_3 = QGroupBox(self.tab1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.labelOutOfStock = QLabel(self.groupBox_3)
        self.labelOutOfStock.setObjectName(u"labelOutOfStock")
        self.labelOutOfStock.setEnabled(False)
        font1 = QFont()
        font1.setBold(True)
        self.labelOutOfStock.setFont(font1)

        self.horizontalLayout_13.addWidget(self.labelOutOfStock)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_13.addWidget(self.label_11)

        self.label_29 = QLabel(self.groupBox_3)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_29)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_13.addWidget(self.label_12)

        self.labelCritical = QLabel(self.groupBox_3)
        self.labelCritical.setObjectName(u"labelCritical")
        palette = QPalette()
        brush = QBrush(QColor(255, 38, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.labelCritical.setPalette(palette)
        self.labelCritical.setFont(font1)

        self.horizontalLayout_13.addWidget(self.labelCritical)

        self.label_33 = QLabel(self.groupBox_3)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_13.addWidget(self.label_33)

        self.spinBoxInventoryCriticalLevel = QDoubleSpinBox(self.groupBox_3)
        self.spinBoxInventoryCriticalLevel.setObjectName(u"spinBoxInventoryCriticalLevel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinBoxInventoryCriticalLevel.sizePolicy().hasHeightForWidth())
        self.spinBoxInventoryCriticalLevel.setSizePolicy(sizePolicy1)
        self.spinBoxInventoryCriticalLevel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.spinBoxInventoryCriticalLevel)

        self.label_27 = QLabel(self.groupBox_3)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_13.addWidget(self.label_27)

        self.labelWarning = QLabel(self.groupBox_3)
        self.labelWarning.setObjectName(u"labelWarning")
        palette1 = QPalette()
        brush1 = QBrush(QColor(255, 147, 0, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        self.labelWarning.setPalette(palette1)
        self.labelWarning.setFont(font1)

        self.horizontalLayout_13.addWidget(self.labelWarning)

        self.label_35 = QLabel(self.groupBox_3)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_13.addWidget(self.label_35)

        self.spinBoxInventoryWarningLevel = QDoubleSpinBox(self.groupBox_3)
        self.spinBoxInventoryWarningLevel.setObjectName(u"spinBoxInventoryWarningLevel")
        sizePolicy1.setHeightForWidth(self.spinBoxInventoryWarningLevel.sizePolicy().hasHeightForWidth())
        self.spinBoxInventoryWarningLevel.setSizePolicy(sizePolicy1)
        self.spinBoxInventoryWarningLevel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.spinBoxInventoryWarningLevel)

        self.label_28 = QLabel(self.groupBox_3)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_13.addWidget(self.label_28)

        self.labelAvailable = QLabel(self.groupBox_3)
        self.labelAvailable.setObjectName(u"labelAvailable")
        palette2 = QPalette()
        brush2 = QBrush(QColor(0, 153, 51, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.labelAvailable.setPalette(palette2)

        self.horizontalLayout_13.addWidget(self.labelAvailable)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)


        self.verticalLayout_24.addLayout(self.horizontalLayout_13)


        self.verticalLayout_27.addWidget(self.groupBox_3)

        self.groupBox_15 = QGroupBox(self.tab1)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.verticalLayout_26 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.checkBoxOrderProgress = QCheckBox(self.groupBox_15)
        self.checkBoxOrderProgress.setObjectName(u"checkBoxOrderProgress")

        self.verticalLayout_26.addWidget(self.checkBoxOrderProgress)


        self.verticalLayout_27.addWidget(self.groupBox_15)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_27.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        self.verticalLayout_5 = QVBoxLayout(self.tab2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.groupBox_7 = QGroupBox(self.tab2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.comboBoxOrderUI = QComboBox(self.groupBox_7)
        self.comboBoxOrderUI.setObjectName(u"comboBoxOrderUI")

        self.verticalLayout_3.addWidget(self.comboBoxOrderUI)


        self.horizontalLayout_8.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.comboBoxTabPosition = QComboBox(self.groupBox_8)
        self.comboBoxTabPosition.setObjectName(u"comboBoxTabPosition")

        self.verticalLayout_4.addWidget(self.comboBoxTabPosition)


        self.horizontalLayout_8.addWidget(self.groupBox_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBoxOrderGeometry = QGroupBox(self.tab2)
        self.groupBoxOrderGeometry.setObjectName(u"groupBoxOrderGeometry")
        sizePolicy1.setHeightForWidth(self.groupBoxOrderGeometry.sizePolicy().hasHeightForWidth())
        self.groupBoxOrderGeometry.setSizePolicy(sizePolicy1)
        self.verticalLayout_10 = QVBoxLayout(self.groupBoxOrderGeometry)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.spinBoxOrderListFontSize = QSpinBox(self.groupBoxOrderGeometry)
        self.spinBoxOrderListFontSize.setObjectName(u"spinBoxOrderListFontSize")
        self.spinBoxOrderListFontSize.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.spinBoxOrderListFontSize, 4, 1, 1, 1)

        self.spinBoxOrderListColumns = QSpinBox(self.groupBoxOrderGeometry)
        self.spinBoxOrderListColumns.setObjectName(u"spinBoxOrderListColumns")
        self.spinBoxOrderListColumns.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.spinBoxOrderListColumns, 1, 1, 1, 1)

        self.label_13 = QLabel(self.groupBoxOrderGeometry)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_2 = QLabel(self.groupBoxOrderGeometry)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.groupBoxOrderGeometry)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.spinBoxOrderListRows = QSpinBox(self.groupBoxOrderGeometry)
        self.spinBoxOrderListRows.setObjectName(u"spinBoxOrderListRows")
        self.spinBoxOrderListRows.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.spinBoxOrderListRows, 0, 1, 1, 1)

        self.spinBoxOrderListSpacing = QSpinBox(self.groupBoxOrderGeometry)
        self.spinBoxOrderListSpacing.setObjectName(u"spinBoxOrderListSpacing")
        self.spinBoxOrderListSpacing.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.spinBoxOrderListSpacing, 2, 1, 1, 1)

        self.label_17 = QLabel(self.groupBoxOrderGeometry)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 4, 0, 1, 1)

        self.label_15 = QLabel(self.groupBoxOrderGeometry)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 3, 0, 1, 1)

        self.fontComboBoxOrderList = QFontComboBox(self.groupBoxOrderGeometry)
        self.fontComboBoxOrderList.setObjectName(u"fontComboBoxOrderList")
        sizePolicy1.setHeightForWidth(self.fontComboBoxOrderList.sizePolicy().hasHeightForWidth())
        self.fontComboBoxOrderList.setSizePolicy(sizePolicy1)
        self.fontComboBoxOrderList.setEditable(False)

        self.gridLayout_5.addWidget(self.fontComboBoxOrderList, 3, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_5)


        self.horizontalLayout_3.addWidget(self.groupBoxOrderGeometry)

        self.groupBoxTableGeometry = QGroupBox(self.tab2)
        self.groupBoxTableGeometry.setObjectName(u"groupBoxTableGeometry")
        sizePolicy1.setHeightForWidth(self.groupBoxTableGeometry.sizePolicy().hasHeightForWidth())
        self.groupBoxTableGeometry.setSizePolicy(sizePolicy1)
        self.verticalLayout_11 = QVBoxLayout(self.groupBoxTableGeometry)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.label_16 = QLabel(self.groupBoxTableGeometry)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_6.addWidget(self.label_16, 3, 0, 1, 1)

        self.spinBoxTableListRows = QSpinBox(self.groupBoxTableGeometry)
        self.spinBoxTableListRows.setObjectName(u"spinBoxTableListRows")
        self.spinBoxTableListRows.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.spinBoxTableListRows, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBoxTableGeometry)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_14 = QLabel(self.groupBoxTableGeometry)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_5 = QLabel(self.groupBoxTableGeometry)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_6.addWidget(self.label_5, 1, 0, 1, 1)

        self.spinBoxTableListColumns = QSpinBox(self.groupBoxTableGeometry)
        self.spinBoxTableListColumns.setObjectName(u"spinBoxTableListColumns")
        self.spinBoxTableListColumns.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.spinBoxTableListColumns, 1, 1, 1, 1)

        self.spinBoxTableListSpacing = QSpinBox(self.groupBoxTableGeometry)
        self.spinBoxTableListSpacing.setObjectName(u"spinBoxTableListSpacing")
        self.spinBoxTableListSpacing.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.spinBoxTableListSpacing, 2, 1, 1, 1)

        self.fontComboBoxTableList = QFontComboBox(self.groupBoxTableGeometry)
        self.fontComboBoxTableList.setObjectName(u"fontComboBoxTableList")
        sizePolicy1.setHeightForWidth(self.fontComboBoxTableList.sizePolicy().hasHeightForWidth())
        self.fontComboBoxTableList.setSizePolicy(sizePolicy1)
        self.fontComboBoxTableList.setEditable(False)

        self.gridLayout_6.addWidget(self.fontComboBoxTableList, 3, 1, 1, 1)

        self.spinBoxTableListFontSize = QSpinBox(self.groupBoxTableGeometry)
        self.spinBoxTableListFontSize.setObjectName(u"spinBoxTableListFontSize")
        self.spinBoxTableListFontSize.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.spinBoxTableListFontSize, 4, 1, 1, 1)

        self.label_18 = QLabel(self.groupBoxTableGeometry)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 4, 0, 1, 1)


        self.verticalLayout_11.addLayout(self.gridLayout_6)


        self.horizontalLayout_3.addWidget(self.groupBoxTableGeometry)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.groupBox_2 = QGroupBox(self.tab2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.labelRed_2 = QLabel(self.groupBox_2)
        self.labelRed_2.setObjectName(u"labelRed_2")
        self.labelRed_2.setFont(font)
        self.labelRed_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.labelRed_2, 0, 1, 1, 1)

        self.labelYellow = QLabel(self.groupBox_2)
        self.labelYellow.setObjectName(u"labelYellow")
        self.labelYellow.setFont(font)
        self.labelYellow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.labelYellow, 0, 2, 1, 1)

        self.labelRed = QLabel(self.groupBox_2)
        self.labelRed.setObjectName(u"labelRed")
        self.labelRed.setFont(font)
        self.labelRed.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.labelRed, 0, 3, 1, 1)

        self.labelRed_3 = QLabel(self.groupBox_2)
        self.labelRed_3.setObjectName(u"labelRed_3")
        self.labelRed_3.setFont(font)
        self.labelRed_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.labelRed_3, 0, 4, 1, 1)

        self.labelYellow_3 = QLabel(self.groupBox_2)
        self.labelYellow_3.setObjectName(u"labelYellow_3")
        self.labelYellow_3.setFont(font)

        self.gridLayout_4.addWidget(self.labelYellow_3, 1, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_31 = QLabel(self.groupBox_2)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_10.addWidget(self.label_31)

        self.spinBoxWarningLevel = QDoubleSpinBox(self.groupBox_2)
        self.spinBoxWarningLevel.setObjectName(u"spinBoxWarningLevel")
        sizePolicy1.setHeightForWidth(self.spinBoxWarningLevel.sizePolicy().hasHeightForWidth())
        self.spinBoxWarningLevel.setSizePolicy(sizePolicy1)
        self.spinBoxWarningLevel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.spinBoxWarningLevel)


        self.gridLayout_4.addLayout(self.horizontalLayout_10, 1, 1, 1, 1)

        self.colorComboBoxWB = ColorComboBox(self.groupBox_2)
        self.colorComboBoxWB.setObjectName(u"colorComboBoxWB")

        self.gridLayout_4.addWidget(self.colorComboBoxWB, 1, 2, 1, 1)

        self.colorComboBoxWT = ColorComboBox(self.groupBox_2)
        self.colorComboBoxWT.setObjectName(u"colorComboBoxWT")

        self.gridLayout_4.addWidget(self.colorComboBoxWT, 1, 3, 1, 1)

        self.pushButtonExampleWL = ButtonItemExample(self.groupBox_2)
        self.pushButtonExampleWL.setObjectName(u"pushButtonExampleWL")

        self.gridLayout_4.addWidget(self.pushButtonExampleWL, 1, 4, 1, 1)

        self.labelYellow_4 = QLabel(self.groupBox_2)
        self.labelYellow_4.setObjectName(u"labelYellow_4")
        self.labelYellow_4.setFont(font)

        self.gridLayout_4.addWidget(self.labelYellow_4, 2, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_32 = QLabel(self.groupBox_2)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_11.addWidget(self.label_32)

        self.spinBoxCriticalLevel = QDoubleSpinBox(self.groupBox_2)
        self.spinBoxCriticalLevel.setObjectName(u"spinBoxCriticalLevel")
        sizePolicy1.setHeightForWidth(self.spinBoxCriticalLevel.sizePolicy().hasHeightForWidth())
        self.spinBoxCriticalLevel.setSizePolicy(sizePolicy1)
        self.spinBoxCriticalLevel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.spinBoxCriticalLevel)


        self.gridLayout_4.addLayout(self.horizontalLayout_11, 2, 1, 1, 1)

        self.colorComboBoxCB = ColorComboBox(self.groupBox_2)
        self.colorComboBoxCB.setObjectName(u"colorComboBoxCB")

        self.gridLayout_4.addWidget(self.colorComboBoxCB, 2, 2, 1, 1)

        self.colorComboBoxCT = ColorComboBox(self.groupBox_2)
        self.colorComboBoxCT.setObjectName(u"colorComboBoxCT")

        self.gridLayout_4.addWidget(self.colorComboBoxCT, 2, 3, 1, 1)

        self.pushButtonExampleCL = ButtonItemExample(self.groupBox_2)
        self.pushButtonExampleCL.setObjectName(u"pushButtonExampleCL")

        self.gridLayout_4.addWidget(self.pushButtonExampleCL, 2, 4, 1, 1)

        self.label_21 = QLabel(self.groupBox_2)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_4.addWidget(self.label_21, 3, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_12.addWidget(self.label_22)

        self.label_23 = QLabel(self.groupBox_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_23)


        self.gridLayout_4.addLayout(self.horizontalLayout_12, 3, 1, 1, 1)

        self.colorComboBoxDB = ColorComboBox(self.groupBox_2)
        self.colorComboBoxDB.setObjectName(u"colorComboBoxDB")

        self.gridLayout_4.addWidget(self.colorComboBoxDB, 3, 2, 1, 1)

        self.colorComboBoxDT = ColorComboBox(self.groupBox_2)
        self.colorComboBoxDT.setObjectName(u"colorComboBoxDT")

        self.gridLayout_4.addWidget(self.colorComboBoxDT, 3, 3, 1, 1)

        self.pushButtonExampleDL = ButtonItemExample(self.groupBox_2)
        self.pushButtonExampleDL.setObjectName(u"pushButtonExampleDL")

        self.gridLayout_4.addWidget(self.pushButtonExampleDL, 3, 4, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_4)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.verticalSpacer_4 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab2, "")
        self.tab3 = QWidget()
        self.tab3.setObjectName(u"tab3")
        self.verticalLayout_25 = QVBoxLayout(self.tab3)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox_6 = QGroupBox(self.tab3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.groupBox_6)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalSliderDinner = QSlider(self.groupBox_6)
        self.horizontalSliderDinner.setObjectName(u"horizontalSliderDinner")
        self.horizontalSliderDinner.setMaximum(24)
        self.horizontalSliderDinner.setPageStep(8)
        self.horizontalSliderDinner.setValue(18)
        self.horizontalSliderDinner.setSliderPosition(18)
        self.horizontalSliderDinner.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSliderDinner.setInvertedAppearance(False)
        self.horizontalSliderDinner.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horizontalSliderDinner.setTickInterval(1)

        self.gridLayout_3.addWidget(self.horizontalSliderDinner, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_6)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.spinBoxLunch = QSpinBox(self.groupBox_6)
        self.spinBoxLunch.setObjectName(u"spinBoxLunch")
        self.spinBoxLunch.setMaximum(24)
        self.spinBoxLunch.setValue(11)

        self.gridLayout_3.addWidget(self.spinBoxLunch, 0, 2, 1, 1)

        self.spinBoxDinner = QSpinBox(self.groupBox_6)
        self.spinBoxDinner.setObjectName(u"spinBoxDinner")
        self.spinBoxDinner.setMaximum(24)
        self.spinBoxDinner.setValue(18)

        self.gridLayout_3.addWidget(self.spinBoxDinner, 1, 2, 1, 1)

        self.horizontalSliderLunch = QSlider(self.groupBox_6)
        self.horizontalSliderLunch.setObjectName(u"horizontalSliderLunch")
        self.horizontalSliderLunch.setMaximum(24)
        self.horizontalSliderLunch.setPageStep(8)
        self.horizontalSliderLunch.setValue(11)
        self.horizontalSliderLunch.setTracking(True)
        self.horizontalSliderLunch.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalSliderLunch.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.horizontalSliderLunch.setTickInterval(1)

        self.gridLayout_3.addWidget(self.horizontalSliderLunch, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_3)


        self.gridLayout_9.addWidget(self.groupBox_6, 0, 0, 2, 1)

        self.groupBox_11 = QGroupBox(self.tab3)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.radioButtonTable = QRadioButton(self.groupBox_11)
        self.radioButtonTable.setObjectName(u"radioButtonTable")
        self.radioButtonTable.setChecked(True)

        self.horizontalLayout_15.addWidget(self.radioButtonTable)

        self.radioButtonTakeaway = QRadioButton(self.groupBox_11)
        self.radioButtonTakeaway.setObjectName(u"radioButtonTakeaway")

        self.horizontalLayout_15.addWidget(self.radioButtonTakeaway)


        self.verticalLayout_7.addLayout(self.horizontalLayout_15)


        self.gridLayout_9.addWidget(self.groupBox_11, 0, 1, 1, 1)

        self.groupBox_9 = QGroupBox(self.tab3)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButtonCash = QRadioButton(self.groupBox_9)
        self.radioButtonCash.setObjectName(u"radioButtonCash")
        self.radioButtonCash.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radioButtonCash)

        self.radioButtonElectronic = QRadioButton(self.groupBox_9)
        self.radioButtonElectronic.setObjectName(u"radioButtonElectronic")

        self.horizontalLayout_7.addWidget(self.radioButtonElectronic)


        self.verticalLayout_18.addLayout(self.horizontalLayout_7)


        self.gridLayout_9.addWidget(self.groupBox_9, 1, 1, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_9)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.groupBox_5 = QGroupBox(self.tab3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.checkBoxUseTableList = QCheckBox(self.groupBox_5)
        self.checkBoxUseTableList.setObjectName(u"checkBoxUseTableList")

        self.verticalLayout_8.addWidget(self.checkBoxUseTableList)

        self.checkBoxShowInventory = QCheckBox(self.groupBox_5)
        self.checkBoxShowInventory.setObjectName(u"checkBoxShowInventory")

        self.verticalLayout_8.addWidget(self.checkBoxShowInventory)

        self.checkBoxAutoVariants = QCheckBox(self.groupBox_5)
        self.checkBoxAutoVariants.setObjectName(u"checkBoxAutoVariants")

        self.verticalLayout_8.addWidget(self.checkBoxAutoVariants)

        self.checkBoxMandatoryTableNumber = QCheckBox(self.groupBox_5)
        self.checkBoxMandatoryTableNumber.setObjectName(u"checkBoxMandatoryTableNumber")

        self.verticalLayout_8.addWidget(self.checkBoxMandatoryTableNumber)

        self.checkBoxMandatoryName = QCheckBox(self.groupBox_5)
        self.checkBoxMandatoryName.setObjectName(u"checkBoxMandatoryName")

        self.verticalLayout_8.addWidget(self.checkBoxMandatoryName)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_5.addWidget(self.label_20)

        self.spinBoxMaxCovers = QSpinBox(self.groupBox_5)
        self.spinBoxMaxCovers.setObjectName(u"spinBoxMaxCovers")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinBoxMaxCovers.sizePolicy().hasHeightForWidth())
        self.spinBoxMaxCovers.setSizePolicy(sizePolicy2)
        self.spinBoxMaxCovers.setMinimum(0)
        self.spinBoxMaxCovers.setMaximum(999)
        self.spinBoxMaxCovers.setValue(0)

        self.horizontalLayout_5.addWidget(self.spinBoxMaxCovers)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_9.addWidget(self.groupBox_5)

        self.groupBox = QGroupBox(self.tab3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radioButtonEventBased = QRadioButton(self.groupBox)
        self.radioButtonEventBased.setObjectName(u"radioButtonEventBased")
        self.radioButtonEventBased.setChecked(True)

        self.horizontalLayout_6.addWidget(self.radioButtonEventBased)

        self.radioButtonDayBased = QRadioButton(self.groupBox)
        self.radioButtonDayBased.setObjectName(u"radioButtonDayBased")

        self.horizontalLayout_6.addWidget(self.radioButtonDayBased)

        self.radioButtonDayPartBased = QRadioButton(self.groupBox)
        self.radioButtonDayPartBased.setObjectName(u"radioButtonDayPartBased")

        self.horizontalLayout_6.addWidget(self.radioButtonDayPartBased)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.label_26)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_6)


        self.horizontalLayout_9.addWidget(self.groupBox)


        self.verticalLayout_25.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.groupBox_13 = QGroupBox(self.tab3)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.checkBoxMenuItemDescription = QCheckBox(self.groupBox_13)
        self.checkBoxMenuItemDescription.setObjectName(u"checkBoxMenuItemDescription")

        self.verticalLayout_23.addWidget(self.checkBoxMenuItemDescription)


        self.horizontalLayout_14.addWidget(self.groupBox_13)

        self.groupBox_12 = QGroupBox(self.tab3)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxInactivity = QCheckBox(self.groupBox_12)
        self.checkBoxInactivity.setObjectName(u"checkBoxInactivity")

        self.horizontalLayout.addWidget(self.checkBoxInactivity)

        self.spinBoxInactivityTime = QSpinBox(self.groupBox_12)
        self.spinBoxInactivityTime.setObjectName(u"spinBoxInactivityTime")
        self.spinBoxInactivityTime.setEnabled(False)
        self.spinBoxInactivityTime.setMinimum(30)
        self.spinBoxInactivityTime.setMaximum(1200)

        self.horizontalLayout.addWidget(self.spinBoxInactivityTime)

        self.labelInactivity = QLabel(self.groupBox_12)
        self.labelInactivity.setObjectName(u"labelInactivity")
        self.labelInactivity.setEnabled(False)

        self.horizontalLayout.addWidget(self.labelInactivity)


        self.verticalLayout_22.addLayout(self.horizontalLayout)


        self.horizontalLayout_14.addWidget(self.groupBox_12)


        self.verticalLayout_25.addLayout(self.horizontalLayout_14)

        self.verticalSpacer_5 = QSpacerItem(20, 130, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_5)

        self.tabWidget.addTab(self.tab3, "")
        self.tab4 = QWidget()
        self.tab4.setObjectName(u"tab4")
        self.verticalLayout_19 = QVBoxLayout(self.tab4)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.groupBox_4 = QGroupBox(self.tab4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelCopy_4 = QLabel(self.groupBox_4)
        self.labelCopy_4.setObjectName(u"labelCopy_4")

        self.gridLayout.addWidget(self.labelCopy_4, 0, 2, 1, 1)

        self.labelCopy = QLabel(self.groupBox_4)
        self.labelCopy.setObjectName(u"labelCopy")

        self.gridLayout.addWidget(self.labelCopy, 0, 1, 1, 1)

        self.labelCopy_3 = QLabel(self.groupBox_4)
        self.labelCopy_3.setObjectName(u"labelCopy_3")

        self.gridLayout.addWidget(self.labelCopy_3, 0, 3, 1, 1)

        self.labelCopy_2 = QLabel(self.groupBox_4)
        self.labelCopy_2.setObjectName(u"labelCopy_2")

        self.gridLayout.addWidget(self.labelCopy_2, 0, 0, 1, 1)

        self.comboBoxCustomerPrinter = RelationalComboBox(self.groupBox_4)
        self.comboBoxCustomerPrinter.setObjectName(u"comboBoxCustomerPrinter")
        self.comboBoxCustomerPrinter.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxCustomerPrinter.sizePolicy().hasHeightForWidth())
        self.comboBoxCustomerPrinter.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboBoxCustomerPrinter, 1, 3, 1, 1)

        self.spinBoxCustomerCopies = QSpinBox(self.groupBox_4)
        self.spinBoxCustomerCopies.setObjectName(u"spinBoxCustomerCopies")
        self.spinBoxCustomerCopies.setEnabled(False)
        self.spinBoxCustomerCopies.setMinimum(1)

        self.gridLayout.addWidget(self.spinBoxCustomerCopies, 1, 1, 1, 1)

        self.comboBoxCustomerReport = RelationalComboBox(self.groupBox_4)
        self.comboBoxCustomerReport.setObjectName(u"comboBoxCustomerReport")
        self.comboBoxCustomerReport.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxCustomerReport.sizePolicy().hasHeightForWidth())
        self.comboBoxCustomerReport.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboBoxCustomerReport, 1, 2, 1, 1)

        self.checkBoxCustomerCopy = QCheckBox(self.groupBox_4)
        self.checkBoxCustomerCopy.setObjectName(u"checkBoxCustomerCopy")
        self.checkBoxCustomerCopy.setChecked(False)

        self.gridLayout.addWidget(self.checkBoxCustomerCopy, 1, 0, 1, 1)

        self.spinBoxCoverCopies = QSpinBox(self.groupBox_4)
        self.spinBoxCoverCopies.setObjectName(u"spinBoxCoverCopies")
        self.spinBoxCoverCopies.setEnabled(False)
        self.spinBoxCoverCopies.setMinimum(1)

        self.gridLayout.addWidget(self.spinBoxCoverCopies, 7, 1, 1, 1)

        self.comboBoxCoverReport = RelationalComboBox(self.groupBox_4)
        self.comboBoxCoverReport.setObjectName(u"comboBoxCoverReport")
        self.comboBoxCoverReport.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxCoverReport.sizePolicy().hasHeightForWidth())
        self.comboBoxCoverReport.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboBoxCoverReport, 7, 2, 1, 1)

        self.comboBoxDepartmentReport = RelationalComboBox(self.groupBox_4)
        self.comboBoxDepartmentReport.setObjectName(u"comboBoxDepartmentReport")
        self.comboBoxDepartmentReport.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxDepartmentReport.sizePolicy().hasHeightForWidth())
        self.comboBoxDepartmentReport.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboBoxDepartmentReport, 3, 2, 1, 1)

        self.checkBoxDepartmentCopy = QCheckBox(self.groupBox_4)
        self.checkBoxDepartmentCopy.setObjectName(u"checkBoxDepartmentCopy")
        self.checkBoxDepartmentCopy.setChecked(False)

        self.gridLayout.addWidget(self.checkBoxDepartmentCopy, 3, 0, 1, 1)

        self.checkBoxCoverCopy = QCheckBox(self.groupBox_4)
        self.checkBoxCoverCopy.setObjectName(u"checkBoxCoverCopy")
        self.checkBoxCoverCopy.setChecked(False)

        self.gridLayout.addWidget(self.checkBoxCoverCopy, 7, 0, 1, 1)

        self.spinBoxDepartmentCopies = QSpinBox(self.groupBox_4)
        self.spinBoxDepartmentCopies.setObjectName(u"spinBoxDepartmentCopies")
        self.spinBoxDepartmentCopies.setEnabled(False)
        self.spinBoxDepartmentCopies.setMinimum(1)

        self.gridLayout.addWidget(self.spinBoxDepartmentCopies, 3, 1, 1, 1)

        self.comboBoxCoverPrinter = RelationalComboBox(self.groupBox_4)
        self.comboBoxCoverPrinter.setObjectName(u"comboBoxCoverPrinter")
        self.comboBoxCoverPrinter.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxCoverPrinter.sizePolicy().hasHeightForWidth())
        self.comboBoxCoverPrinter.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.comboBoxCoverPrinter, 7, 3, 1, 1)

        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_19.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(380, 289, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab4, "")
        self.tab5 = QWidget()
        self.tab5.setObjectName(u"tab5")
        self.verticalLayout_16 = QVBoxLayout(self.tab5)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.groupBoxAutomaticUpdate = QGroupBox(self.tab5)
        self.groupBoxAutomaticUpdate.setObjectName(u"groupBoxAutomaticUpdate")
        self.groupBoxAutomaticUpdate.setCheckable(True)
        self.groupBoxAutomaticUpdate.setChecked(False)
        self.verticalLayout_15 = QVBoxLayout(self.groupBoxAutomaticUpdate)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.groupBoxAutomaticUpdate)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.spinBoxAutomaticUpdateInterval = QSpinBox(self.groupBoxAutomaticUpdate)
        self.spinBoxAutomaticUpdateInterval.setObjectName(u"spinBoxAutomaticUpdateInterval")

        self.horizontalLayout_4.addWidget(self.spinBoxAutomaticUpdateInterval)

        self.label_19 = QLabel(self.groupBoxAutomaticUpdate)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.label_19)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_15.addLayout(self.horizontalLayout_4)


        self.verticalLayout_16.addWidget(self.groupBoxAutomaticUpdate)

        self.groupBoxOrderedDeliveredReport = QGroupBox(self.tab5)
        self.groupBoxOrderedDeliveredReport.setObjectName(u"groupBoxOrderedDeliveredReport")
        sizePolicy1.setHeightForWidth(self.groupBoxOrderedDeliveredReport.sizePolicy().hasHeightForWidth())
        self.groupBoxOrderedDeliveredReport.setSizePolicy(sizePolicy1)
        self.groupBoxOrderedDeliveredReport.setCheckable(True)
        self.groupBoxOrderedDeliveredReport.setChecked(False)
        self.verticalLayout_14 = QVBoxLayout(self.groupBoxOrderedDeliveredReport)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_10 = QLabel(self.groupBoxOrderedDeliveredReport)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.label_10, 0, 1, 1, 1)

        self.labelCopy_5 = QLabel(self.groupBoxOrderedDeliveredReport)
        self.labelCopy_5.setObjectName(u"labelCopy_5")
        sizePolicy1.setHeightForWidth(self.labelCopy_5.sizePolicy().hasHeightForWidth())
        self.labelCopy_5.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.labelCopy_5, 0, 0, 1, 1)

        self.comboBoxOrderedDeliveredReport = RelationalComboBox(self.groupBoxOrderedDeliveredReport)
        self.comboBoxOrderedDeliveredReport.setObjectName(u"comboBoxOrderedDeliveredReport")
        sizePolicy1.setHeightForWidth(self.comboBoxOrderedDeliveredReport.sizePolicy().hasHeightForWidth())
        self.comboBoxOrderedDeliveredReport.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.comboBoxOrderedDeliveredReport, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBoxOrderedDeliveredReport)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)

        self.comboBoxOrderedDeliveredPrinterClass = RelationalComboBox(self.groupBoxOrderedDeliveredReport)
        self.comboBoxOrderedDeliveredPrinterClass.setObjectName(u"comboBoxOrderedDeliveredPrinterClass")
        sizePolicy1.setHeightForWidth(self.comboBoxOrderedDeliveredPrinterClass.sizePolicy().hasHeightForWidth())
        self.comboBoxOrderedDeliveredPrinterClass.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.comboBoxOrderedDeliveredPrinterClass, 1, 2, 1, 1)

        self.spinBoxOrderedDeliveredCopies = QSpinBox(self.groupBoxOrderedDeliveredReport)
        self.spinBoxOrderedDeliveredCopies.setObjectName(u"spinBoxOrderedDeliveredCopies")
        self.spinBoxOrderedDeliveredCopies.setMinimum(1)

        self.gridLayout_2.addWidget(self.spinBoxOrderedDeliveredCopies, 1, 0, 1, 1)

        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)

        self.verticalLayout_12.addLayout(self.gridLayout_2)


        self.verticalLayout_14.addLayout(self.verticalLayout_12)


        self.verticalLayout_16.addWidget(self.groupBoxOrderedDeliveredReport)

        self.verticalSpacer_3 = QSpacerItem(20, 273, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab5, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_17.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_17.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label_24.setBuddy(self.spinBoxQuantityDecimals)
        self.label_25.setBuddy(self.lineEditCurrencySymbol)
        self.labelCopy_4.setBuddy(self.spinBoxCustomerCopies)
        self.labelCopy.setBuddy(self.spinBoxCustomerCopies)
        self.labelCopy_3.setBuddy(self.spinBoxCustomerCopies)
        self.labelCopy_2.setBuddy(self.spinBoxCustomerCopies)
        self.labelCopy_5.setBuddy(self.spinBoxCustomerCopies)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        self.checkBoxCustomerCopy.clicked["bool"].connect(self.spinBoxCustomerCopies.setEnabled)
        self.checkBoxCoverCopy.clicked["bool"].connect(self.spinBoxCoverCopies.setEnabled)
        self.checkBoxDepartmentCopy.clicked["bool"].connect(self.spinBoxDepartmentCopies.setEnabled)
        self.checkBoxCustomerCopy.clicked["bool"].connect(self.comboBoxCustomerReport.setEnabled)
        self.checkBoxCoverCopy.clicked["bool"].connect(self.comboBoxCoverReport.setEnabled)
        self.checkBoxCustomerCopy.clicked["bool"].connect(self.comboBoxCustomerPrinter.setEnabled)
        self.checkBoxCoverCopy.clicked["bool"].connect(self.comboBoxCoverPrinter.setEnabled)
        self.checkBoxDepartmentCopy.clicked["bool"].connect(self.comboBoxDepartmentReport.setEnabled)
        self.horizontalSliderLunch.valueChanged.connect(self.spinBoxLunch.setValue)
        self.horizontalSliderDinner.valueChanged.connect(self.spinBoxDinner.setValue)
        self.checkBoxInactivity.clicked["bool"].connect(self.spinBoxInactivityTime.setEnabled)
        self.checkBoxInactivity.clicked["bool"].connect(self.labelInactivity.setEnabled)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.labelIcon.setText(QCoreApplication.translate("SettingsDialog", u"Icon", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("SettingsDialog", u"Formats", None))
        self.label_24.setText(QCoreApplication.translate("SettingsDialog", u"Number of decimal places for the quantity", None))
        self.label_9.setText(QCoreApplication.translate("SettingsDialog", u"Number of decimal places for the price", None))
        self.label_30.setText(QCoreApplication.translate("SettingsDialog", u"Number of decimal places for the amount", None))
        self.label_25.setText(QCoreApplication.translate("SettingsDialog", u"Currency symbol", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("SettingsDialog", u"New item normal stock level colors", None))
        self.labelYellow_12.setText(QCoreApplication.translate("SettingsDialog", u"Background color", None))
        self.labelRed_9.setText(QCoreApplication.translate("SettingsDialog", u"Text color", None))
        self.labelRed_8.setText(QCoreApplication.translate("SettingsDialog", u"Example", None))
        self.pushButtonExampleNL.setText(QCoreApplication.translate("SettingsDialog", u"Normal", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SettingsDialog", u"Items inventory stock threshold levels", None))
        self.labelOutOfStock.setText(QCoreApplication.translate("SettingsDialog", u"Out of stock", None))
        self.label_11.setText(QCoreApplication.translate("SettingsDialog", u"=", None))
        self.label_29.setText(QCoreApplication.translate("SettingsDialog", u"0", None))
        self.label_12.setText(QCoreApplication.translate("SettingsDialog", u"<", None))
        self.labelCritical.setText(QCoreApplication.translate("SettingsDialog", u"Critical", None))
        self.label_33.setText(QCoreApplication.translate("SettingsDialog", u"<=", None))
        self.label_27.setText(QCoreApplication.translate("SettingsDialog", u"<", None))
        self.labelWarning.setText(QCoreApplication.translate("SettingsDialog", u"Warning", None))
        self.label_35.setText(QCoreApplication.translate("SettingsDialog", u"<=", None))
        self.label_28.setText(QCoreApplication.translate("SettingsDialog", u"<", None))
        self.labelAvailable.setText(QCoreApplication.translate("SettingsDialog", u"Available", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("SettingsDialog", u"Order progress", None))
        self.checkBoxOrderProgress.setText(QCoreApplication.translate("SettingsDialog", u"Order progress management (ordered delivered)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("SettingsDialog", u"Main", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("SettingsDialog", u"Order entry user interface", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("SettingsDialog", u"Department tab position", None))
        self.groupBoxOrderGeometry.setTitle(QCoreApplication.translate("SettingsDialog", u"Order list base geometry", None))
        self.label_13.setText(QCoreApplication.translate("SettingsDialog", u"Spacing", None))
        self.label_2.setText(QCoreApplication.translate("SettingsDialog", u"Columns", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Rows", None))
        self.label_17.setText(QCoreApplication.translate("SettingsDialog", u"Font size", None))
        self.label_15.setText(QCoreApplication.translate("SettingsDialog", u"Font", None))
        self.groupBoxTableGeometry.setTitle(QCoreApplication.translate("SettingsDialog", u"Table list base geometry", None))
        self.label_16.setText(QCoreApplication.translate("SettingsDialog", u"Font", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"Rows", None))
        self.label_14.setText(QCoreApplication.translate("SettingsDialog", u"Spacing", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"Columns", None))
        self.label_18.setText(QCoreApplication.translate("SettingsDialog", u"Font size", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"Visual alarm colors for stock level", None))
        self.labelRed_2.setText(QCoreApplication.translate("SettingsDialog", u"Stock level", None))
        self.labelYellow.setText(QCoreApplication.translate("SettingsDialog", u"Background color", None))
        self.labelRed.setText(QCoreApplication.translate("SettingsDialog", u"Text color", None))
        self.labelRed_3.setText(QCoreApplication.translate("SettingsDialog", u"Example", None))
        self.labelYellow_3.setText(QCoreApplication.translate("SettingsDialog", u"Warning", None))
        self.label_31.setText(QCoreApplication.translate("SettingsDialog", u"<=", None))
        self.pushButtonExampleWL.setText(QCoreApplication.translate("SettingsDialog", u"Warning", None))
        self.labelYellow_4.setText(QCoreApplication.translate("SettingsDialog", u"Critical", None))
        self.label_32.setText(QCoreApplication.translate("SettingsDialog", u"<=", None))
        self.pushButtonExampleCL.setText(QCoreApplication.translate("SettingsDialog", u"Critical", None))
        self.label_21.setText(QCoreApplication.translate("SettingsDialog", u"Out of stock", None))
        self.label_22.setText(QCoreApplication.translate("SettingsDialog", u"=", None))
        self.label_23.setText(QCoreApplication.translate("SettingsDialog", u"0", None))
        self.pushButtonExampleDL.setText(QCoreApplication.translate("SettingsDialog", u"Disabled", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("SettingsDialog", u"Order entry UI", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("SettingsDialog", u"Lunch / Dinner start time", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"Lunch", None))
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"Dinner", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("SettingsDialog", u"Default delivery", None))
        self.radioButtonTable.setText(QCoreApplication.translate("SettingsDialog", u"Table", None))
        self.radioButtonTakeaway.setText(QCoreApplication.translate("SettingsDialog", u"Takeaway", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("SettingsDialog", u"Default payment", None))
        self.radioButtonCash.setText(QCoreApplication.translate("SettingsDialog", u"Cash", None))
        self.radioButtonElectronic.setText(QCoreApplication.translate("SettingsDialog", u"Electronic", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SettingsDialog", u"Form parameters", None))
        self.checkBoxUseTableList.setText(QCoreApplication.translate("SettingsDialog", u"Use table list", None))
        self.checkBoxShowInventory.setText(QCoreApplication.translate("SettingsDialog", u"Always show inventory", None))
        self.checkBoxAutoVariants.setText(QCoreApplication.translate("SettingsDialog", u"Show variants automatically", None))
        self.checkBoxMandatoryTableNumber.setText(QCoreApplication.translate("SettingsDialog", u"Mandatory table number", None))
        self.checkBoxMandatoryName.setText(QCoreApplication.translate("SettingsDialog", u"Mandatory name for takeaway", None))
        self.label_20.setText(QCoreApplication.translate("SettingsDialog", u"Max covers value", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"Order number based on", None))
        self.radioButtonEventBased.setText(QCoreApplication.translate("SettingsDialog", u"Event", None))
        self.radioButtonDayBased.setText(QCoreApplication.translate("SettingsDialog", u"Day", None))
        self.radioButtonDayPartBased.setText(QCoreApplication.translate("SettingsDialog", u"Day part", None))
        self.label_26.setText(QCoreApplication.translate("SettingsDialog", u"Order number will restart from 1 on change Event/Day/Day part", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("SettingsDialog", u"Other parmeters", None))
        self.checkBoxMenuItemDescription.setText(QCoreApplication.translate("SettingsDialog", u"Menu description on menu items", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("SettingsDialog", u"Window inactivity", None))
        self.checkBoxInactivity.setText(QCoreApplication.translate("SettingsDialog", u"Check inactivity after", None))
        self.labelInactivity.setText(QCoreApplication.translate("SettingsDialog", u"Seconds", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), QCoreApplication.translate("SettingsDialog", u"Order entry control", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SettingsDialog", u"Order printing settings", None))
        self.labelCopy_4.setText(QCoreApplication.translate("SettingsDialog", u"Report", None))
        self.labelCopy.setText(QCoreApplication.translate("SettingsDialog", u"# Copies", None))
        self.labelCopy_3.setText(QCoreApplication.translate("SettingsDialog", u"Printer class", None))
        self.labelCopy_2.setText(QCoreApplication.translate("SettingsDialog", u"Print", None))
        self.checkBoxCustomerCopy.setText(QCoreApplication.translate("SettingsDialog", u"Customer", None))
        self.checkBoxDepartmentCopy.setText(QCoreApplication.translate("SettingsDialog", u"Department", None))
        self.checkBoxCoverCopy.setText(QCoreApplication.translate("SettingsDialog", u"Cover", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab4), QCoreApplication.translate("SettingsDialog", u"Order print", None))
        self.groupBoxAutomaticUpdate.setTitle(QCoreApplication.translate("SettingsDialog", u"Ordered delivered automatic update", None))
        self.label_7.setText(QCoreApplication.translate("SettingsDialog", u"Update view after", None))
        self.label_19.setText(QCoreApplication.translate("SettingsDialog", u"seconds", None))
        self.groupBoxOrderedDeliveredReport.setTitle(QCoreApplication.translate("SettingsDialog", u"Print ordered delivered report", None))
        self.label_10.setText(QCoreApplication.translate("SettingsDialog", u"Report", None))
        self.labelCopy_5.setText(QCoreApplication.translate("SettingsDialog", u"# Copies", None))
        self.label_8.setText(QCoreApplication.translate("SettingsDialog", u"Printer class", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab5), QCoreApplication.translate("SettingsDialog", u"Control report and view", None))
    # retranslateUi

