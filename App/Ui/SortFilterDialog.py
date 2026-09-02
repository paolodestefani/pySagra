# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SortFilterDialog.ui'
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
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_SortFilterDialog(object):
    def setupUi(self, SortFilterDialog):
        if not SortFilterDialog.objectName():
            SortFilterDialog.setObjectName(u"SortFilterDialog")
        SortFilterDialog.resize(667, 475)
        self.verticalLayout_5 = QVBoxLayout(SortFilterDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBoxSetting = QComboBox(SortFilterDialog)
        self.comboBoxSetting.setObjectName(u"comboBoxSetting")

        self.verticalLayout_3.addWidget(self.comboBoxSetting)

        self.tabWidget = QTabWidget(SortFilterDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabFilters = QWidget()
        self.tabFilters.setObjectName(u"tabFilters")
        self.verticalLayout_10 = QVBoxLayout(self.tabFilters)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.scrollAreaFilters = QScrollArea(self.tabFilters)
        self.scrollAreaFilters.setObjectName(u"scrollAreaFilters")
        self.scrollAreaFilters.setWidgetResizable(True)
        self.scrollAreaWidgetContentsFilters = QWidget()
        self.scrollAreaWidgetContentsFilters.setObjectName(u"scrollAreaWidgetContentsFilters")
        self.scrollAreaWidgetContentsFilters.setGeometry(QRect(0, 0, 589, 265))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContentsFilters)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.layoutFilters = QGridLayout()
        self.layoutFilters.setObjectName(u"layoutFilters")
        self.layoutFilters.setHorizontalSpacing(12)
        self.layoutFilters.setVerticalSpacing(6)
        self.layoutFilters.setContentsMargins(6, 6, 6, 6)

        self.verticalLayout_7.addLayout(self.layoutFilters)

        self.scrollAreaFilters.setWidget(self.scrollAreaWidgetContentsFilters)

        self.verticalLayout_10.addWidget(self.scrollAreaFilters)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxMaxRows = QCheckBox(self.tabFilters)
        self.checkBoxMaxRows.setObjectName(u"checkBoxMaxRows")
        self.checkBoxMaxRows.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBoxMaxRows)

        self.spinBoxMaxRows = QSpinBox(self.tabFilters)
        self.spinBoxMaxRows.setObjectName(u"spinBoxMaxRows")
        self.spinBoxMaxRows.setMaximum(99999)

        self.horizontalLayout_3.addWidget(self.spinBoxMaxRows)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.pushButtonUserDefault = QPushButton(self.tabFilters)
        self.pushButtonUserDefault.setObjectName(u"pushButtonUserDefault")

        self.horizontalLayout_3.addWidget(self.pushButtonUserDefault)


        self.verticalLayout_10.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tabFilters, "")
        self.tabSorting = QWidget()
        self.tabSorting.setObjectName(u"tabSorting")
        self.verticalLayout_8 = QVBoxLayout(self.tabSorting)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollAreaSorting = QScrollArea(self.tabSorting)
        self.scrollAreaSorting.setObjectName(u"scrollAreaSorting")
        self.scrollAreaSorting.setWidgetResizable(True)
        self.scrollAreaWidgetContentsSorting = QWidget()
        self.scrollAreaWidgetContentsSorting.setObjectName(u"scrollAreaWidgetContentsSorting")
        self.scrollAreaWidgetContentsSorting.setGeometry(QRect(0, 0, 589, 308))
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
        self.tabCustomize = QWidget()
        self.tabCustomize.setObjectName(u"tabCustomize")
        self.verticalLayout_9 = QVBoxLayout(self.tabCustomize)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.scrollAreaPrintOptions = QScrollArea(self.tabCustomize)
        self.scrollAreaPrintOptions.setObjectName(u"scrollAreaPrintOptions")
        self.scrollAreaPrintOptions.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 589, 308))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBoxCurrent = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxCurrent.setObjectName(u"groupBoxCurrent")
        self.verticalLayout = QVBoxLayout(self.groupBoxCurrent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonUpdate = QPushButton(self.groupBoxCurrent)
        self.pushButtonUpdate.setObjectName(u"pushButtonUpdate")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUpdate.sizePolicy().hasHeightForWidth())
        self.pushButtonUpdate.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonUpdate)

        self.pushButtonDelete = QPushButton(self.groupBoxCurrent)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")
        sizePolicy.setHeightForWidth(self.pushButtonDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonDelete.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonDelete)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pushButtonClassDefault = QPushButton(self.groupBoxCurrent)
        self.pushButtonClassDefault.setObjectName(u"pushButtonClassDefault")

        self.horizontalLayout.addWidget(self.pushButtonClassDefault)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.pushButtonSetSorting = QPushButton(self.groupBoxCurrent)
        self.pushButtonSetSorting.setObjectName(u"pushButtonSetSorting")

        self.horizontalLayout.addWidget(self.pushButtonSetSorting)

        self.spinBoxClassSorting = QSpinBox(self.groupBoxCurrent)
        self.spinBoxClassSorting.setObjectName(u"spinBoxClassSorting")

        self.horizontalLayout.addWidget(self.spinBoxClassSorting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addWidget(self.groupBoxCurrent)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEditNewName = QLineEdit(self.groupBox)
        self.lineEditNewName.setObjectName(u"lineEditNewName")

        self.gridLayout.addWidget(self.lineEditNewName, 0, 1, 1, 1)

        self.pushButtonNewCustomization = QPushButton(self.groupBox)
        self.pushButtonNewCustomization.setObjectName(u"pushButtonNewCustomization")

        self.gridLayout.addWidget(self.pushButtonNewCustomization, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 86, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEditSortFilterClass = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEditSortFilterClass.setObjectName(u"lineEditSortFilterClass")
        self.lineEditSortFilterClass.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEditSortFilterClass.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEditSortFilterClass)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.scrollAreaPrintOptions.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_9.addWidget(self.scrollAreaPrintOptions)

        self.tabWidget.addTab(self.tabCustomize, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(SortFilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        QWidget.setTabOrder(self.comboBoxSetting, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.scrollAreaFilters)
        QWidget.setTabOrder(self.scrollAreaFilters, self.checkBoxMaxRows)
        QWidget.setTabOrder(self.checkBoxMaxRows, self.spinBoxMaxRows)
        QWidget.setTabOrder(self.spinBoxMaxRows, self.pushButtonUserDefault)
        QWidget.setTabOrder(self.pushButtonUserDefault, self.scrollAreaSorting)
        QWidget.setTabOrder(self.scrollAreaSorting, self.scrollAreaPrintOptions)
        QWidget.setTabOrder(self.scrollAreaPrintOptions, self.pushButtonUpdate)
        QWidget.setTabOrder(self.pushButtonUpdate, self.pushButtonDelete)
        QWidget.setTabOrder(self.pushButtonDelete, self.pushButtonClassDefault)
        QWidget.setTabOrder(self.pushButtonClassDefault, self.pushButtonSetSorting)
        QWidget.setTabOrder(self.pushButtonSetSorting, self.spinBoxClassSorting)
        QWidget.setTabOrder(self.spinBoxClassSorting, self.lineEditNewName)
        QWidget.setTabOrder(self.lineEditNewName, self.pushButtonNewCustomization)

        self.retranslateUi(SortFilterDialog)
        self.buttonBox.accepted.connect(SortFilterDialog.accept)
        self.buttonBox.rejected.connect(SortFilterDialog.reject)
        self.checkBoxMaxRows.clicked["bool"].connect(self.spinBoxMaxRows.setEnabled)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SortFilterDialog)
    # setupUi

    def retranslateUi(self, SortFilterDialog):
        SortFilterDialog.setWindowTitle(QCoreApplication.translate("SortFilterDialog", u"Sort & Filter", None))
        self.checkBoxMaxRows.setText(QCoreApplication.translate("SortFilterDialog", u"Max rows", None))
        self.pushButtonUserDefault.setText(QCoreApplication.translate("SortFilterDialog", u"Set as user default", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilters), QCoreApplication.translate("SortFilterDialog", u"Filters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSorting), QCoreApplication.translate("SortFilterDialog", u"Sorting", None))
        self.groupBoxCurrent.setTitle(QCoreApplication.translate("SortFilterDialog", u"Current customization", None))
        self.pushButtonUpdate.setText(QCoreApplication.translate("SortFilterDialog", u"Update", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("SortFilterDialog", u"Delete", None))
        self.pushButtonClassDefault.setText(QCoreApplication.translate("SortFilterDialog", u"Set as class default", None))
        self.pushButtonSetSorting.setText(QCoreApplication.translate("SortFilterDialog", u"Set sorting to", None))
        self.groupBox.setTitle(QCoreApplication.translate("SortFilterDialog", u"New customization", None))
        self.label_2.setText(QCoreApplication.translate("SortFilterDialog", u"Name", None))
        self.pushButtonNewCustomization.setText(QCoreApplication.translate("SortFilterDialog", u"Create", None))
        self.label.setText(QCoreApplication.translate("SortFilterDialog", u"Class", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCustomize), QCoreApplication.translate("SortFilterDialog", u"Customize", None))
    # retranslateUi

