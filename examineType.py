import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

# UI 연결
form_exclass = uic.loadUiType("ex_menu.ui")[0]

class examinList(QDialog, QWidget, form_exclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("희망 진료 선택")

        self.selected_examine = ""

        self.checkBox_0.toggled.connect(self.choiceGroup_1)
        self.checkBox_1.toggled.connect(self.choiceGroup_1)
        self.checkBox_2.toggled.connect(self.choiceGroup_1)
        self.checkBox_3.toggled.connect(self.choiceGroup_1)
        self.checkBox_4.toggled.connect(self.choiceGroup_1)
        self.checkBox_5.toggled.connect(self.choiceGroup_1)
        self.checkBox_6.toggled.connect(self.choiceGroup_1)

        self.checkBox_7.toggled.connect(self.choiceGroup_2)
        self.checkBox_8.toggled.connect(self.choiceGroup_2)
        self.checkBox_9.toggled.connect(self.choiceGroup_2)
        self.checkBox_10.toggled.connect(self.choiceGroup_2)
        self.checkBox_11.toggled.connect(self.choiceGroup_2)

        self.checkBox_12.toggled.connect(self.choiceGroup_3)
        self.checkBox_13.toggled.connect(self.choiceGroup_3)
        self.checkBox_14.toggled.connect(self.choiceGroup_3)
        self.checkBox_15.toggled.connect(self.choiceGroup_3)
        self.checkBox_16.toggled.connect(self.choiceGroup_3)
        self.checkBox_17.toggled.connect(self.choiceGroup_3)
        self.checkBox_18.toggled.connect(self.choiceGroup_3)

        self.choice_button.clicked.connect(self.choiceList)

        # 이건 테스트 부분
        self.button_group1 = QButtonGroup(self)
        self.button_group1.addButton(self.checkBox_0)
        self.button_group1.addButton(self.checkBox_1)
        self.button_group1.addButton(self.checkBox_2)
        self.button_group1.addButton(self.checkBox_3)
        self.button_group1.addButton(self.checkBox_4)
        self.button_group1.addButton(self.checkBox_5)
        self.button_group1.addButton(self.checkBox_6)

        self.button_group2 = QButtonGroup(self)
        self.button_group2.addButton(self.checkBox_7)
        self.button_group2.addButton(self.checkBox_8)
        self.button_group2.addButton(self.checkBox_9)
        self.button_group2.addButton(self.checkBox_10)
        self.button_group2.addButton(self.checkBox_11)

        self.button_group3 = QButtonGroup(self)
        self.button_group3.addButton(self.checkBox_12)
        self.button_group3.addButton(self.checkBox_13)
        self.button_group3.addButton(self.checkBox_14)
        self.button_group3.addButton(self.checkBox_15)
        self.button_group3.addButton(self.checkBox_16)
        self.button_group3.addButton(self.checkBox_17)
        self.button_group3.addButton(self.checkBox_18)

    def choiceList(self):
        sel_item = ""
        for index in range(self.Layout_1.count()):
            widget_item = self.Layout_1.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                sel_item = (widget_item.widget().text())
        for index in range(self.Layout_2.count()):
            widget_item = self.Layout_2.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                sel_item = (widget_item.widget().text())
        for index in range(self.Layout_3.count()):
            widget_item = self.Layout_3.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                sel_item = (widget_item.widget().text())

        print(sel_item)
        self.selected_examine = sel_item
        self.close()

    def choiceGroup_1(self):
        self.button_group1.setExclusive(True)
        self.button_group2.setExclusive(False)
        self.button_group3.setExclusive(False)

        for index in range(self.Layout_2.count()):
            widget_item = self.Layout_2.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)

        for index in range(self.Layout_3.count()):
            widget_item = self.Layout_3.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)

    def choiceGroup_2(self):
        self.button_group1.setExclusive(False)
        self.button_group2.setExclusive(True)
        self.button_group3.setExclusive(False)

        for index in range(self.Layout_1.count()):
            widget_item = self.Layout_1.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)

        for index in range(self.Layout_3.count()):
            widget_item = self.Layout_3.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)

    def choiceGroup_3(self):
        self.button_group1.setExclusive(False)
        self.button_group2.setExclusive(False)
        self.button_group3.setExclusive(True)

        for index in range(self.Layout_1.count()):
            widget_item = self.Layout_1.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)

        for index in range(self.Layout_2.count()):
            widget_item = self.Layout_2.itemAt(index)
            if widget_item.widget() and widget_item.widget().isChecked():
                widget_item.widget().setChecked(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = examinList()
    myWindow.show()
    app.exec_()
