# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrintDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox
import resources_rc

class Ui_PrintDialog(object):
    def setupUi(self, PrintDialog):
        if not PrintDialog.objectName():
            PrintDialog.setObjectName(u"PrintDialog")
        PrintDialog.resize(640, 480)
        self.verticalLayout_14 = QVBoxLayout(PrintDialog)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButtonPrintPreview = QToolButton(PrintDialog)
        self.toolButtonPrintPreview.setObjectName(u"toolButtonPrintPreview")
        self.toolButtonPrintPreview.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonPrintPreview)

        self.toolButtonPrint = QToolButton(PrintDialog)
        self.toolButtonPrint.setObjectName(u"toolButtonPrint")
        self.toolButtonPrint.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonPrint)

        self.toolButtonPrintDirect = QToolButton(PrintDialog)
        self.toolButtonPrintDirect.setObjectName(u"toolButtonPrintDirect")
        self.toolButtonPrintDirect.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonPrintDirect)

        self.toolButtonPrintPDF = QToolButton(PrintDialog)
        self.toolButtonPrintPDF.setObjectName(u"toolButtonPrintPDF")
        self.toolButtonPrintPDF.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.toolButtonPrintPDF)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_14.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.comboBoxReportCustomizations = QComboBox(PrintDialog)
        self.comboBoxReportCustomizations.setObjectName(u"comboBoxReportCustomizations")

        self.horizontalLayout_7.addWidget(self.comboBoxReportCustomizations)

        self.label_3 = QLabel(PrintDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.comboBoxReportList = QComboBox(PrintDialog)
        self.comboBoxReportList.setObjectName(u"comboBoxReportList")

        self.horizontalLayout_7.addWidget(self.comboBoxReportList)

        self.horizontalLayout_7.setStretch(0, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout_7)

        self.tabWidget = QTabWidget(PrintDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabParameters = QWidget()
        self.tabParameters.setObjectName(u"tabParameters")
        self.verticalLayout_6 = QVBoxLayout(self.tabParameters)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.scrollAreaParameters = QScrollArea(self.tabParameters)
        self.scrollAreaParameters.setObjectName(u"scrollAreaParameters")
        self.scrollAreaParameters.setWidgetResizable(True)
        self.scrollAreaWidgetContentsParameters = QWidget()
        self.scrollAreaWidgetContentsParameters.setObjectName(u"scrollAreaWidgetContentsParameters")
        self.scrollAreaWidgetContentsParameters.setGeometry(QRect(0, 0, 596, 303))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContentsParameters)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.layoutParameters = QGridLayout()
        self.layoutParameters.setObjectName(u"layoutParameters")
        self.layoutParameters.setHorizontalSpacing(12)
        self.layoutParameters.setVerticalSpacing(6)
        self.layoutParameters.setContentsMargins(6, 6, 6, 6)

        self.verticalLayout_3.addLayout(self.layoutParameters)

        self.scrollAreaParameters.setWidget(self.scrollAreaWidgetContentsParameters)

        self.verticalLayout_6.addWidget(self.scrollAreaParameters)

        self.tabWidget.addTab(self.tabParameters, "")
        self.tabFilters = QWidget()
        self.tabFilters.setObjectName(u"tabFilters")
        self.verticalLayout_7 = QVBoxLayout(self.tabFilters)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.scrollAreaFilters = QScrollArea(self.tabFilters)
        self.scrollAreaFilters.setObjectName(u"scrollAreaFilters")
        self.scrollAreaFilters.setWidgetResizable(True)
        self.scrollAreaWidgetContentsFilters = QWidget()
        self.scrollAreaWidgetContentsFilters.setObjectName(u"scrollAreaWidgetContentsFilters")
        self.scrollAreaWidgetContentsFilters.setGeometry(QRect(0, 0, 596, 303))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContentsFilters)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.layoutFilters = QGridLayout()
        self.layoutFilters.setObjectName(u"layoutFilters")
        self.layoutFilters.setHorizontalSpacing(12)
        self.layoutFilters.setVerticalSpacing(6)
        self.layoutFilters.setContentsMargins(6, 6, 6, 6)

        self.verticalLayout_5.addLayout(self.layoutFilters)

        self.scrollAreaFilters.setWidget(self.scrollAreaWidgetContentsFilters)

        self.verticalLayout_7.addWidget(self.scrollAreaFilters)

        self.tabWidget.addTab(self.tabFilters, "")
        self.tabSorting = QWidget()
        self.tabSorting.setObjectName(u"tabSorting")
        self.verticalLayout_8 = QVBoxLayout(self.tabSorting)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(6, 6, 6, 6)
        self.scrollAreaSorting = QScrollArea(self.tabSorting)
        self.scrollAreaSorting.setObjectName(u"scrollAreaSorting")
        self.scrollAreaSorting.setWidgetResizable(True)
        self.scrollAreaWidgetContentsSorting = QWidget()
        self.scrollAreaWidgetContentsSorting.setObjectName(u"scrollAreaWidgetContentsSorting")
        self.scrollAreaWidgetContentsSorting.setGeometry(QRect(0, 0, 596, 303))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContentsSorting)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.layoutSorting = QGridLayout()
        self.layoutSorting.setObjectName(u"layoutSorting")
        self.layoutSorting.setHorizontalSpacing(12)
        self.layoutSorting.setVerticalSpacing(6)
        self.layoutSorting.setContentsMargins(6, 6, 6, 6)

        self.verticalLayout_4.addLayout(self.layoutSorting)

        self.scrollAreaSorting.setWidget(self.scrollAreaWidgetContentsSorting)

        self.verticalLayout_8.addWidget(self.scrollAreaSorting)

        self.tabWidget.addTab(self.tabSorting, "")
        self.tabPintOptions = QWidget()
        self.tabPintOptions.setObjectName(u"tabPintOptions")
        self.verticalLayout_9 = QVBoxLayout(self.tabPintOptions)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.scrollAreaPrintOptions = QScrollArea(self.tabPintOptions)
        self.scrollAreaPrintOptions.setObjectName(u"scrollAreaPrintOptions")
        self.scrollAreaPrintOptions.setWidgetResizable(True)
        self.scrollAreaWidgetContentsOptions = QWidget()
        self.scrollAreaWidgetContentsOptions.setObjectName(u"scrollAreaWidgetContentsOptions")
        self.scrollAreaWidgetContentsOptions.setGeometry(QRect(0, 0, 588, 283))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContentsOptions)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.groupBoxPrint = QGroupBox(self.scrollAreaWidgetContentsOptions)
        self.groupBoxPrint.setObjectName(u"groupBoxPrint")
        self.verticalLayout_11 = QVBoxLayout(self.groupBoxPrint)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelDirectPrint = QLabel(self.groupBoxPrint)
        self.labelDirectPrint.setObjectName(u"labelDirectPrint")

        self.horizontalLayout_4.addWidget(self.labelDirectPrint)

        self.comboBoxPrinters = QComboBox(self.groupBoxPrint)
        self.comboBoxPrinters.setObjectName(u"comboBoxPrinters")

        self.horizontalLayout_4.addWidget(self.comboBoxPrinters)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_11.addLayout(self.verticalLayout_2)


        self.verticalLayout_18.addWidget(self.groupBoxPrint)

        self.groupBoxPDFExport = QGroupBox(self.scrollAreaWidgetContentsOptions)
        self.groupBoxPDFExport.setObjectName(u"groupBoxPDFExport")
        self.verticalLayout_13 = QVBoxLayout(self.groupBoxPDFExport)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(self.groupBoxPDFExport)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.lineEditDirectory = QLineEdit(self.groupBoxPDFExport)
        self.lineEditDirectory.setObjectName(u"lineEditDirectory")

        self.gridLayout.addWidget(self.lineEditDirectory, 0, 1, 1, 1)

        self.pushButtonSelectDirectory = QPushButton(self.groupBoxPDFExport)
        self.pushButtonSelectDirectory.setObjectName(u"pushButtonSelectDirectory")

        self.gridLayout.addWidget(self.pushButtonSelectDirectory, 0, 2, 1, 1)

        self.label_7 = QLabel(self.groupBoxPDFExport)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.lineEditFileName = QLineEdit(self.groupBoxPDFExport)
        self.lineEditFileName.setObjectName(u"lineEditFileName")

        self.gridLayout.addWidget(self.lineEditFileName, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBoxPDFExport)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)


        self.verticalLayout_13.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBoxOpenPDF = QCheckBox(self.groupBoxPDFExport)
        self.checkBoxOpenPDF.setObjectName(u"checkBoxOpenPDF")

        self.horizontalLayout_2.addWidget(self.checkBoxOpenPDF)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_4 = QLabel(self.groupBoxPDFExport)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.comboBoxPDFVersion = RelationalComboBox(self.groupBoxPDFExport)
        self.comboBoxPDFVersion.setObjectName(u"comboBoxPDFVersion")

        self.horizontalLayout_2.addWidget(self.comboBoxPDFVersion)

        self.label_5 = QLabel(self.groupBoxPDFExport)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.spinBoxResolution = QSpinBox(self.groupBoxPDFExport)
        self.spinBoxResolution.setObjectName(u"spinBoxResolution")
        self.spinBoxResolution.setMinimum(20)
        self.spinBoxResolution.setMaximum(300)
        self.spinBoxResolution.setValue(96)

        self.horizontalLayout_2.addWidget(self.spinBoxResolution)

        self.label_9 = QLabel(self.groupBoxPDFExport)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_2.addWidget(self.label_9)


        self.verticalLayout_13.addLayout(self.horizontalLayout_2)


        self.verticalLayout_18.addWidget(self.groupBoxPDFExport)

        self.verticalSpacer_3 = QSpacerItem(20, 68, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_3)

        self.scrollAreaPrintOptions.setWidget(self.scrollAreaWidgetContentsOptions)

        self.verticalLayout_9.addWidget(self.scrollAreaPrintOptions)

        self.tabWidget.addTab(self.tabPintOptions, "")
        self.tabCustomize = QWidget()
        self.tabCustomize.setObjectName(u"tabCustomize")
        self.verticalLayout_15 = QVBoxLayout(self.tabCustomize)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.scrollAreaCustomize = QScrollArea(self.tabCustomize)
        self.scrollAreaCustomize.setObjectName(u"scrollAreaCustomize")
        self.scrollAreaCustomize.setWidgetResizable(True)
        self.scrollAreaWidgetContentsCustomize = QWidget()
        self.scrollAreaWidgetContentsCustomize.setObjectName(u"scrollAreaWidgetContentsCustomize")
        self.scrollAreaWidgetContentsCustomize.setGeometry(QRect(0, 0, 568, 400))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContentsCustomize)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBoxCurrent = QGroupBox(self.scrollAreaWidgetContentsCustomize)
        self.groupBoxCurrent.setObjectName(u"groupBoxCurrent")
        self.verticalLayout_17 = QVBoxLayout(self.groupBoxCurrent)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonUpdate = QPushButton(self.groupBoxCurrent)
        self.pushButtonUpdate.setObjectName(u"pushButtonUpdate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUpdate.sizePolicy().hasHeightForWidth())
        self.pushButtonUpdate.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButtonUpdate)

        self.pushButtonDelete = QPushButton(self.groupBoxCurrent)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")
        sizePolicy.setHeightForWidth(self.pushButtonDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonDelete.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButtonDelete)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.pushButtonSetSorting = QPushButton(self.groupBoxCurrent)
        self.pushButtonSetSorting.setObjectName(u"pushButtonSetSorting")

        self.horizontalLayout_3.addWidget(self.pushButtonSetSorting)

        self.spinBoxClassSorting = QSpinBox(self.groupBoxCurrent)
        self.spinBoxClassSorting.setObjectName(u"spinBoxClassSorting")

        self.horizontalLayout_3.addWidget(self.spinBoxClassSorting)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_3)


        self.verticalLayout_17.addLayout(self.verticalLayout_10)


        self.verticalLayout.addWidget(self.groupBoxCurrent)

        self.groupBoxNew = QGroupBox(self.scrollAreaWidgetContentsCustomize)
        self.groupBoxNew.setObjectName(u"groupBoxNew")
        self.verticalLayout_12 = QVBoxLayout(self.groupBoxNew)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBoxNew)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.lineEditNewName = QLineEdit(self.groupBoxNew)
        self.lineEditNewName.setObjectName(u"lineEditNewName")

        self.horizontalLayout_5.addWidget(self.lineEditNewName)

        self.pushButtonNewCustomization = QPushButton(self.groupBoxNew)
        self.pushButtonNewCustomization.setObjectName(u"pushButtonNewCustomization")

        self.horizontalLayout_5.addWidget(self.pushButtonNewCustomization)


        self.verticalLayout_12.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addWidget(self.groupBoxNew)

        self.labelWarningOnNew = QLabel(self.scrollAreaWidgetContentsCustomize)
        self.labelWarningOnNew.setObjectName(u"labelWarningOnNew")
        self.labelWarningOnNew.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelWarningOnNew)

        self.verticalSpacer_2 = QSpacerItem(198, 135, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.scrollAreaWidgetContentsCustomize)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.labelReportClass = QLabel(self.scrollAreaWidgetContentsCustomize)
        self.labelReportClass.setObjectName(u"labelReportClass")
        font = QFont()
        font.setBold(True)
        self.labelReportClass.setFont(font)

        self.horizontalLayout_6.addWidget(self.labelReportClass)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.scrollAreaCustomize.setWidget(self.scrollAreaWidgetContentsCustomize)

        self.verticalLayout_15.addWidget(self.scrollAreaCustomize)

        self.tabWidget.addTab(self.tabCustomize, "")

        self.verticalLayout_14.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(PrintDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_14.addWidget(self.buttonBox)


        self.retranslateUi(PrintDialog)
        self.buttonBox.accepted.connect(PrintDialog.accept)
        self.buttonBox.rejected.connect(PrintDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PrintDialog)
    # setupUi

    def retranslateUi(self, PrintDialog):
        PrintDialog.setWindowTitle(QCoreApplication.translate("PrintDialog", u"Print", None))
        self.toolButtonPrintPreview.setText(QCoreApplication.translate("PrintDialog", u"Print preview", None))
        self.toolButtonPrint.setText(QCoreApplication.translate("PrintDialog", u"Print", None))
        self.toolButtonPrintDirect.setText(QCoreApplication.translate("PrintDialog", u"Print direct", None))
        self.toolButtonPrintPDF.setText(QCoreApplication.translate("PrintDialog", u"Export PDF", None))
        self.label_3.setText(QCoreApplication.translate("PrintDialog", u"Report", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabParameters), QCoreApplication.translate("PrintDialog", u"Parameters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), QCoreApplication.translate("PrintDialog", u"Filters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSorting), QCoreApplication.translate("PrintDialog", u"Sorting", None))
        self.groupBoxPrint.setTitle(QCoreApplication.translate("PrintDialog", u"Print", None))
        self.labelDirectPrint.setText(QCoreApplication.translate("PrintDialog", u"Direct print to", None))
        self.groupBoxPDFExport.setTitle(QCoreApplication.translate("PrintDialog", u"Export to PDF file", None))
        self.label_6.setText(QCoreApplication.translate("PrintDialog", u"Directory", None))
        self.pushButtonSelectDirectory.setText(QCoreApplication.translate("PrintDialog", u"Select ...", None))
        self.label_7.setText(QCoreApplication.translate("PrintDialog", u"File name", None))
        self.label_8.setText(QCoreApplication.translate("PrintDialog", u".pdf", None))
        self.checkBoxOpenPDF.setText(QCoreApplication.translate("PrintDialog", u"Open PDF file after creation", None))
        self.label_4.setText(QCoreApplication.translate("PrintDialog", u"PDF version", None))
        self.label_5.setText(QCoreApplication.translate("PrintDialog", u"Resolution", None))
        self.label_9.setText(QCoreApplication.translate("PrintDialog", u"dpi", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPintOptions), QCoreApplication.translate("PrintDialog", u"Options", None))
        self.groupBoxCurrent.setTitle(QCoreApplication.translate("PrintDialog", u"Current customization", None))
        self.pushButtonUpdate.setText(QCoreApplication.translate("PrintDialog", u"Update", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("PrintDialog", u"Delete", None))
        self.pushButtonSetSorting.setText(QCoreApplication.translate("PrintDialog", u"Set sorting to", None))
        self.groupBoxNew.setTitle(QCoreApplication.translate("PrintDialog", u"New customization", None))
        self.label_2.setText(QCoreApplication.translate("PrintDialog", u"Name", None))
        self.pushButtonNewCustomization.setText(QCoreApplication.translate("PrintDialog", u"Create", None))
        self.labelWarningOnNew.setText(QCoreApplication.translate("PrintDialog", u"Creating a new customization does not save its parameters, you need to select the new customization, set the parameters/filters/sorting and update it", None))
        self.label.setText(QCoreApplication.translate("PrintDialog", u"Report Class: ", None))
        self.labelReportClass.setText(QCoreApplication.translate("PrintDialog", u"Report Class: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCustomize), QCoreApplication.translate("PrintDialog", u"Customize", None))
    # retranslateUi

