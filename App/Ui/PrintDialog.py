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
        PrintDialog.resize(758, 493)
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
        self.scrollAreaWidgetContentsParameters.setGeometry(QRect(0, 0, 714, 316))
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
        self.scrollAreaWidgetContentsFilters.setGeometry(QRect(0, 0, 98, 28))
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
        self.tabPintOptions = QWidget()
        self.tabPintOptions.setObjectName(u"tabPintOptions")
        self.verticalLayout_9 = QVBoxLayout(self.tabPintOptions)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.scrollAreaPrintOptions = QScrollArea(self.tabPintOptions)
        self.scrollAreaPrintOptions.setObjectName(u"scrollAreaPrintOptions")
        self.scrollAreaPrintOptions.setWidgetResizable(True)
        self.scrollAreaWidgetContentsOptions = QWidget()
        self.scrollAreaWidgetContentsOptions.setObjectName(u"scrollAreaWidgetContentsOptions")
        self.scrollAreaWidgetContentsOptions.setGeometry(QRect(0, 0, 574, 259))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContentsOptions)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
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


        self.horizontalLayout_8.addWidget(self.groupBoxPrint)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.pushButtonUserDefault = QPushButton(self.scrollAreaWidgetContentsOptions)
        self.pushButtonUserDefault.setObjectName(u"pushButtonUserDefault")

        self.horizontalLayout_8.addWidget(self.pushButtonUserDefault)


        self.verticalLayout_18.addLayout(self.horizontalLayout_8)

        self.groupBoxPDFExport = QGroupBox(self.scrollAreaWidgetContentsOptions)
        self.groupBoxPDFExport.setObjectName(u"groupBoxPDFExport")
        self.verticalLayout_13 = QVBoxLayout(self.groupBoxPDFExport)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(5, 5, 5, 5)
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

        self.verticalSpacer_3 = QSpacerItem(549, 34, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        self.scrollAreaWidgetContentsCustomize.setGeometry(QRect(0, 0, 686, 378))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContentsCustomize)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
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

        self.pushButtonClassDefault = QPushButton(self.groupBoxCurrent)
        self.pushButtonClassDefault.setObjectName(u"pushButtonClassDefault")

        self.horizontalLayout_3.addWidget(self.pushButtonClassDefault)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

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


        self.verticalLayout_16.addWidget(self.groupBoxCurrent)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContentsCustomize)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelReportClass = QLabel(self.groupBox)
        self.labelReportClass.setObjectName(u"labelReportClass")
        font = QFont()
        font.setBold(True)
        self.labelReportClass.setFont(font)

        self.horizontalLayout_5.addWidget(self.labelReportClass)

        self.comboBoxReportList = QComboBox(self.groupBox)
        self.comboBoxReportList.setObjectName(u"comboBoxReportList")

        self.horizontalLayout_5.addWidget(self.comboBoxReportList)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_9.addWidget(self.groupBox)

        self.groupBoxNew = QGroupBox(self.scrollAreaWidgetContentsCustomize)
        self.groupBoxNew.setObjectName(u"groupBoxNew")
        self.verticalLayout_12 = QVBoxLayout(self.groupBoxNew)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEditNewName = QLineEdit(self.groupBoxNew)
        self.lineEditNewName.setObjectName(u"lineEditNewName")

        self.horizontalLayout_6.addWidget(self.lineEditNewName)

        self.pushButtonNewCustomization = QPushButton(self.groupBoxNew)
        self.pushButtonNewCustomization.setObjectName(u"pushButtonNewCustomization")

        self.horizontalLayout_6.addWidget(self.pushButtonNewCustomization)


        self.verticalLayout_12.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_9.addWidget(self.groupBoxNew)


        self.verticalLayout_16.addLayout(self.horizontalLayout_9)

        self.labelWarningOnNew = QLabel(self.scrollAreaWidgetContentsCustomize)
        self.labelWarningOnNew.setObjectName(u"labelWarningOnNew")
        self.labelWarningOnNew.setWordWrap(True)

        self.verticalLayout_16.addWidget(self.labelWarningOnNew)

        self.verticalSpacer_2 = QSpacerItem(198, 135, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_2)

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

        QWidget.setTabOrder(self.toolButtonPrintPreview, self.toolButtonPrint)
        QWidget.setTabOrder(self.toolButtonPrint, self.toolButtonPrintDirect)
        QWidget.setTabOrder(self.toolButtonPrintDirect, self.toolButtonPrintPDF)
        QWidget.setTabOrder(self.toolButtonPrintPDF, self.comboBoxReportCustomizations)
        QWidget.setTabOrder(self.comboBoxReportCustomizations, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.scrollAreaParameters)
        QWidget.setTabOrder(self.scrollAreaParameters, self.scrollAreaFilters)
        QWidget.setTabOrder(self.scrollAreaFilters, self.scrollAreaPrintOptions)
        QWidget.setTabOrder(self.scrollAreaPrintOptions, self.comboBoxPrinters)
        QWidget.setTabOrder(self.comboBoxPrinters, self.pushButtonUserDefault)
        QWidget.setTabOrder(self.pushButtonUserDefault, self.lineEditDirectory)
        QWidget.setTabOrder(self.lineEditDirectory, self.pushButtonSelectDirectory)
        QWidget.setTabOrder(self.pushButtonSelectDirectory, self.lineEditFileName)
        QWidget.setTabOrder(self.lineEditFileName, self.checkBoxOpenPDF)
        QWidget.setTabOrder(self.checkBoxOpenPDF, self.comboBoxPDFVersion)
        QWidget.setTabOrder(self.comboBoxPDFVersion, self.spinBoxResolution)
        QWidget.setTabOrder(self.spinBoxResolution, self.scrollAreaCustomize)
        QWidget.setTabOrder(self.scrollAreaCustomize, self.pushButtonUpdate)
        QWidget.setTabOrder(self.pushButtonUpdate, self.pushButtonDelete)
        QWidget.setTabOrder(self.pushButtonDelete, self.pushButtonClassDefault)
        QWidget.setTabOrder(self.pushButtonClassDefault, self.pushButtonSetSorting)
        QWidget.setTabOrder(self.pushButtonSetSorting, self.spinBoxClassSorting)
        QWidget.setTabOrder(self.spinBoxClassSorting, self.comboBoxReportList)
        QWidget.setTabOrder(self.comboBoxReportList, self.lineEditNewName)
        QWidget.setTabOrder(self.lineEditNewName, self.pushButtonNewCustomization)

        self.retranslateUi(PrintDialog)
        self.buttonBox.accepted.connect(PrintDialog.accept)
        self.buttonBox.rejected.connect(PrintDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PrintDialog)
    # setupUi

    def retranslateUi(self, PrintDialog):
        PrintDialog.setWindowTitle(QCoreApplication.translate("PrintDialog", u"Print", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPrintPreview.setToolTip(QCoreApplication.translate("PrintDialog", u"Print preview", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPrintPreview.setText(QCoreApplication.translate("PrintDialog", u"Print preview", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPrint.setToolTip(QCoreApplication.translate("PrintDialog", u"Print", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPrint.setText(QCoreApplication.translate("PrintDialog", u"Print", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPrintDirect.setToolTip(QCoreApplication.translate("PrintDialog", u"Print direct", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPrintDirect.setText(QCoreApplication.translate("PrintDialog", u"Print direct", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPrintPDF.setToolTip(QCoreApplication.translate("PrintDialog", u"Export to a PDF file", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPrintPDF.setText(QCoreApplication.translate("PrintDialog", u"Export PDF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabParameters), QCoreApplication.translate("PrintDialog", u"Parameters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), QCoreApplication.translate("PrintDialog", u"Filters", None))
        self.groupBoxPrint.setTitle(QCoreApplication.translate("PrintDialog", u"Print", None))
        self.labelDirectPrint.setText(QCoreApplication.translate("PrintDialog", u"Direct print to", None))
        self.pushButtonUserDefault.setText(QCoreApplication.translate("PrintDialog", u"Set as user default", None))
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
        self.pushButtonClassDefault.setText(QCoreApplication.translate("PrintDialog", u"Set as class default", None))
        self.pushButtonSetSorting.setText(QCoreApplication.translate("PrintDialog", u"Set sorting to", None))
        self.groupBox.setTitle(QCoreApplication.translate("PrintDialog", u"Report class / Report", None))
        self.labelReportClass.setText(QCoreApplication.translate("PrintDialog", u"Class", None))
        self.groupBoxNew.setTitle(QCoreApplication.translate("PrintDialog", u"New customization", None))
        self.pushButtonNewCustomization.setText(QCoreApplication.translate("PrintDialog", u"Create", None))
        self.labelWarningOnNew.setText(QCoreApplication.translate("PrintDialog", u"Creating a new customization does not save its parameters, you need to select the new customization, set the parameters/filters/sorting and update it", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCustomize), QCoreApplication.translate("PrintDialog", u"Customize", None))
    # retranslateUi

