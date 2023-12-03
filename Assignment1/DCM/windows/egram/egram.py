from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QWidget, QMessageBox, QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries

class EgramWindow(QMainWindow):
    def __init__(self, stacked_window):
        super(EgramWindow, self).__init__()
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle('Egram')

        self.atrial_series = QLineSeries()
        self.ventricular_series = QLineSeries()

        self.chart = QChart()
        self.chart.addSeries(self.atrial_series)
        self.chart.addSeries(self.ventricular_series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.combo_box = QComboBox()
        self.combo_box.addItem('Atrial')
        self.combo_box.addItem('Ventricular')
        self.combo_box.addItem('Both')
        self.combo_box.currentIndexChanged.connect(self.switch_display)

        self.back_Button = QPushButton('Back')
        self.back_Button.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
        self.back_Button.setgeometry(25, 25, 100, 50)
        self.back_Button.clicked.connect(self.back_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.chart_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_data(self, atrial_data, ventricular_data):
        self.atrial_series.append(self.atrial_series.count(), atrial_data)
        self.ventricular_series.append(self.ventricular_series.count(), ventricular_data)
        self.chart.axisX(self.atrial_series).setRange(0, self.atrial_series.count())
        self.chart.axisY(self.atrial_series).setRange(min(self.atrial_series.pointsVector()), max(self.atrial_series.pointsVector()))
        self.chart.axisX(self.ventricular_series).setRange(0, self.ventricular_series.count())
        self.chart.axisY(self.ventricular_series).setRange(min(self.ventricular_series.pointsVector()), max(self.ventricular_series.pointsVector()))

    def switch_display(self):
        display_mode = self.combo_box.currentText()
        if display_mode == 'Atrial':
            self.atrial_series.setVisible(True)
            self.ventricular_series.setVisible(False)
        elif display_mode == 'Ventricular':
            self.atrial_series.setVisible(False)
            self.ventricular_series.setVisible(True)
        elif display_mode == 'Both':
            self.atrial_series.setVisible(True)
            self.ventricular_series.setVisible(True)

    def back_clicked(self): # if back button is clicked, show popup window
        self.stacked_window.setCurrentIndex(1)
        # clear stack
        self.stacked_window.removeWidget(self.stacked_window.widget(2))
        self.stacked_window.setWindowTitle("Landing Page")
