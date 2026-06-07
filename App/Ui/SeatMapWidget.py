# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SeatMapWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.Control import (ButtonColor, ButtonItemExample)
from App.Widget.View import EnhancedTableView

class Ui_SeatMapWidget(object):
    def setupUi(self, SeatMapWidget):
        if not SeatMapWidget.objectName():
            SeatMapWidget.setObjectName(u"SeatMapWidget")
        SeatMapWidget.resize(734, 607)
        font = QFont()
        font.setKerning(True)
        SeatMapWidget.setFont(font)
        self.verticalLayout_11 = QVBoxLayout(SeatMapWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.stackedWidget = QStackedWidget(SeatMapWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageList = QWidget()
        self.pageList.setObjectName(u"pageList")
        self.verticalLayout_13 = QVBoxLayout(self.pageList)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.tableView = EnhancedTableView(self.pageList)
        self.tableView.setObjectName(u"tableView")

        self.horizontalLayout_11.addWidget(self.tableView)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBoxTablePosition = QGroupBox(self.pageList)
        self.groupBoxTablePosition.setObjectName(u"groupBoxTablePosition")
        self.verticalLayout_9 = QVBoxLayout(self.groupBoxTablePosition)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.label_6 = QLabel(self.groupBoxTablePosition)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_7.addWidget(self.label_6)

        self.spinBoxStartRow = QSpinBox(self.groupBoxTablePosition)
        self.spinBoxStartRow.setObjectName(u"spinBoxStartRow")
        self.spinBoxStartRow.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxStartRow.setMinimum(1)
        self.spinBoxStartRow.setMaximum(999)
        self.spinBoxStartRow.setValue(1)

        self.horizontalLayout_7.addWidget(self.spinBoxStartRow)

        self.label_7 = QLabel(self.groupBoxTablePosition)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.spinBoxNumRows = QSpinBox(self.groupBoxTablePosition)
        self.spinBoxNumRows.setObjectName(u"spinBoxNumRows")
        self.spinBoxNumRows.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxNumRows.setMinimum(1)
        self.spinBoxNumRows.setMaximum(999)
        self.spinBoxNumRows.setValue(1)

        self.horizontalLayout_7.addWidget(self.spinBoxNumRows)

        self.label_8 = QLabel(self.groupBoxTablePosition)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_7.addWidget(self.label_8)

        self.spinBoxNumColumns = QSpinBox(self.groupBoxTablePosition)
        self.spinBoxNumColumns.setObjectName(u"spinBoxNumColumns")
        self.spinBoxNumColumns.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxNumColumns.setMinimum(1)
        self.spinBoxNumColumns.setMaximum(999)
        self.spinBoxNumColumns.setValue(1)

        self.horizontalLayout_7.addWidget(self.spinBoxNumColumns)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)


        self.verticalLayout_10.addWidget(self.groupBoxTablePosition)

        self.groupBoxTableCode = QGroupBox(self.pageList)
        self.groupBoxTableCode.setObjectName(u"groupBoxTableCode")
        self.verticalLayout_8 = QVBoxLayout(self.groupBoxTableCode)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButtonRowColumn = QRadioButton(self.groupBoxTableCode)
        self.radioButtonRowColumn.setObjectName(u"radioButtonRowColumn")
        self.radioButtonRowColumn.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioButtonRowColumn)

        self.radioButtonColumnRow = QRadioButton(self.groupBoxTableCode)
        self.radioButtonColumnRow.setObjectName(u"radioButtonColumnRow")

        self.verticalLayout_2.addWidget(self.radioButtonColumnRow)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_9 = QLabel(self.groupBoxTableCode)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_10 = QLabel(self.groupBoxTableCode)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.label_11 = QLabel(self.groupBoxTableCode)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_12 = QLabel(self.groupBoxTableCode)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 0, 3, 1, 1)

        self.lineEditPrefix = QLineEdit(self.groupBoxTableCode)
        self.lineEditPrefix.setObjectName(u"lineEditPrefix")
        self.lineEditPrefix.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.lineEditPrefix, 1, 0, 1, 1)

        self.spinBoxRowPadding = QSpinBox(self.groupBoxTableCode)
        self.spinBoxRowPadding.setObjectName(u"spinBoxRowPadding")
        self.spinBoxRowPadding.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxRowPadding.setMaximum(15)

        self.gridLayout.addWidget(self.spinBoxRowPadding, 1, 1, 1, 1)

        self.spinBoxColumnPadding = QSpinBox(self.groupBoxTableCode)
        self.spinBoxColumnPadding.setObjectName(u"spinBoxColumnPadding")
        self.spinBoxColumnPadding.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxColumnPadding.setMaximum(99999)

        self.gridLayout.addWidget(self.spinBoxColumnPadding, 1, 2, 1, 1)

        self.lineEditSuffix = QLineEdit(self.groupBoxTableCode)
        self.lineEditSuffix.setObjectName(u"lineEditSuffix")

        self.gridLayout.addWidget(self.lineEditSuffix, 1, 3, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)


        self.verticalLayout_10.addWidget(self.groupBoxTableCode)

        self.groupBoxButtonColor = QGroupBox(self.pageList)
        self.groupBoxButtonColor.setObjectName(u"groupBoxButtonColor")
        self.verticalLayout = QVBoxLayout(self.groupBoxButtonColor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonChooseBackground = QPushButton(self.groupBoxButtonColor)
        self.pushButtonChooseBackground.setObjectName(u"pushButtonChooseBackground")

        self.horizontalLayout_5.addWidget(self.pushButtonChooseBackground)

        self.pushButtonExample = ButtonItemExample(self.groupBoxButtonColor)
        self.pushButtonExample.setObjectName(u"pushButtonExample")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonExample.sizePolicy().hasHeightForWidth())
        self.pushButtonExample.setSizePolicy(sizePolicy)
        self.pushButtonExample.setMinimumSize(QSize(0, 30))
        self.pushButtonExample.setBaseSize(QSize(0, 0))

        self.horizontalLayout_5.addWidget(self.pushButtonExample)

        self.pushButtonChooseText = QPushButton(self.groupBoxButtonColor)
        self.pushButtonChooseText.setObjectName(u"pushButtonChooseText")

        self.horizontalLayout_5.addWidget(self.pushButtonChooseText)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.checkBoxChangeBackgroundColor = QCheckBox(self.groupBoxButtonColor)
        self.checkBoxChangeBackgroundColor.setObjectName(u"checkBoxChangeBackgroundColor")

        self.verticalLayout.addWidget(self.checkBoxChangeBackgroundColor)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButtonBGC4 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC4.setObjectName(u"pushButtonBGC4")
        self.pushButtonBGC4.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC4, 0, 3, 1, 1)

        self.pushButtonBGC5 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC5.setObjectName(u"pushButtonBGC5")
        self.pushButtonBGC5.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC5, 0, 4, 1, 1)

        self.pushButtonBGC2 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC2.setObjectName(u"pushButtonBGC2")
        self.pushButtonBGC2.setCheckable(False)
        self.pushButtonBGC2.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC2, 0, 1, 1, 1)

        self.pushButtonBGC3 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC3.setObjectName(u"pushButtonBGC3")
        self.pushButtonBGC3.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC3, 0, 2, 1, 1)

        self.pushButtonBGC1 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC1.setObjectName(u"pushButtonBGC1")
        self.pushButtonBGC1.setEnabled(True)
        self.pushButtonBGC1.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC1, 0, 0, 1, 1)

        self.pushButtonBGC6 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC6.setObjectName(u"pushButtonBGC6")
        self.pushButtonBGC6.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC6, 1, 0, 1, 1)

        self.pushButtonBGC8 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC8.setObjectName(u"pushButtonBGC8")
        self.pushButtonBGC8.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC8, 1, 2, 1, 1)

        self.pushButtonBGC7 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC7.setObjectName(u"pushButtonBGC7")
        self.pushButtonBGC7.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC7, 1, 1, 1, 1)

        self.pushButtonBGC9 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC9.setObjectName(u"pushButtonBGC9")
        self.pushButtonBGC9.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC9, 1, 3, 1, 1)

        self.pushButtonBGC10 = ButtonColor(self.groupBoxButtonColor)
        self.pushButtonBGC10.setObjectName(u"pushButtonBGC10")
        self.pushButtonBGC10.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC10, 1, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pushButtonGenerateTables = QPushButton(self.groupBoxButtonColor)
        self.pushButtonGenerateTables.setObjectName(u"pushButtonGenerateTables")

        self.horizontalLayout_10.addWidget(self.pushButtonGenerateTables)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_10)


        self.verticalLayout_10.addWidget(self.groupBoxButtonColor)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.pushButtonDeleteAll = QPushButton(self.pageList)
        self.pushButtonDeleteAll.setObjectName(u"pushButtonDeleteAll")
        self.pushButtonDeleteAll.setStyleSheet(u"")

        self.horizontalLayout_8.addWidget(self.pushButtonDeleteAll)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)


        self.horizontalLayout_11.addLayout(self.verticalLayout_10)


        self.verticalLayout_12.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButtonPreview = QPushButton(self.pageList)
        self.pushButtonPreview.setObjectName(u"pushButtonPreview")

        self.horizontalLayout_9.addWidget(self.pushButtonPreview)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_12.addLayout(self.horizontalLayout_9)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)

        self.stackedWidget.addWidget(self.pageList)
        self.pagePreview = QWidget()
        self.pagePreview.setObjectName(u"pagePreview")
        self.verticalLayout_4 = QVBoxLayout(self.pagePreview)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = QScrollArea(self.pagePreview)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 684, 492))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.framePreview = QFrame(self.scrollAreaWidgetContents)
        self.framePreview.setObjectName(u"framePreview")
        self.framePreview.setFrameShape(QFrame.Shape.StyledPanel)
        self.framePreview.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.framePreview)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayoutPreview = QGridLayout()
        self.gridLayoutPreview.setObjectName(u"gridLayoutPreview")
        self.gridLayoutPreview.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.verticalLayout_6.addLayout(self.gridLayoutPreview)


        self.verticalLayout_7.addWidget(self.framePreview)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonEdit = QPushButton(self.pagePreview)
        self.pushButtonEdit.setObjectName(u"pushButtonEdit")
        self.pushButtonEdit.setCheckable(False)

        self.horizontalLayout_4.addWidget(self.pushButtonEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.groupBoxBaseGeometry = QGroupBox(self.pagePreview)
        self.groupBoxBaseGeometry.setObjectName(u"groupBoxBaseGeometry")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxBaseGeometry)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBoxBaseGeometry)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBoxRows = QSpinBox(self.groupBoxBaseGeometry)
        self.spinBoxRows.setObjectName(u"spinBoxRows")
        self.spinBoxRows.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxRows)

        self.label_2 = QLabel(self.groupBoxBaseGeometry)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBoxColumns = QSpinBox(self.groupBoxBaseGeometry)
        self.spinBoxColumns.setObjectName(u"spinBoxColumns")
        self.spinBoxColumns.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxColumns)

        self.label_3 = QLabel(self.groupBoxBaseGeometry)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBoxSpacing = QSpinBox(self.groupBoxBaseGeometry)
        self.spinBoxSpacing.setObjectName(u"spinBoxSpacing")
        self.spinBoxSpacing.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.spinBoxSpacing)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.horizontalLayout_4.addWidget(self.groupBoxBaseGeometry)

        self.groupBoxMinimunSize = QGroupBox(self.pagePreview)
        self.groupBoxMinimunSize.setObjectName(u"groupBoxMinimunSize")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxMinimunSize)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.groupBoxMinimunSize)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.spinBoxMinWidth = QSpinBox(self.groupBoxMinimunSize)
        self.spinBoxMinWidth.setObjectName(u"spinBoxMinWidth")
        self.spinBoxMinWidth.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxMinWidth.setMinimum(30)
        self.spinBoxMinWidth.setMaximum(300)

        self.horizontalLayout_3.addWidget(self.spinBoxMinWidth)

        self.label_5 = QLabel(self.groupBoxMinimunSize)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.spinBoxMinHeight = QSpinBox(self.groupBoxMinimunSize)
        self.spinBoxMinHeight.setObjectName(u"spinBoxMinHeight")
        self.spinBoxMinHeight.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinBoxMinHeight.setMinimum(30)
        self.spinBoxMinHeight.setMaximum(300)

        self.horizontalLayout_3.addWidget(self.spinBoxMinHeight)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addWidget(self.groupBoxMinimunSize)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.stackedWidget.addWidget(self.pagePreview)

        self.verticalLayout_11.addWidget(self.stackedWidget)


        self.retranslateUi(SeatMapWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SeatMapWidget)
    # setupUi

    def retranslateUi(self, SeatMapWidget):
        SeatMapWidget.setWindowTitle(QCoreApplication.translate("SeatMapWidget", u"Seat Map", None))
        self.groupBoxTablePosition.setTitle(QCoreApplication.translate("SeatMapWidget", u"Table position and number", None))
        self.label_6.setText(QCoreApplication.translate("SeatMapWidget", u"Start row", None))
        self.label_7.setText(QCoreApplication.translate("SeatMapWidget", u"Rows", None))
        self.label_8.setText(QCoreApplication.translate("SeatMapWidget", u"Columns", None))
        self.groupBoxTableCode.setTitle(QCoreApplication.translate("SeatMapWidget", u"Table code", None))
        self.radioButtonRowColumn.setText(QCoreApplication.translate("SeatMapWidget", u"row + column", None))
        self.radioButtonColumnRow.setText(QCoreApplication.translate("SeatMapWidget", u"column + row", None))
        self.label_9.setText(QCoreApplication.translate("SeatMapWidget", u"Pefix", None))
        self.label_10.setText(QCoreApplication.translate("SeatMapWidget", u"Row padding", None))
        self.label_11.setText(QCoreApplication.translate("SeatMapWidget", u"Column padding", None))
        self.label_12.setText(QCoreApplication.translate("SeatMapWidget", u"Suffix", None))
        self.groupBoxButtonColor.setTitle(QCoreApplication.translate("SeatMapWidget", u"Button color", None))
        self.pushButtonChooseBackground.setText(QCoreApplication.translate("SeatMapWidget", u"Background color ...", None))
        self.pushButtonExample.setText(QCoreApplication.translate("SeatMapWidget", u"Example", None))
        self.pushButtonChooseText.setText(QCoreApplication.translate("SeatMapWidget", u"Text color ...", None))
        self.checkBoxChangeBackgroundColor.setText(QCoreApplication.translate("SeatMapWidget", u"Change background color on change row/column", None))
        self.pushButtonBGC4.setText("")
        self.pushButtonBGC5.setText("")
        self.pushButtonBGC2.setText("")
        self.pushButtonBGC3.setText("")
        self.pushButtonBGC1.setText("")
        self.pushButtonBGC6.setText("")
        self.pushButtonBGC8.setText("")
        self.pushButtonBGC7.setText("")
        self.pushButtonBGC9.setText("")
        self.pushButtonBGC10.setText("")
        self.pushButtonGenerateTables.setText(QCoreApplication.translate("SeatMapWidget", u"Generate table numbers", None))
        self.pushButtonDeleteAll.setText(QCoreApplication.translate("SeatMapWidget", u"Delete All", None))
        self.pushButtonPreview.setText(QCoreApplication.translate("SeatMapWidget", u"Preview", None))
        self.pushButtonEdit.setText(QCoreApplication.translate("SeatMapWidget", u"Edit", None))
        self.groupBoxBaseGeometry.setTitle(QCoreApplication.translate("SeatMapWidget", u"Base geometry", None))
        self.label.setText(QCoreApplication.translate("SeatMapWidget", u"Rows", None))
        self.label_2.setText(QCoreApplication.translate("SeatMapWidget", u"Columns", None))
        self.label_3.setText(QCoreApplication.translate("SeatMapWidget", u"Spacing", None))
        self.groupBoxMinimunSize.setTitle(QCoreApplication.translate("SeatMapWidget", u"Minimum size", None))
        self.label_4.setText(QCoreApplication.translate("SeatMapWidget", u"Width", None))
        self.label_5.setText(QCoreApplication.translate("SeatMapWidget", u"Height", None))
    # retranslateUi

