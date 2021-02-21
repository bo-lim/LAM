
now = datetime.now().strftime('%Y-%m-%d_%H%M')


class stat_app(QDialog):

    def __init__(self):
        super().__init__()
        self.setVisible(True)
        self.student_stat = None
        self.class_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.time_class = None
        self.initUI()

    def initUI(self):
        print("stat_app initUI로 들어옴")
        grid = QGridLayout()
        self.setLayout(grid)

        x, y, z = final_output()
        self.get_info(x, y, z)

        # Graph drawing
        self.fig = plt.Figure()
        ax = self.fig.add_subplot(111)
        ax.set_title(ex.className + "\n" + now + "\n" + "Class Attention Guage")
        ax.set_xlabel('Time(divided by 10)')
        ax.set_ylabel('Guage')
        self.time_class = list(range(len(self.class_stat)))
        ax.plot(self.time_class, self.class_stat, label='Class Attention Guage')
        self.canvas = FigureCanvas(self.fig)

        # Student stat printing
        self.stat_tb = QTableWidget(self)
        self.stat_tb.setRowCount(len(self.student_stat))
        self.stat_tb.setColumnCount(3)
        self.set_stat_table()

        # Layout
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)
        grid.addWidget(QLabel('Final Stat'), 0, 0)
        grid.addLayout(leftLayout, 1, 0)
        grid.addWidget(QLabel('Student Stat'), 0, 1)
        grid.addWidget(self.stat_tb, 1, 1)

        # Add export button
        btn = QPushButton('Export', self)
        grid.addWidget(btn, 2, 1)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.export_clicked)

        self.setWindowTitle('Final Result Data')
        self.setWindowIcon(QIcon("Pictures/LAM로고.png"))
        self.setGeometry(500, 400, 1015, 700)
        self.show()

        # setting up student table

    def set_stat_table(self):
        column_headers = ['name', 'score', 'reaction']
        row = 0
        print("set_stat_table 정보")
        print(self.student_stat)
        self.stat_tb.setHorizontalHeaderLabels(column_headers)
        for key, value in self.student_stat.items():
            self.stat_tb.setItem(row, 0, QTableWidgetItem(key))
            self.stat_tb.setItem(row, 1, QTableWidgetItem(str(value[0])))
            self.stat_tb.setItem(row, 2, QTableWidgetItem(str(value[1])))
            row += 1

        # if export button is clicked,
        # student stat .csv // class graph .jpg
        # are exported

    def get_info(self, st_stat, class_score, c_stat):
        print("get_info 정보")
        print(st_stat)
        print(class_score)
        print(c_stat)
        self.student_stat = st_stat
        self.class_stat = c_stat
        print("self 정보")
        print(self.student_stat)
        print(self.class_stat)

    def export_clicked(self):
        print("Export 버튼의 정보")
        print(self.class_stat)
        print(self.student_stat)
        f = open(ex.className + '_csv' + now + '_result.csv', 'w', encoding="UTF-8")
        f.write('time' + ',' + 'avg' + '\n')
        row = 0
        for value, row in zip(self.class_stat, range(len(self.class_stat))):
            f.write(str(row) + ',' + str(value) + '\n')
        f.write('\n')

        f.write('name' + ',' + 'score' + ',' + 'reaction' + '\n')
        for key, value in self.student_stat.items():
            f.write(key + ',' + str(value[0]) + ',' + str(value[1]) + '\n')
        f.close()
        self.fig.savefig(ex.className + '_jpg' + now + '_graph.jpg')