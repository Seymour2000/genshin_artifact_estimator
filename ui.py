from PyQt6 import QtCore, QtWidgets
from mainwindow import Ui_MainWindow
from core import SYW, Feature
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import seaborn as sns

class PressWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, control=None):
        super().__init__(parent)
        self.control = control
        self.setGeometry(QtCore.QRect(0, 190, 341, 191))
        self.setObjectName("widget_plot_2")
        #self.setMouseTracking(True)
    def mousePressEvent(self, event):
        pos_x = event.pos().x()
        self.control.mark(pos_x)
    def mouseMoveEvent(self, event):
        pos_x = event.pos().x()
        self.control.mark(pos_x)


class UI(Ui_MainWindow):
    def __init__(self, main_window):
        super().setupUi(main_window)
        self.widget_plot_3 = PressWidget(parent=self.groupBox_3, control=self)
        self.feature_cursor = 0
        self.nextIsNone = False
        self.check_button()
        self.pushButton_feature_0.clicked.connect(self.change_cursor_0)
        self.pushButton_feature_1.clicked.connect(self.change_cursor_1)
        self.pushButton_feature_2.clicked.connect(self.change_cursor_2)
        self.pushButton_feature_3.clicked.connect(self.change_cursor_3)
        self.pushButton_feature_4.clicked.connect(self.change_cursor_4)
        for i in range(10):
            exec('self.horizontalSlider_{}.valueChanged.connect(self.show_{})'.format(i+1, i+1))
        for i in range(10):
            exec('self.lineEdit_{}.editingFinished.connect(self.set_{})'.format(i+1, i+1))

        self.pushButton_reset_weights.clicked.connect(self.reset_weights)

        self.pushButton_select_1.clicked.connect(lambda: self.select_feature(self.pushButton_select_1.text()))
        self.pushButton_select_2.clicked.connect(lambda: self.select_feature(self.pushButton_select_2.text()))
        self.pushButton_select_3.clicked.connect(lambda: self.select_feature(self.pushButton_select_3.text()))
        self.pushButton_select_4.clicked.connect(lambda: self.select_feature(self.pushButton_select_4.text()))
        self.pushButton_select_5.clicked.connect(lambda: self.select_feature(self.pushButton_select_5.text()))
        self.pushButton_select_6.clicked.connect(lambda: self.select_feature(self.pushButton_select_6.text()))
        self.pushButton_select_7.clicked.connect(lambda: self.select_feature(self.pushButton_select_7.text()))
        self.pushButton_select_8.clicked.connect(lambda: self.select_feature(self.pushButton_select_8.text()))
        self.pushButton_select_9.clicked.connect(lambda: self.select_feature(self.pushButton_select_9.text()))
        self.pushButton_select_10.clicked.connect(lambda: self.select_feature(self.pushButton_select_10.text()))
        self.pushButton_select_11.clicked.connect(lambda: self.select_feature(self.pushButton_select_11.text()))

        self.pushButton_features_reset.clicked.connect(self.reset_feature)
        self.horizontalSlider_level.valueChanged.connect(self.show_level)
        self.lineEdit_level.editingFinished.connect(self.set_level)

        self.pushButton_current_score.clicked.connect(self.current_score)

        self.pushButton_estimation.clicked.connect(self.estimation)

        self.fig_1 = plt.figure()
        #self.fig_1.patch.set_facecolor('grey')
        #self.fig_1.patch.set_alpha(0.11)
        plt.tight_layout()
        self.canvas_1 = FigureCanvas(self.fig_1)
        self.canvas_2 = FigureCanvas(self.fig_1)
        layout_1 = QtWidgets.QVBoxLayout(self.widget_plot_1)
        layout_1.addWidget(self.canvas_1)
        layout_2 = QtWidgets.QVBoxLayout(self.widget_plot_2)
        layout_2.addWidget(self.canvas_2)

        self.verticalSlider.valueChanged.connect(self.smooth)
        self.data = None


    def set_fig_para(self):
        plt.tick_params(width=0.5, labelsize=6, direction='in')
        #ax = self.fig_1.add_axes((0.1, 0.15, 0.9, 0.85))

    def smooth(self):
        if self.data == None:
            return
        elif len(self.data[0]) <= 1:
            return
        else:
            data_len = len(self.data[1])
            smooth_data = [0]*data_len
            degree = self.verticalSlider.value()
            half_degree = int((degree-1)/2)
            for i in range(half_degree):
                smooth_value = 0
                for j in range(2*i+3):
                    smooth_value += self.data[1][j]
                #smooth_data[i] = smooth_value/(2*i+3)
                smooth_data[i] = smooth_value / degree
            for i in range(half_degree, data_len-half_degree-2):
                smooth_value = 0
                for j in range(i-half_degree, i-half_degree+degree):
                    smooth_value += self.data[1][j]
                smooth_data[i] = smooth_value/degree
            for i in range(data_len-half_degree-2, data_len):
                smooth_value = 0
                for j in range(2*i-data_len+1, data_len):
                    smooth_value += self.data[1][j]
                #smooth_data[i] = smooth_value/((data_len-i)*2-1)
                smooth_data[i] = smooth_value / degree
            #self.fig_1.clear()
            plt.cla()
            plt.fill_between(x=self.data[2], y1=smooth_data, facecolor='r', alpha=0.1)
            self.set_fig_para()
            sns.lineplot(x=self.data[2], y=smooth_data)
            self.canvas_1.draw()

    def mark(self, pos_x):
        if (self.data is None) or pos_x < 60 or pos_x > 289:
            return
        data_len = len(self.data[0])
        mark_pos = int((pos_x-60)/230*data_len)
        plt.cla()
        self.set_fig_para()
        plt.fill_between(x=self.data[2], y1=self.data[0], facecolor='b', alpha=0.1)
        sns.lineplot(x=self.data[2], y=self.data[0])
        mark_x = self.data[2][mark_pos]
        mark_y = self.data[0][mark_pos]
        plt.scatter(mark_x, mark_y)
        plt.annotate(text='({}, {:.2})'.format(int(mark_x), mark_y), xy=(mark_x, mark_y), xytext=(-20, +10), textcoords='offset points', fontsize=9)
        self.canvas_2.draw()

    def invalid_inputs(self, syw):
        num = 0
        for i in syw.features:
            if i is None:
                num += 1
                if num > 1:
                    return True
        if syw.level >= 20:
            self.current_score()
            return True
        return False

    def estimation(self):
        feature = self.export_feature()
        syw = self.export_syw()
        if self.invalid_inputs(syw):
            self.data = None
            self.fig_1.clear()
            self.canvas_1.draw()
            self.canvas_2.draw()
            self.textBrowser_expactation.setText(None)
            return
        self.data = syw.distribution(feature, simulation_times=10000)

        plt.cla()
        plt.fill_between(x=self.data[2],y1=self.data[1], facecolor='r', alpha=0.1)
        self.set_fig_para()
        sns.lineplot(x=self.data[2],y=self.data[1])
        self.canvas_1.draw()

        plt.cla()
        plt.fill_between(x=self.data[2], y1=self.data[0], facecolor='b', alpha=0.1)
        self.set_fig_para()
        sns.lineplot(x=self.data[2], y=self.data[0])
        self.canvas_2.draw()

        self.textBrowser_expactation.setText('%.2f' % self.data[3])
        standard = [30,35,40,45,50,55]
        chance = [0]*len(standard)
        for i in range(len(standard)):
            if standard[i] < self.data[2][0]:
                chance[i] = 1
            elif standard[i] > self.data[2][-1]:
                chance[i] = 0
            else:
                chance[i] = self.data[0][int((standard[i] - self.data[2][0]) * 10)]
        for i in range(len(standard)):
            self.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem('%.2f' % chance[i]))
        self.verticalSlider.setRange(1, max(1, int(len(self.data[2])/20)))
        self.verticalSlider.setValue(1)
        self.current_score()

    def current_score(self):
        feature = self.export_feature()
        syw = self.export_syw()
        score = syw.score(feature)
        self.pushButton_current_score.setText("%.2f" % score)

    def trans_value(self, text):
        if text == '':
            return 0
        else:
            try:
                value = float(text)
            except:
                return 0
            else:
                return value


    def export_feature(self):

        feature = Feature(self.trans_value(self.lineEdit_1.text()),
                          self.trans_value(self.lineEdit_2.text()),
                          self.trans_value(self.lineEdit_3.text()),
                          self.trans_value(self.lineEdit_7.text()),
                          self.trans_value(self.lineEdit_4.text()),
                          self.trans_value(self.lineEdit_5.text()),
                          self.trans_value(self.lineEdit_6.text()),
                          self.trans_value(self.lineEdit_8.text()),
                          self.trans_value(self.lineEdit_9.text()),
                          self.trans_value(self.lineEdit_10.text()))
        return feature

    def translate(self, ui_str):
        ui_list = ['小生命','小防御','小攻击','大生命','大防御','大攻击','元素精通','充能效率','暴击率','暴击伤害','无','']
        code_list = ['HP', 'DEF', 'ATK', 'HP_Rate', 'DEF_Rate', 'ATK_Rate', 'Element_Mastery', 'Energy_Recharge', 'CRIT_Rate', 'CRIT_DMG', None, None]
        code_str = code_list[ui_list.index(ui_str)]
        return code_str

    def export_syw(self):
        syw = SYW(self.translate(self.pushButton_feature_0.text()),
                  self.trans_value(self.lineEdit_level.text()),
                  self.translate(self.pushButton_feature_1.text()),
                  self.translate(self.pushButton_feature_2.text()),
                  self.translate(self.pushButton_feature_3.text()),
                  self.translate(self.pushButton_feature_4.text()),
                  self.trans_value(self.lineEdit_value_1.text()),
                  self.trans_value(self.lineEdit_value_2.text()),
                  self.trans_value(self.lineEdit_value_3.text()),
                  self.trans_value(self.lineEdit_value_4.text()),
                  )
        return syw

    def reset_feature(self):
        for i in range(4):
            exec('self.lineEdit_value_{}.setText("")'.format(i+1))
        for i in range(5):
            exec('self.pushButton_feature_{}.setText("")'.format(i))
        self.pushButton_current_score.setText("")
        self.change_cursor_0()
        self.horizontalSlider_level.setValue(0)
        self.lineEdit_level.setText('')

    def select_feature(self, feature_str):
        exec('self.pushButton_feature_{}.setText(feature_str)'.format(self.feature_cursor))
        exec('self.nextIsNone = (self.pushButton_feature_{}.text() == "")'.format(min(4, self.feature_cursor+1)))
        if self.nextIsNone:
            cursor = min(4, self.feature_cursor+1)
            exec('self.change_cursor_{}()'.format(cursor))

    def check_button(self):
        for i in range(5):
            exec('self.pushButton_feature_{}.setChecked(False)'.format(i))
        exec('self.pushButton_feature_{}.setChecked(True)'.format(self.feature_cursor))

    def reset_weights(self):
        for i in range(10):
            exec('self.horizontalSlider_{}.setValue(0)'.format(i+1))
            exec('self.lineEdit_{}.setText("")'.format(i+1))

    def change_cursor_0(self):
        self.feature_cursor = 0
        self.check_button()
    def change_cursor_1(self):
        self.feature_cursor = 1
        self.check_button()
    def change_cursor_2(self):
        self.feature_cursor = 2
        self.check_button()
    def change_cursor_3(self):
        self.feature_cursor = 3
        self.check_button()
    def change_cursor_4(self):
        self.feature_cursor = 4
        self.check_button()

    def show_level(self):
        self.lineEdit_level.setText(str(self.horizontalSlider_level.value()))

    def show_1(self):
        self.lineEdit_1.setText(str(self.horizontalSlider_1.value()/100))
    def show_2(self):
        self.lineEdit_2.setText(str(self.horizontalSlider_2.value()/100))
    def show_3(self):
        self.lineEdit_3.setText(str(self.horizontalSlider_3.value()/100))
    def show_4(self):
        self.lineEdit_4.setText(str(self.horizontalSlider_4.value()/100))
    def show_5(self):
        self.lineEdit_5.setText(str(self.horizontalSlider_5.value()/100))
    def show_6(self):
        self.lineEdit_6.setText(str(self.horizontalSlider_6.value()/100))
    def show_7(self):
        self.lineEdit_7.setText(str(self.horizontalSlider_7.value()/100))
    def show_8(self):
        self.lineEdit_8.setText(str(self.horizontalSlider_8.value()/100))
    def show_9(self):
        self.lineEdit_9.setText(str(self.horizontalSlider_9.value()/100))
    def show_10(self):
        self.lineEdit_10.setText(str(self.horizontalSlider_10.value()/100))

    def set_level(self):
        value = max(min(int(self.lineEdit_level.text()),20),0)
        self.lineEdit_level.setText(str(value))
        self.horizontalSlider_level.setValue(value)

    def set_1(self):
        try:
            value = max(min(float(self.lineEdit_1.text()),1),0)
        except:
            value = 0
        self.lineEdit_1.setText(str(value))
        self.horizontalSlider_1.setValue(int(value*100))
    def set_2(self):
        try:
            value = max(min(float(self.lineEdit_2.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_2.setText(str(value))
        self.horizontalSlider_2.setValue(int(value*100))
    def set_3(self):
        try:
            value = max(min(float(self.lineEdit_3.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_3.setText(str(value))
        self.horizontalSlider_3.setValue(int(value*100))
    def set_4(self):
        try:
            value = max(min(float(self.lineEdit_4.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_4.setText(str(value))
        self.horizontalSlider_4.setValue(int(value*100))
    def set_5(self):
        try:
            value = max(min(float(self.lineEdit_5.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_5.setText(str(value))
        self.horizontalSlider_5.setValue(int(value*100))
    def set_6(self):
        try:
            value = max(min(float(self.lineEdit_6.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_6.setText(str(value))
        self.horizontalSlider_6.setValue(int(value*100))
    def set_7(self):
        try:
            value = max(min(float(self.lineEdit_7.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_7.setText(str(value))
        self.horizontalSlider_7.setValue(int(value*100))
    def set_8(self):
        try:
            value = max(min(float(self.lineEdit_8.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_8.setText(str(value))
        self.horizontalSlider_8.setValue(int(value*100))
    def set_9(self):
        try:
            value = max(min(float(self.lineEdit_9.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_9.setText(str(value))
        self.horizontalSlider_9.setValue(int(value*100))
    def set_10(self):
        try:
            value = max(min(float(self.lineEdit_10.text()), 1), 0)
        except:
            value = 0
        self.lineEdit_10.setText(str(value))
        self.horizontalSlider_10.setValue(int(value*100))

