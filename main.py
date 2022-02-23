import PyQt5.QtWidgets as Qtwid
from functools import partial


class MainWindow(Qtwid.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        #  self.setFixedSize(500, 500)
        self.setLayout(Qtwid.QVBoxLayout())
        self.keypad()
        self.text = ''  # значение для помощи выводу на экран
        self.temp_numb = []
        self.show()

    def keypad(self):
        container = Qtwid.QWidget()
        container.setLayout(Qtwid.QGridLayout())

        # textfield
        self.field = Qtwid.QLineEdit('0')
        # self.field.setEnabled(False)
        self.field.setReadOnly(True)
        container.layout().addWidget(self.field, 0, 0, 1, 4)

        # buttons
        names = ['', '', '', '',
                 'Enter', '', 'Clear', '',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '', '+', '', ]

        positions = [(i, j) for i in range(6) for j in range(4)]
        # создание сетки кнопок
        for position, name in zip(positions, names):
            if name == '':
                continue
            elif name in ('Enter', 'Clear', '0', '+'):
                button = Qtwid.QPushButton(name)
                button.clicked.connect(partial(self.display_field, name))
                container.layout().addWidget(button, *position, 1, 2)
            else:
                button = Qtwid.QPushButton(name)
                button.clicked.connect(partial(self.display_field, name))
                container.layout().addWidget(button, *position)
        self.layout().addWidget(container)  # отображение кнопок контейнера

    def show_error(self):
        dialog = Qtwid.QMessageBox()
        dialog.setStyle(Qtwid.QStyleFactory.create('Fusion'))
        dialog.setWindowTitle('Error')
        dialog.setText('Делить на ноль нельзя!\nРезультат будет обнулён')
        dialog.exec()

    # триггеры для каждой из кнопок
    def display_field(self, name):
        if name == 'Clear':
            self.text = ''
            self.temp_numb.clear()
            self.field.setText('0')
        elif name == 'Enter':
            self.temp_numb.append(self.text)
            self.logic()
        elif name in ('-', '+', '*', '/'):
            self.temp_numb.append(self.text)
            # проверка на то, что уже записано в темп и замена знака
            if self.temp_numb[-1].isnumeric():
                self.temp_numb.append(name)
            elif self.temp_numb[-2] in ('-', '+', '*', '/'):
                self.temp_numb[-2] = name
                self.temp_numb.pop()
            self.text = ''
        else:
            self.text += name
            self.field.setText(self.text)

    # логика вычислений + определения вычислений
    def logic(self):
        numbers = []
        operations = []
        for i in range(len(self.temp_numb)):
            if self.temp_numb[i].isnumeric():
                numbers.append(int(self.temp_numb[i]))
            else:
                operations.append(self.temp_numb[i])
        accum = numbers.pop(0)
        for i in range(len(numbers)):
            if operations[i] == '+':
                accum += numbers[i]
            elif operations[i] == '-':
                accum -= numbers[i]
            elif operations[i] == '/':
                if numbers[i] == 0:
                    self.show_error()
                    accum = ''
                else:
                    accum /= numbers[i]
            elif operations[i] == '*':
                accum *= numbers[i]
        self.field.setText(str(accum))
        self.text = ''
        self.temp_numb.clear()
        self.display_field(str(accum))


app = Qtwid.QApplication([])
mw = MainWindow()
app.setStyle(Qtwid.QStyleFactory.create('Fusion'))
app.exec_()
