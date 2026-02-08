# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReportWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox
from App.Widget.View import EnhancedTableView

class Ui_ReportWidget(object):
    def setupUi(self, ReportWidget):
        if not ReportWidget.objectName():
            ReportWidget.setObjectName(u"ReportWidget")
        ReportWidget.resize(1105, 662)
        self.verticalLayout_6 = QVBoxLayout(ReportWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(ReportWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.form = QWidget()
        self.form.setObjectName(u"form")
        self.verticalLayout_3 = QVBoxLayout(self.form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditCode = QLineEdit(self.form)
        self.lineEditCode.setObjectName(u"lineEditCode")
        self.lineEditCode.setEnabled(False)

        self.gridLayout.addWidget(self.lineEditCode, 0, 1, 1, 1)

        self.label_3 = QLabel(self.form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.comboBoxL10n = RelationalComboBox(self.form)
        self.comboBoxL10n.setObjectName(u"comboBoxL10n")
        self.comboBoxL10n.setEnabled(True)
        self.comboBoxL10n.setEditable(False)

        self.gridLayout.addWidget(self.comboBoxL10n, 0, 3, 1, 1)

        self.label_2 = QLabel(self.form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)

        self.comboBoxClass = QComboBox(self.form)
        self.comboBoxClass.setObjectName(u"comboBoxClass")

        self.gridLayout.addWidget(self.comboBoxClass, 0, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(168, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.checkBoxSystem = QCheckBox(self.form)
        self.checkBoxSystem.setObjectName(u"checkBoxSystem")
        self.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout.addWidget(self.checkBoxSystem, 0, 7, 1, 1)

        self.label_4 = QLabel(self.form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEditDescription = QLineEdit(self.form)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.gridLayout.addWidget(self.lineEditDescription, 1, 1, 1, 7)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.groupBox_5 = QGroupBox(self.form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEditXML = QPlainTextEdit(self.groupBox_5)
        self.textEditXML.setObjectName(u"textEditXML")
        font = QFont()
        font.setPointSize(10)
        self.textEditXML.setFont(font)

        self.verticalLayout_2.addWidget(self.textEditXML)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.stackedWidget.addWidget(self.form)
        self.view = QWidget()
        self.view.setObjectName(u"view")
        self.verticalLayout = QVBoxLayout(self.view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(self.view)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.view)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(ReportWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.fontComboBox = QFontComboBox(ReportWidget)
        self.fontComboBox.setObjectName(u"fontComboBox")
        self.fontComboBox.setEditable(True)
        self.fontComboBox.setMaxVisibleItems(20)
        self.fontComboBox.setFontFilters(QFontComboBox.FontFilter.MonospacedFonts)
        font1 = QFont()
        font1.setPointSize(8)
        self.fontComboBox.setCurrentFont(font1)

        self.horizontalLayout.addWidget(self.fontComboBox)

        self.spinBoxFontSize = QSpinBox(ReportWidget)
        self.spinBoxFontSize.setObjectName(u"spinBoxFontSize")

        self.horizontalLayout.addWidget(self.spinBoxFontSize)

        self.pushButtonInsertImage = QPushButton(ReportWidget)
        self.pushButtonInsertImage.setObjectName(u"pushButtonInsertImage")

        self.horizontalLayout.addWidget(self.pushButtonInsertImage)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonDeleteAll = QPushButton(ReportWidget)
        self.pushButtonDeleteAll.setObjectName(u"pushButtonDeleteAll")

        self.horizontalLayout.addWidget(self.pushButtonDeleteAll)

        self.pushButtonDownload = QPushButton(ReportWidget)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.pushButtonUpload = QPushButton(ReportWidget)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout.addWidget(self.pushButtonUpload)

        self.pushButtonDownloadAll = QPushButton(ReportWidget)
        self.pushButtonDownloadAll.setObjectName(u"pushButtonDownloadAll")

        self.horizontalLayout.addWidget(self.pushButtonDownloadAll)

        self.pushButtonUploadAll = QPushButton(ReportWidget)
        self.pushButtonUploadAll.setObjectName(u"pushButtonUploadAll")

        self.horizontalLayout.addWidget(self.pushButtonUploadAll)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        QWidget.setTabOrder(self.lineEditCode, self.comboBoxL10n)
        QWidget.setTabOrder(self.comboBoxL10n, self.comboBoxClass)
        QWidget.setTabOrder(self.comboBoxClass, self.lineEditDescription)
        QWidget.setTabOrder(self.lineEditDescription, self.textEditXML)
        QWidget.setTabOrder(self.textEditXML, self.fontComboBox)
        QWidget.setTabOrder(self.fontComboBox, self.spinBoxFontSize)
        QWidget.setTabOrder(self.spinBoxFontSize, self.pushButtonInsertImage)
        QWidget.setTabOrder(self.pushButtonInsertImage, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonUpload)
        QWidget.setTabOrder(self.pushButtonUpload, self.pushButtonDownloadAll)
        QWidget.setTabOrder(self.pushButtonDownloadAll, self.pushButtonUploadAll)
        QWidget.setTabOrder(self.pushButtonUploadAll, self.tableView)
        QWidget.setTabOrder(self.tableView, self.checkBoxSystem)

        self.retranslateUi(ReportWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ReportWidget)
    # setupUi

    def retranslateUi(self, ReportWidget):
        ReportWidget.setWindowTitle(QCoreApplication.translate("ReportWidget", u"Report", None))
        self.label.setText(QCoreApplication.translate("ReportWidget", u"Code", None))
        self.label_3.setText(QCoreApplication.translate("ReportWidget", u"Language/Country", None))
        self.label_2.setText(QCoreApplication.translate("ReportWidget", u"Class", None))
        self.checkBoxSystem.setText(QCoreApplication.translate("ReportWidget", u"System report", None))
        self.label_4.setText(QCoreApplication.translate("ReportWidget", u"Description", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("ReportWidget", u"XML report definition", None))
        self.label_5.setText(QCoreApplication.translate("ReportWidget", u"Font", None))
        self.pushButtonInsertImage.setText(QCoreApplication.translate("ReportWidget", u"Insert image from file to clipboard", None))
        self.pushButtonDeleteAll.setText(QCoreApplication.translate("ReportWidget", u"Delete All", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("ReportWidget", u"Download ...", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("ReportWidget", u"Upload ...", None))
        self.pushButtonDownloadAll.setText(QCoreApplication.translate("ReportWidget", u"Download all reports...", None))
        self.pushButtonUploadAll.setText(QCoreApplication.translate("ReportWidget", u"Upload all reports ...", None))
    # retranslateUi

