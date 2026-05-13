# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScriptingWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFontComboBox,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox
from App.Widget.View import EnhancedTableView

class Ui_ScriptingWidget(object):
    def setupUi(self, ScriptingWidget):
        if not ScriptingWidget.objectName():
            ScriptingWidget.setObjectName(u"ScriptingWidget")
        ScriptingWidget.resize(908, 585)
        self.verticalLayout_6 = QVBoxLayout(ScriptingWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(ScriptingWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.form = QWidget()
        self.form.setObjectName(u"form")
        self.verticalLayout_3 = QVBoxLayout(self.form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.form)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBoxClass = QComboBox(self.groupBox)
        self.comboBoxClass.setObjectName(u"comboBoxClass")
        self.comboBoxClass.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.comboBoxClass)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBoxMethod = QComboBox(self.groupBox_3)
        self.comboBoxMethod.setObjectName(u"comboBoxMethod")
        self.comboBoxMethod.setEnabled(True)

        self.horizontalLayout_5.addWidget(self.comboBoxMethod)


        self.horizontalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBoxTrigger = RelationalComboBox(self.groupBox_2)
        self.comboBoxTrigger.setObjectName(u"comboBoxTrigger")
        self.comboBoxTrigger.setEnabled(True)

        self.verticalLayout_8.addWidget(self.comboBoxTrigger)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.comboBoxCompany = RelationalComboBox(self.groupBox_4)
        self.comboBoxCompany.setObjectName(u"comboBoxCompany")
        self.comboBoxCompany.setEnabled(True)

        self.verticalLayout_9.addWidget(self.comboBoxCompany)


        self.horizontalLayout_3.addWidget(self.groupBox_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.checkBoxActive = QCheckBox(self.form)
        self.checkBoxActive.setObjectName(u"checkBoxActive")

        self.horizontalLayout_3.addWidget(self.checkBoxActive)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.groupBox_5 = QGroupBox(self.form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.textEditScript = QPlainTextEdit(self.groupBox_5)
        self.textEditScript.setObjectName(u"textEditScript")
        font = QFont()
        font.setFamilies([u"Courier"])
        font.setPointSize(10)
        self.textEditScript.setFont(font)

        self.verticalLayout_2.addWidget(self.textEditScript)


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
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(ScriptingWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.fontComboBox = QFontComboBox(ScriptingWidget)
        self.fontComboBox.setObjectName(u"fontComboBox")
        self.fontComboBox.setEditable(True)
        self.fontComboBox.setMaxVisibleItems(20)
        self.fontComboBox.setFontFilters(QFontComboBox.FontFilter.MonospacedFonts)
        font1 = QFont()
        font1.setFamilies([u"Menlo"])
        font1.setPointSize(8)
        self.fontComboBox.setCurrentFont(font1)

        self.horizontalLayout.addWidget(self.fontComboBox)

        self.spinBoxFontSize = QSpinBox(ScriptingWidget)
        self.spinBoxFontSize.setObjectName(u"spinBoxFontSize")

        self.horizontalLayout.addWidget(self.spinBoxFontSize)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonDownload = QPushButton(ScriptingWidget)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.pushButtonUpload = QPushButton(ScriptingWidget)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout.addWidget(self.pushButtonUpload)

        self.pushButtonDownloadAll = QPushButton(ScriptingWidget)
        self.pushButtonDownloadAll.setObjectName(u"pushButtonDownloadAll")

        self.horizontalLayout.addWidget(self.pushButtonDownloadAll)

        self.pushButtonUploadAll = QPushButton(ScriptingWidget)
        self.pushButtonUploadAll.setObjectName(u"pushButtonUploadAll")

        self.horizontalLayout.addWidget(self.pushButtonUploadAll)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        QWidget.setTabOrder(self.textEditScript, self.fontComboBox)
        QWidget.setTabOrder(self.fontComboBox, self.spinBoxFontSize)
        QWidget.setTabOrder(self.spinBoxFontSize, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonUpload)
        QWidget.setTabOrder(self.pushButtonUpload, self.pushButtonDownloadAll)
        QWidget.setTabOrder(self.pushButtonDownloadAll, self.pushButtonUploadAll)
        QWidget.setTabOrder(self.pushButtonUploadAll, self.tableView)

        self.retranslateUi(ScriptingWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ScriptingWidget)
    # setupUi

    def retranslateUi(self, ScriptingWidget):
        ScriptingWidget.setWindowTitle(QCoreApplication.translate("ScriptingWidget", u"Python scripting", None))
        self.groupBox.setTitle(QCoreApplication.translate("ScriptingWidget", u"Class", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ScriptingWidget", u"Method", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ScriptingWidget", u"Trigger", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ScriptingWidget", u"Company", None))
        self.checkBoxActive.setText(QCoreApplication.translate("ScriptingWidget", u"Active", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("ScriptingWidget", u"Python script", None))
        self.label_5.setText(QCoreApplication.translate("ScriptingWidget", u"Font", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("ScriptingWidget", u"Download ...", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("ScriptingWidget", u"Upload ...", None))
        self.pushButtonDownloadAll.setText(QCoreApplication.translate("ScriptingWidget", u"Download all scripts...", None))
        self.pushButtonUploadAll.setText(QCoreApplication.translate("ScriptingWidget", u"Upload all scripts ...", None))
    # retranslateUi

