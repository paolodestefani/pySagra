# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ViewSettingsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QHeaderView, QSizePolicy, QTableWidgetItem,
    QVBoxLayout, QWidget)

from App.Widget.TableWidget import TableWidgetDragRows

class Ui_ViewSettingsDialog(object):
    def setupUi(self, ViewSettingsDialog):
        if not ViewSettingsDialog.objectName():
            ViewSettingsDialog.setObjectName(u"ViewSettingsDialog")
        ViewSettingsDialog.setWindowModality(Qt.ApplicationModal)
        ViewSettingsDialog.resize(521, 360)
        ViewSettingsDialog.setModal(True)
        self.verticalLayout_3 = QVBoxLayout(ViewSettingsDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxViewSettings = QGroupBox(ViewSettingsDialog)
        self.groupBoxViewSettings.setObjectName(u"groupBoxViewSettings")
        self.verticalLayout = QVBoxLayout(self.groupBoxViewSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = TableWidgetDragRows(self.groupBoxViewSettings)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)


        self.verticalLayout_2.addWidget(self.groupBoxViewSettings)

        self.buttonBox = QDialogButtonBox(ViewSettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(ViewSettingsDialog)
        self.buttonBox.accepted.connect(ViewSettingsDialog.accept)
        self.buttonBox.rejected.connect(ViewSettingsDialog.reject)

        QMetaObject.connectSlotsByName(ViewSettingsDialog)
    # setupUi

    def retranslateUi(self, ViewSettingsDialog):
        ViewSettingsDialog.setWindowTitle(QCoreApplication.translate("ViewSettingsDialog", u"Dialog", None))
        self.groupBoxViewSettings.setTitle(QCoreApplication.translate("ViewSettingsDialog", u"View Settings", None))
    # retranslateUi

