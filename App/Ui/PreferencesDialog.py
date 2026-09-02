# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreferencesDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFontComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        PreferencesDialog.resize(645, 341)
        self.verticalLayout_9 = QVBoxLayout(PreferencesDialog)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.labelIcon = QLabel(PreferencesDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_6.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBoxTheme = QGroupBox(PreferencesDialog)
        self.groupBoxTheme.setObjectName(u"groupBoxTheme")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxTheme)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.comboBoxTheme = RelationalComboBox(self.groupBoxTheme)
        self.comboBoxTheme.setObjectName(u"comboBoxTheme")

        self.verticalLayout_4.addWidget(self.comboBoxTheme)


        self.gridLayout.addWidget(self.groupBoxTheme, 0, 0, 1, 2)

        self.groupBoxColorScheme = QGroupBox(PreferencesDialog)
        self.groupBoxColorScheme.setObjectName(u"groupBoxColorScheme")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxColorScheme)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBoxColorScheme = RelationalComboBox(self.groupBoxColorScheme)
        self.comboBoxColorScheme.setObjectName(u"comboBoxColorScheme")

        self.verticalLayout_3.addWidget(self.comboBoxColorScheme)


        self.gridLayout.addWidget(self.groupBoxColorScheme, 0, 2, 1, 1)

        self.groupBoxTabPosition = QGroupBox(PreferencesDialog)
        self.groupBoxTabPosition.setObjectName(u"groupBoxTabPosition")
        self.verticalLayout_7 = QVBoxLayout(self.groupBoxTabPosition)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.comboBoxTabPosition = RelationalComboBox(self.groupBoxTabPosition)
        self.comboBoxTabPosition.setObjectName(u"comboBoxTabPosition")

        self.verticalLayout_7.addWidget(self.comboBoxTabPosition)


        self.gridLayout.addWidget(self.groupBoxTabPosition, 1, 0, 1, 2)

        self.groupBoxToolButtonStyle = QGroupBox(PreferencesDialog)
        self.groupBoxToolButtonStyle.setObjectName(u"groupBoxToolButtonStyle")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxToolButtonStyle)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBoxToolButtonStyle = RelationalComboBox(self.groupBoxToolButtonStyle)
        self.comboBoxToolButtonStyle.setObjectName(u"comboBoxToolButtonStyle")

        self.verticalLayout_5.addWidget(self.comboBoxToolButtonStyle)


        self.gridLayout.addWidget(self.groupBoxToolButtonStyle, 1, 2, 1, 1)

        self.groupBoxFont = QGroupBox(PreferencesDialog)
        self.groupBoxFont.setObjectName(u"groupBoxFont")
        self.horizontalLayout = QHBoxLayout(self.groupBoxFont)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBoxFontFamily = QFontComboBox(self.groupBoxFont)
        self.comboBoxFontFamily.setObjectName(u"comboBoxFontFamily")
        self.comboBoxFontFamily.setEnabled(False)
        self.comboBoxFontFamily.setEditable(False)

        self.horizontalLayout.addWidget(self.comboBoxFontFamily)

        self.checkBoxDefaultFont = QCheckBox(self.groupBoxFont)
        self.checkBoxDefaultFont.setObjectName(u"checkBoxDefaultFont")
        self.checkBoxDefaultFont.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBoxDefaultFont)


        self.gridLayout.addWidget(self.groupBoxFont, 2, 0, 1, 1)

        self.groupBoxFontSize = QGroupBox(PreferencesDialog)
        self.groupBoxFontSize.setObjectName(u"groupBoxFontSize")
        self.verticalLayout = QVBoxLayout(self.groupBoxFontSize)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spinBoxFontSize = QSpinBox(self.groupBoxFontSize)
        self.spinBoxFontSize.setObjectName(u"spinBoxFontSize")
        self.spinBoxFontSize.setMinimum(6)
        self.spinBoxFontSize.setMaximum(72)
        self.spinBoxFontSize.setValue(10)

        self.verticalLayout.addWidget(self.spinBoxFontSize)


        self.gridLayout.addWidget(self.groupBoxFontSize, 2, 1, 1, 1)

        self.groupBoxIcon = QGroupBox(PreferencesDialog)
        self.groupBoxIcon.setObjectName(u"groupBoxIcon")
        self.verticalLayout_8 = QVBoxLayout(self.groupBoxIcon)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBoxIcons = RelationalComboBox(self.groupBoxIcon)
        self.comboBoxIcons.setObjectName(u"comboBoxIcons")

        self.verticalLayout_8.addWidget(self.comboBoxIcons)


        self.gridLayout.addWidget(self.groupBoxIcon, 2, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.label = QLabel(PreferencesDialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(17, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Help|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.RestoreDefaults)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_9.addWidget(self.buttonBox)


        self.retranslateUi(PreferencesDialog)
        self.buttonBox.accepted.connect(PreferencesDialog.accept)
        self.buttonBox.rejected.connect(PreferencesDialog.reject)
        self.checkBoxDefaultFont.clicked["bool"].connect(self.comboBoxFontFamily.setDisabled)

        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"Preferences", None))
        self.labelIcon.setText(QCoreApplication.translate("PreferencesDialog", u"icon", None))
        self.groupBoxTheme.setTitle(QCoreApplication.translate("PreferencesDialog", u"Theme", None))
        self.groupBoxColorScheme.setTitle(QCoreApplication.translate("PreferencesDialog", u"Color scheme", None))
        self.groupBoxTabPosition.setTitle(QCoreApplication.translate("PreferencesDialog", u"Tab position", None))
        self.groupBoxToolButtonStyle.setTitle(QCoreApplication.translate("PreferencesDialog", u"Tool button style", None))
        self.groupBoxFont.setTitle(QCoreApplication.translate("PreferencesDialog", u"Font family", None))
        self.checkBoxDefaultFont.setText(QCoreApplication.translate("PreferencesDialog", u"Default", None))
        self.groupBoxFontSize.setTitle(QCoreApplication.translate("PreferencesDialog", u"Font size", None))
        self.groupBoxIcon.setTitle(QCoreApplication.translate("PreferencesDialog", u"Icon set", None))
        self.label.setText(QCoreApplication.translate("PreferencesDialog", u"You may need to restart the application for the changes to take effect.", None))
    # retranslateUi

