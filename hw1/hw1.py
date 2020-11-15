import pymysql
from PyQt5.QtWidgets import *
import sys, datetime
import csv
import json
import xml.etree.ElementTree as ET

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='root', password='jeong5607', db=db, charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

    def updateExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='root', password='jeong5607', db=db, charset='utf8')

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit() #갱신할때는 커밋해줘야함. 데이터베이스 벨류 바꿔야되기때문
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:

    def selectPlayerUsingvalue(self, teamidValue, positionValue, nationValue, heightValue, heightM, weightValue, weightM):
        print(teamidValue, positionValue, nationValue, heightValue, heightM, weightValue, weightM)
        if positionValue == "미정" and nationValue =='대한민국':
            if teamidValue == "사용안함":
                sql = "SELECT * FROM player WHERE position IS NULL AND NATION IS NULL"
                paramsl = []
            else:
                sql = "SELECT * FROM player WHERE position IS NULL AND NATION IS NULL AND team_id = %s"
                paramsl = [teamidValue]
        elif positionValue == "미정":
            if teamidValue == "사용안함" and nationValue == "사용안함":
                sql = "SELECT * FROM player WHERE position IS NULL"
                paramsl = []
            elif teamidValue == "사용안함":
                sql = "SELECT * FROM player WHERE position IS NULL AND NATION = %s"
                paramsl = [nationValue]
            elif nationValue == "사용안함":
                sql = "SELECT * FROM player WHERE position IS NULL AND team_id = %s"
                paramsl = [teamidValue]
            else:
                sql = "SELECT * FROM player WHERE position IS NULL AND team_id = %s AND NATION = %s"
                paramsl = [teamidValue, nationValue]
        elif nationValue =='대한민국':
            if teamidValue == "사용안함" and positionValue == "사용안함":
                sql = "SELECT * FROM player WHERE NATION IS NULL"
                paramsl = []
            elif teamidValue == "사용안함":
                sql = "SELECT * FROM player WHERE NATION IS NULL AND position = %s"
                paramsl = [positionValue]
            elif positionValue == "사용안함":
                sql = "SELECT * FROM player WHERE NATION IS NULL AND team_id = %s"
                paramsl = [teamidValue]
            else:
                sql = "SELECT * FROM player WHERE NATION IS NULL AND team_id = %s AND position = %s"
                paramsl = [teamidValue, positionValue]

        elif teamidValue =="사용안함" and positionValue =="사용안함" and nationValue =="사용안함":
            sql = "SELECT * FROM player"
            paramsl = []
        elif teamidValue =='사용안함' and positionValue =="사용안함":
            sql = "SELECT * FROM player WHERE NATION = %s"
            paramsl = [nationValue]
        elif teamidValue =='사용안함' and nationValue =="사용안함":
            sql = "SELECT * FROM player WHERE position = %s"
            paramsl = [positionValue]
        elif positionValue =="사용안함" and nationValue =="사용안함":
            sql = "SELECT * FROM player WHERE team_id = %s"
            paramsl = [teamidValue]
        elif teamidValue =='사용안함':
            sql = "SELECT * FROM player WHERE position = %s AND NATION = %s"
            paramsl = [positionValue, nationValue]
        elif positionValue =='사용안함':
            sql = "SELECT * FROM player WHERE team_id = %s AND NATION = %s"
            paramsl = [teamidValue, nationValue]
        elif nationValue =='사용안함':
            sql = "SELECT * FROM player WHERE team_id = %s AND position = %s"
            paramsl = [teamidValue, positionValue]
        else:
            sql = "SELECT * FROM player WHERE team_id = %s AND position = %s AND NATION = %s"
            paramsl = [teamidValue,positionValue,nationValue]

        if heightValue == "사용안함" and weightValue == "사용안함":
            sql = sql
            paramsl = paramsl
        elif heightValue == "사용안함":
            if weightM=="이상":
                if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT>= %s"
                else:sql = sql + " AND WEIGHT>= %s"
                paramsl.append(weightValue)
            else:
                if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT<= %s"
                else:sql = sql + " AND WEIGHT<= %s"
                paramsl.append(weightValue)

        elif weightValue == "사용안함":
            if heightM=="이상":
                if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE HEIGHT>= %s"
                else:sql = sql + " AND HEIGHT>= %s"
                paramsl.append(heightValue)
            else:
                if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE HEIGHT<= %s"
                else:sql = sql + " AND HEIGHT<= %s"
                paramsl.append(heightValue)
        else:
            if weightM == "이상":
                if heightM =="이상":
                    if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT>= %s AND HEIGHT>= %s"
                    else:sql = sql + " AND WEIGHT>= %s AND HEIGHT>= %s"
                    paramsl.append(weightValue)
                    paramsl.append(heightValue)

                if heightM =="이하":
                    if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT>= %s AND HEIGHT<= %s"
                    else:sql = sql + " AND WEIGHT>= %s AND HEIGHT<= %s"
                    paramsl.append(weightValue)
                    paramsl.append(heightValue)
            elif weightM =="이하":
                if heightM == "이상":
                    if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT<= %s AND HEIGHT>= %s"
                    else:sql = sql + " AND WEIGHT<= %s AND HEIGHT>= %s"
                    paramsl.append(weightValue)
                    paramsl.append(heightValue)
                if heightM == "이하":
                    if (sql[len(sql) - 1] == "r"):sql = sql + " WHERE WEIGHT<= %s AND HEIGHT<= %s"
                    else:sql = sql + " AND WEIGHT<= %s AND HEIGHT<= %s"
                    paramsl.append(weightValue)
                    paramsl.append(heightValue)

        params2 = (tuple(paramsl))
        print(sql)
        print(params2)
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params2)
        return tuples
    ###############################
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의
    def selectPlayerTeamId(self):
        sql = "SELECT DISTINCT team_id FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerPosition(self):
        sql = "SELECT DISTINCT position FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerNation(self):
        sql = "SELECT DISTINCT NATION FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayermaxHeight(self):
        sql = "SELECT MAX(HEIGHT) FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)

        return tuples

    def selectPlayerminHeight(self):
        sql = "SELECT MIN(HEIGHT) FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)

        return tuples

    def selectPlayermaxWeight(self):
        sql = "SELECT MAX(WEIGHT) FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerminWeight(self):
        sql = "SELECT MIN(WEIGHT) FROM player"
        params = ()
        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples


##################################################

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # 윈도우 설정
        self.setWindowTitle("DBAPI를 통한 테이블 위젯 제어 예제")
        self.setGeometry(0, 0, 1100, 620)

        ##### 라벨 설정
        ##########팀명 TEAM_ID
        self.label1 = QLabel("팀명 :", self)
        self.label1.move(100, 50)
        self.label1.resize(100, 20)
        # 콤보스 설정
        self.comboBox1 = QComboBox(self)
        self.comboBox1.addItem("사용안함")
        self.teamidValue = self.comboBox1.currentText()

        ############포지션POSITION
        self.label2 = QLabel("포지션 :", self)
        self.label2.move(300, 50)
        self.label2.resize(100, 20)
        # 콤보스 설정
        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItem("사용안함")
        self.positionValue = self.comboBox2.currentText()

        ########## 출신국NATION
        self.label3 = QLabel("출신국 :", self)
        self.label3.move(500, 50)
        self.label3.resize(100, 20)
        # 콤보스 설정
        self.comboBox3 = QComboBox(self)
        self.comboBox3.addItem("사용안함")
        self.nationValue = self.comboBox3.currentText()
        ############ 키 HEIGHT
        self.label4 = QLabel("키 :", self)
        self.label4.move(100, 80)
        self.label4.resize(100, 20)
        # 콤보스 설정
        self.comboBox4 = QComboBox(self)
        self.comboBox4.addItem("사용안함")
        self.heightValue = self.comboBox4.currentText()



        #선택박스
        self.groupbox1 = QGroupBox(self)
        self.radioBtn1 = QRadioButton("이상")
        self.radioBtn1.setChecked(True)
        self.heightM = ("이상")
        self.radioBtn1.clicked.connect(self.comboBox_Activated)
        self.radioBtn2 = QRadioButton("이하")
        self.radioBtn2.clicked.connect(self.comboBox_Activated)
        hBox = QHBoxLayout()
        hBox.addWidget(self.radioBtn1)
        hBox.addWidget(self.radioBtn2)
        self.groupbox1.setLayout(hBox)
        self.groupbox1.move(230, 70)
        self.groupbox1.setStyleSheet("background-color:#f9f9f9;")

        ########## 몸무게 WEIGHT
        self.label5 = QLabel("몸무게 :", self)
        self.label5.move(400, 80)
        self.label5.resize(100, 20)
        # 콤보스 설정
        self.comboBox5 = QComboBox(self)
        self.comboBox5.addItem("사용안함")
        self.weightValue = self.comboBox5.currentText()
        #선택박스
        self.groupbox2 = QGroupBox(self)
        self.radioBtn3 = QRadioButton("이상")
        self.radioBtn3.setChecked(True)
        self.weightM = ("이상")
        self.radioBtn3.clicked.connect(self.comboBox_Activated)
        self.radioBtn4 = QRadioButton("이하")
        self.radioBtn4.clicked.connect(self.comboBox_Activated)
        hBox = QHBoxLayout()
        hBox.addWidget(self.radioBtn3)
        hBox.addWidget(self.radioBtn4)
        self.groupbox2.setLayout(hBox)
        self.groupbox2.move(550, 70)
        self.groupbox2.setStyleSheet("background-color:#f9f9f9;")

#############################################################
        query = DB_Queries()
        # DB 검색문 실행

        rows1 = query.selectPlayerTeamId()
        columnName = list(rows1[0].keys())[0]
        items1 = ['없음' if row[columnName] == None else row[columnName] for row in rows1]
        self.comboBox1.addItems(items1)

        rows2 = query.selectPlayerPosition()
        columnName = list(rows2[0].keys())[0]
        items2 = ['미정' if row[columnName] == None else row[columnName] for row in rows2]
        self.comboBox2.addItems(items2)

        rows3 = query.selectPlayerNation()
        columnName = list(rows3[0].keys())[0]
        items3 = ['대한민국' if row[columnName] == None else row[columnName] for row in rows3]
        self.comboBox3.addItems(items3)
        ###########키 최대최소 넣어주기 ###################
        rows4max = query.selectPlayermaxHeight()
        heightmax=0
        for sub in rows4max:
            for key in sub:
                heightmax = int(sub[key])
        rows4min = query.selectPlayerminHeight()
        heightmin = 0
        for sub in rows4min:
            for key in sub:
                heightmin = int(sub[key])

        for i in range(heightmin,heightmax+1):
            self.comboBox4.addItem(str(i))

        ###################몸무게 넣어주기##############
        rows5max = query.selectPlayermaxWeight()
        weightmax = 0
        for sub in rows5max:
            for key in sub:
                weightmax = int(sub[key])

        rows5min = query.selectPlayerminWeight()
        weightmin = 0
        for sub in rows5min:
            for key in sub:
                weightmin = int(sub[key])

        for i in range(weightmin, weightmax + 1):
            self.comboBox5.addItem(str(i))

        # ***- self.comboBox4.addItems(items)
        # ***- self.comboBox5.addItems(items)

        self.comboBox1.move(170, 50)
        self.comboBox1.resize(100, 20)
        self.comboBox1.activated.connect(self.comboBox_Activated)

        self.comboBox2.move(370, 50)
        self.comboBox2.resize(100, 20)
        self.comboBox2.activated.connect(self.comboBox_Activated)

        self.comboBox3.move(570, 50)
        # *** - self.comboBox3.move(170, 80)
        self.comboBox3.resize(100, 20)
        self.comboBox3.activated.connect(self.comboBox_Activated)

        self.comboBox4.move(130, 80)
        self.comboBox4.resize(100, 20)
        self.comboBox4.activated.connect(self.comboBox_Activated)

        self.comboBox5.move(450, 80)
        self.comboBox5.resize(100, 20)
        self.comboBox5.activated.connect(self.comboBox_Activated)

        # 푸쉬버튼(초기화버튼) 설정
        self.pushButton = QPushButton("초기화", self)
        self.pushButton.move(700, 40)
        self.pushButton. resize(100, 30)
        self.pushButton.clicked.connect(self.btnClear_Clicked)
        # 푸쉬버튼(검색버튼)  설정
        self.pushButton = QPushButton("검색", self)
        self.pushButton.move(700, 70)
        self.pushButton.resize(100, 30)
        self.pushButton.clicked.connect(self.pushButton_Clicked)

        #테이블위젯 설정
        self.tableWidget = QTableWidget(self)   # QTableWidget 객체 생성
        self.tableWidget.move(50, 120)
        self.tableWidget.resize(1000, 400)
        # self.tableWidget.move(50, 120)
        # self.tableWidget.resize(500, 400)

        #파일출력
        self.label6 = QLabel("파일 출력", self)
        self.label6.move(60, 550)
        self.label6.resize(100, 20)

        self.groupbox3 = QGroupBox(self)
        self.radioBtn5 = QRadioButton(" CSV")
        self.radioBtn5.setChecked(True)
        self.radioBtn5.clicked.connect(self.save_Activated)
        self.radioBtn6 = QRadioButton(" JSON")
        self.radioBtn6.clicked.connect(self.save_Activated)
        self.radioBtn7 = QRadioButton(" XML")
        self.radioBtn7.clicked.connect(self.save_Activated)
        hBox = QHBoxLayout()
        hBox.addWidget(self.radioBtn5)
        hBox.addWidget(self.radioBtn6)
        hBox.addWidget(self.radioBtn7)
        self.groupbox3.setLayout(hBox)
        self.groupbox3.move(70, 570)
        self.groupbox3.setStyleSheet("background-color:#f9f9f9;")

        self.pushButton = QPushButton("저장", self)
        self.pushButton.move(700, 580)
        self.pushButton.resize(100, 30)
        self.pushButton.clicked.connect(self.saveButton_Clicked)

    def height_radioBtn_Clicked(self):
        heightmsg = ""
        if self.radioBtn1.isChecked():
            heightmsg = "이상"
        elif self.radioBtn2.isChecked():
            heightmsg = "이하"

        return heightmsg


    def weight_radioBtn_Clicked(self):
        weightmsg = ""
        if self.radioBtn3.isChecked():
            weightmsg = "이상"
        elif self.radioBtn4.isChecked():
            weightmsg = "이하"

        return weightmsg

    def save_radioBtn_Clicked(self):
        savemsg = ""
        if self.radioBtn5.isChecked():
            savemsg = "CSV"
        elif self.radioBtn6.isChecked():
            savemsg = "JSON"
        elif self.radioBtn7.isChecked():
            savemsg = "XML"
        return savemsg

    def btnClear_Clicked(self):
        self.comboBox1.setCurrentIndex(0)
        self.comboBox2.setCurrentIndex(0)
        self.comboBox3.setCurrentIndex(0)
        self.comboBox4.setCurrentIndex(0)
        self.comboBox5.setCurrentIndex(0)
        self.radioBtn1.setChecked(True)
        self.radioBtn3.setChecked(True)
        self.radioBtn5.setChecked(True)
        QMessageBox.about(self, "", "초기화 되었습니다")
        self.tableWidget.clearContents()

    def comboBox_Activated(self):
        self.teamidValue = self.comboBox1.currentText()
        self.positionValue = self.comboBox2.currentText()  # positionValue를 통해 선택한 포지션 값을 전달
        self.nationValue = self.comboBox3.currentText()
        self.heightValue = self.comboBox4.currentText()
        self.weightValue = self.comboBox5.currentText()
        self.weightM = self.weight_radioBtn_Clicked()
        self.heightM = self.height_radioBtn_Clicked()

    def pushButton_Clicked(self):

        # DB 검색문 실행
        query = DB_Queries()
        players = query.selectPlayerUsingvalue(self.teamidValue,self.positionValue,self.nationValue,self.heightValue,self.heightM,self.weightValue,self.weightM)

        if players is not None:

            if len(players) != 0:

                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(len(players))
                self.tableWidget.setColumnCount(len(players[0]))
                columnNames = list(players[0].keys())
                self.tableWidget.setHorizontalHeaderLabels(columnNames)
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

                for rowIDX in range(len(players)):
                    player = players[rowIDX]
                    for k, v in player.items():
                        columnIDX = columnNames.index(k)
                        if columnIDX == 6:
                            if v == None: item = QTableWidgetItem("미정")
                            else: item = QTableWidgetItem(str(v))
                        elif columnIDX == 8:
                            if v == None: item = QTableWidgetItem("대한민국")
                            else: item = QTableWidgetItem(str(v))
                        else:
                            if v == None:continue
                            elif isinstance(v, datetime.date):      # QTableWidgetItem 객체 생성
                                item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                            else:
                                item = QTableWidgetItem(str(v))
                        self.tableWidget.setItem(rowIDX, columnIDX, item)

                print(item)
            else:
                QMessageBox.about(self, "", "검색된 데이터가 없습니다")
                self.tableWidget.clearContents()
        else:
            QMessageBox.about(self, "","검색된 데이터가 없습니다" )
            self.tableWidget.clearContents()

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def save_Activated(self):
        self.saveM = self.save_radioBtn_Clicked()

    def saveButton_Clicked(self):
        self.saveM = self.save_radioBtn_Clicked()
        query = DB_Queries()
        players = query.selectPlayerUsingvalue(self.teamidValue, self.positionValue, self.nationValue, self.heightValue,
                                               self.heightM, self.weightValue, self.weightM)

        if self.saveM == "CSV":
            if len(players) != 0:
                f = open('playersCSV.csv', 'w', encoding='utf-8', newline='')
                wr = csv.writer(f)

                columnNames = list(players[0].keys())
                print(columnNames)
                print()
                wr.writerow(columnNames)

                for rowIDX in range(len(players)):
                    row = list(players[rowIDX].values())
                    print(row)
                    wr.writerow(row)

                f.close()
                QMessageBox.about(self, "", "저장되었습니다")
            else:
                QMessageBox.about(self, "", "저장할 내용이 없습니다")

        elif self.saveM == "JSON":
            if len(players) != 0:
                for player in players:
                    for k, v in player.items():
                        if isinstance(v, datetime.date):
                            player[k] = v.strftime('%Y-%m-%d')  # 키가 k인 item의 값 v를 수정
                            print(player[k])
                print()

                newDict = dict(playerGK=players)  # 키가 playeGK이고 value가 players
                print(newDict)

                with open('playerJSON.json', 'w', encoding='utf-8') as f:
                    json.dump(newDict, f, indent=4, ensure_ascii=False)
                QMessageBox.about(self, "", "저장되었습니다")
            else:
                QMessageBox.about(self, "", "저장할 내용이 없습니다")

        elif self.saveM == "XML":
            if len(players) != 0:
                for player in players:
                    for k, v in player.items():
                        if isinstance(v, datetime.date):
                            player[k] = v.strftime('%Y-%m-%d')  # 키가 k인 item의 값 v를 수정

                newDict = dict(playerGK=players)
                print(newDict)

                tableName = list(newDict.keys())[0]
                tableRows = list(newDict.values())[0]

                rootElement = ET.Element('Table')
                rootElement.attrib['name'] = tableName

                for row in tableRows:
                    rowElement = ET.Element('Row')
                    rootElement.append(rowElement)

                    for columnName in list(row.keys()):
                        if row[columnName] == None:
                            rowElement.attrib[columnName] = ''
                        else:
                            rowElement.attrib[columnName] = row[columnName]

                        if type(row[columnName]) == int:
                            rowElement.attrib[columnName] = str(row[columnName])

                ET.ElementTree(rootElement).write('playerXML.xml', encoding='utf-8', xml_declaration=True)
                QMessageBox.about(self, "", "저장되었습니다")
            else:
                QMessageBox.about(self, "", "저장할 내용이 없습니다")

#########################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()