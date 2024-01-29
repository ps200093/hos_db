import delicateInfo
import sys

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import mysql.connector

from examineType import examinList

# UI 연결
form_secondclass = uic.loadUiType("kiosk_GUI.ui")[0]


class firstcome(QDialog, QWidget, form_secondclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("초진")

        # DB 연결
        self.conn = mysql.connector.connect(
            host=delicateInfo.host,
            user=delicateInfo.user,
            password=delicateInfo.password,
            database='hos_db'
        )
        self.cursor = self.conn.cursor()

        # LineEdit 설정
        self.name_box.setValidator(QRegExpValidator(QRegExp("[a-zA-Z가-힣]{30}"), self))
        self.birth_box.setEchoMode(QLineEdit.Password)
        self.birth_box.setValidator(QRegExpValidator(QRegExp("[0-9]{6}"), self))

        self.phone_box_default.setValidator(QRegExpValidator(QRegExp("[0-9]{3}"), self))
        self.phone_box_2.setValidator(QRegExpValidator(QRegExp("[0-9]{4}"), self))
        self.phone_box_3.setValidator(QRegExpValidator(QRegExp("[0-9]{4}"), self))

        # 홈으로
        self.back_main.clicked.connect(self.accept)

        # 다음
        self.enter_button.clicked.connect(self.check_info)

        self.sel_item = ""
        self.dup_pt = []

    def check_info(self):  # 초진 정보 입력
        new_pt_name = self.name_box.text()
        new_pt_birth = self.birth_box.text()
        new_pt_phone = (self.phone_box_default.text() + "-"
                        + self.phone_box_2.text() + "-"
                        + self.phone_box_3.text())

        sex = ""
        if self.sex_bt.isChecked():
            sex = 'M'
        elif self.sex_bt2.isChecked():
            sex = 'F'

        if new_pt_name and len(new_pt_birth) == 6 and len(new_pt_phone) == 13 and sex:
            MessageBoxBt = QMessageBox.information(self, " 확인 ",
                                                   "이름 : " + new_pt_name +
                                                   "\n생년월일 : " + new_pt_birth +
                                                   "\n전화번호 : " + new_pt_phone +
                                                   "\n\n입력하신 정보가 맞습니까?",
                                                   QMessageBox.Yes | QMessageBox.Cancel)
            if MessageBoxBt == QMessageBox.Yes:
                print("Yes is clicked")

                query = ("SELECT * FROM patient where pt_name = %s "
                         "AND pt_sex = %s "
                         "AND pt_birth = %s "
                         "AND pt_phone = %s")
                values = (new_pt_name, sex, new_pt_birth, new_pt_phone)
                self.cursor.execute(query, values)
                search_pt_result = self.cursor.fetchall()
                print("검색된 환자 목록 : ", search_pt_result)

                if search_pt_result:
                    print("이미 정보가 있음")
                    self.exList = examinList()
                    self.exList.show()
                    self.exList.exec_()

                    self.dup_pt = (search_pt_result[0])
                    self.sel_item = self.exList.selected_examine
                    self.accept()
                    # print("선택 진료 : ", self.exList.selected_examine)

                else:
                    print("환자 정보 신규 등록")
                    insert_query = ("INSERT INTO patient (pt_name, pt_sex, pt_birth, pt_phone)"
                                    " VALUES (%s, %s, %s, %s)")
                    data = (new_pt_name, sex, new_pt_birth, new_pt_phone)
                    self.cursor.execute(insert_query, data)
                    self.conn.commit()

                    query = ("SELECT * FROM patient where pt_name = %s "
                             "AND pt_sex = %s "
                             "AND pt_birth = %s "
                             "AND pt_phone = %s")
                    values = (new_pt_name, sex, new_pt_birth, new_pt_phone)
                    self.cursor.execute(query, values)
                    search_pt_result = self.cursor.fetchall()
                    print("추가된 환자 목록 : ", search_pt_result)
                    self.conn.commit()

                    self.exList = examinList()
                    self.exList.show()
                    self.exList.exec_()

                    self.dup_pt = (search_pt_result[0])
                    self.sel_item = self.exList.selected_examine
                    self.accept()
                # self.accept()  #창 닫기
            else:
                print("입력 취소")
        else:
            QMessageBox.critical(self, "ERROR", "전부 입력해주십시오.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = firstcome()
    myWindow.show()
    app.exec_()
