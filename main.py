import delicateInfo
import sys

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import mysql.connector

from SecondWindow import firstcome
from rebookedWindow import rebooked

# UI 연결
form_class = uic.loadUiType("hos_GUI.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("병원 관리 프로그램")

        # DB 연결
        self.conn = mysql.connector.connect(
            host=delicateInfo.host,
            user=delicateInfo.user,
            password=delicateInfo.password,
            database='hos_db'
        )
        self.cursor = self.conn.cursor()

        self.input_name_box.setValidator(QRegExpValidator(QRegExp("[a-zA-Z가-힣]{30}"), self))
        self.input_name_box.textChanged.connect(self.choice_pt_name)
        self.input_name_box.returnPressed.connect(self.choice_pt_name)

        self.pt_name_bt.clicked.connect(self.pt_name_input)
        self.search_pt.currentIndexChanged.connect(self.pt_name_input)
        self.dr_login.currentIndexChanged.connect(self.on_combo_box_changed)

        self.display_data()

        self.current_date_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.current_date_time)
        self.timer.start(1000)

        self.ex_date_box.currentIndexChanged.connect(self.date_changed)
        self.ex_date_box.currentIndexChanged.connect(self.dr_name_mark)
        self.apply_diagnosis.clicked.connect(self.popup)

        #방문자 레이아웃
        self.fst_come.clicked.connect(self.second_window)
        self.re_come.clicked.connect(self.third_window)

        #접수버튼
        self.receiveBt.clicked.connect(self.take_over)
        self.take_over_id = ""
        self.take_over_name = ""

    def second_window(self):    #초진
        self.second = firstcome()
        self.second.show()
        print("초진 화면 출력")

        self.second.exec_()
        if(self.second.dup_pt and self.second.sel_item):
            print("초진 환자 정보", self.second.dup_pt)
            print("선택 초진 정보 : ", self.second.sel_item)
            input_pt_id = self.second.dup_pt[0]
            input_pt_name = self.second.dup_pt[1]
            self.add_table_item(input_pt_id, input_pt_name, self.second.sel_item)
        else: print("입력 취소됨")

    def third_window(self):    #재진
        self.third = rebooked()
        self.third.show()
        print("재진 화면 출력")

        self.third.exec_()
        if (self.third.dup_pt and self.third.sel_item):
            print("재진 환자 정보", self.third.dup_pt)
            print("선택 재진 정보 : ", self.third.sel_item)
            input_pt_id = self.third.dup_pt[0]
            input_pt_name = self.third.dup_pt[1]
            self.add_table_item(input_pt_id, input_pt_name, self.third.sel_item)


    def add_table_item(self, pid, name, item):
        cur_row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(cur_row_count)
        target_data = [str(pid), name, item]
        for cur_col_count in range(0, 3):
            self.tableWidget.setItem(cur_row_count, cur_col_count, QTableWidgetItem(target_data[cur_col_count]))
            #self.tableWidget.setCellWidget(cur_row_count, 3, QRadioButton())

    def take_over(self):
        cur_row_count = self.tableWidget.rowCount()
        if cur_row_count > 0:
            self.take_over_id = ""
            mid_take_over_id = self.tableWidget.item(0, 0)
            self.take_over_id = mid_take_over_id.text()
            mid_take_over_name = self.tableWidget.item(0, 1)
            self.take_over_name = ""
            self.take_over_name = mid_take_over_name.text()
            self.listWidget.clear()
            self.input_name_box.clear()
            self.input_name_box.setText(self.take_over_name)
            asdf = self.take_over_id + " " + self.take_over_name
            print("asdf = ", asdf)
            self.search_pt.clear()
            self.search_pt.insertItem(0, asdf)
            self.tableWidget.removeRow(0)
        else:
            print("접수 인원 없음")


    def choice_pt_name(self):
        self.conn.commit()
        selected_item = self.input_name_box.text()

        print("검색한 환자 : ", selected_item)
        query = "SELECT pt_id, pt_name FROM patient where pt_name = %s"
        self.cursor.execute(query, (selected_item,))
        dup_pt_result = self.cursor.fetchall()
        print("검색된 환자 목록 : ", dup_pt_result)
        self.search_pt.clear()
        self.listWidget.clear()
        self.ex_date_box.clear()
        self.diagnosis_ex.clear()
        self.dr_name_box.clear()

        if dup_pt_result:
            pt_cho = dup_pt_result[0]
            print(pt_cho)
            print(type(pt_cho))
            dup_table_data = [' '.join(map(str, item)) for item in dup_pt_result]
            for row in dup_table_data:
                self.search_pt.addItem(row)
        else:
            self.listWidget.addItem("환자 정보 없음")

    def pt_name_input(self):
        if self.search_pt.currentText():
            input_string = self.search_pt.currentText()
            word_list = input_string.split()
            current_pt_id = word_list[0]
            print("current_pt_id : ", current_pt_id)

            ipt_name = self.input_name_box.text()
            print("현재 선택된 환자 name : ", ipt_name)
            query = "SELECT pt_name, pt_birth, pt_sex FROM patient where pt_id = %s"
            self.cursor.execute(query, (current_pt_id,))
            result = self.cursor.fetchall()
            print("환자 정보    ", result)
            # print("환자 정보 타입", type(result))

            if result:
                self.listWidget.clear()
                list_result = result[0]
                for item_text in list(list_result):
                    print("item : ", item_text)
                    self.listWidget.addItem(str(item_text))

                ipt_id = "SELECT pt_id FROM patient where pt_id = %s"
                self.cursor.execute(ipt_id, (current_pt_id,))
                result_pt_id = self.cursor.fetchall()
                pt_id = [int(row[0]) for row in result_pt_id]
                print("현재 선택된 환자 id : ", pt_id[0])

                query_pt_data = "SELECT ex_date FROM examine where pt_id = %s"
                self.cursor.execute(query_pt_data, (pt_id[0],))
                result_ex_date = self.cursor.fetchall()
                reversed_list = list(reversed([str(row[0]) for row in result_ex_date]))
                # print("reversed_ex_date : ", reversed_list)

                self.ex_date_box.clear()
                for row in reversed_list:
                    self.ex_date_box.addItem(row)
            else:
                self.listWidget.addItem("테이블에 데이터가 없습니다.")
        else:
            print("현재 입력된 데이터 없음")

    def display_data(self):
        query = "SELECT dr_name FROM doctor"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            self.dr_login.addItem(row[0])

    def on_combo_box_changed(self):
        selected_item = self.dr_login.currentText()
        print("현재 사용자: ", selected_item)

    def date_changed(self):
        selected_date = self.ex_date_box.currentText()
        # print("selected_date : ", selected_date)
        if selected_date:
            print("\n선택한 날짜: ", selected_date)
            query = "SELECT ex_id FROM examine where ex_date = %s"
            self.cursor.execute(query, (selected_date,))
            ex_id_result = self.cursor.fetchall()
            print("ex_id : ", [str(row[0]) for row in ex_id_result])

            query = "SELECT ex_diagnosis FROM diagnosis where ex_id = %s"
            self.cursor.execute(query, [str(row[0]) for row in ex_id_result])
            ex_diagnosis_result = self.cursor.fetchall()
            print("진단명 : ", [str(row[0]) for row in ex_diagnosis_result])
            table_data = "\n".join([str(row[0]) for row in ex_diagnosis_result])
            self.diagnosis_ex.setPlainText(table_data)
        else:
            print("선택된 날짜 없음")

    def dr_name_mark(self):
        selected_date = self.ex_date_box.currentText()
        if selected_date:
            query = "SELECT dr_id FROM examine where ex_date = %s"
            self.cursor.execute(query, (selected_date,))
            dr_id_result = self.cursor.fetchall()
            dr_id = [str(row[0]) for row in dr_id_result]

            query = "SELECT dr_name FROM doctor where dr_id = %s"
            self.cursor.execute(query, (dr_id[0],))
            dr_name_result = self.cursor.fetchall()
            result = [item[0] for item in dr_name_result]
            print("진단한 의사 이름 : ", result[0])
            self.dr_name_box.setPlainText(result[0])
        else:
            print("의사 이름 에러")

    def current_date_time(self):
        current_time = QDateTime.currentDateTime()
        current_time_format = current_time.toString("yyyy-MM-dd hh:mm:ss")
        self.current_date.setText(current_time_format)

    def popup(self):
        if self.search_pt.count()>0:
            diagnosis = self.input_diagnosis.toPlainText()
            input_string = self.search_pt.currentText()
            word_list = input_string.split()
            current_pt_id = word_list[0]

            current_dr_name = self.dr_login.currentText()
            if diagnosis and current_pt_id:
                print("진료 내용 : ", diagnosis)
                query = "SELECT pt_name, pt_birth, pt_sex FROM patient where pt_id = %s"
                self.cursor.execute(query, (current_pt_id,))
                result = self.cursor.fetchall()
                str_result = ""

                for i in result[0]:
                    str_result += str(i)
                    str_result += '\n'

                str_result += '\n'
                icheck = '\n\n진료 내용을 저장하시겠습니까?\n'

                buttonReply = QMessageBox.information(
                    self, '확인', "현재 사용자 : " + current_dr_name +
                                "\n\n<환자 정보>\n" + str_result +
                                "<진료 내용>\n" + diagnosis + icheck,
                                QMessageBox.Save | QMessageBox.Cancel
                )
                if buttonReply == QMessageBox.Save:
                    print('Save clicked.')
                    self.insert_examine()
                    QMessageBox.about(self, '  ', "저장되었습니다. ")
                    self.input_diagnosis.clear()
                elif buttonReply == QMessageBox.Cancel:
                    print('Cancel clicked.')
                    self.input_diagnosis.clear()
        else:
            print("입력 정보 없음")

    def insert_examine(self):
        input_string = self.search_pt.currentText()
        word_list = input_string.split()
        current_pt_id = word_list[0]
        current_dr_id = self.dr_login.currentText()

        query = "SELECT dr_id FROM doctor where dr_name = %s"
        self.cursor.execute(query, (current_dr_id,))
        dr_id_result = self.cursor.fetchall()
        dr_id = [str(row[0]) for row in dr_id_result]

        ex_sql = "INSERT INTO examine (dr_id, pt_id) VALUES (%s, %s)"
        self.cursor.execute(ex_sql, (int(dr_id[0]), int(current_pt_id)))
        self.conn.commit()

        query = "SELECT ex_id FROM examine where dr_id = %s AND pt_id = %s"
        self.cursor.execute(query, (int(dr_id[0]), int(current_pt_id)))
        ex_id_result = self.cursor.fetchall()
        ex_id = [int(row[0]) for row in ex_id_result]
        ex_id_max = max(ex_id)

        diagnosis = self.input_diagnosis.toPlainText()
        dig_sql = "INSERT INTO diagnosis (ex_id, ex_diagnosis) VALUES (%s, %s)"
        self.cursor.execute(dig_sql, (ex_id_max, diagnosis))
        self.conn.commit()
        self.choice_pt_name()

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
