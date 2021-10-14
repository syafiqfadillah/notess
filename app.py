import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QPushButton, QGridLayout, QTextEdit, QDialog, QTabWidget
)

from gui.layout import Ui_MainWindow
from gui.dialog import Ui_Dialog


class CustomDialog(QDialog, Ui_Dialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

	def get_text(self):
		return self.lineEdit.text()


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.interfaces = {}

		self.actionSave.triggered.connect(self.save_data)

		self.actionLoad.triggered.connect(self.load_data)

		self.actionAdd_Tab.triggered.connect(self.add_tab)
		self.actionAdd_Tab.triggered.connect(self.buttons_connect)

		self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
		self.tabWidget.tabCloseRequested.connect(self.delete_data_tab)

	def buttons_connect(self):
		for key in self.interfaces.keys():
			if not self.interfaces[key][2]:
				self.interfaces[key][1].clicked.connect(lambda: self.add_note(self.tabWidget.currentIndex()))
				self.interfaces[key][2] = True

	def add_note(self, index, text_default=""):
		layout = self.interfaces[index][0]

		layout.addWidget(QTextEdit(text_default), self.interfaces[index][-1], 0)

		self.interfaces[index][-1] += 1

		layout.addWidget(layout.itemAt(self.interfaces[index][-1]-1).widget(), self.interfaces[index][-1], 0)
		
	def save_data(self):
		self.create_folder("data")

		for layout_keys in self.interfaces.keys():

		
			self.create_folder(fr"data\\{self.tabWidget.tabText(layout_keys)}")

			layout = self.interfaces[layout_keys][0]

			for widget_index in range(layout.count()):
				widget = layout.itemAt(widget_index).widget()
				if not isinstance(widget, QPushButton):
					with open(fr"data\\{self.tabWidget.tabText(layout_keys)}\text_{widget_index}.txt", "w") as e:
						e.write(f"{widget.toPlainText()}\n")

	def load_data(self):
		for index, folder in enumerate(os.listdir("data")):
			self.tabWidget.addTab(self.create_layout(), folder)
			for file in os.listdir(fr"data\\{folder}"):
				with open(f"data\\{folder}\\{file}", "r") as w:
					self.add_note(index, w.read())

	def check_folder_exist(self, name):
		return name not in os.listdir(os.getcwd())

	def create_folder(self, name):
		if self.check_folder_exist(name.split("\\")[-1]):
			os.mkdir(name)

	def delete_data_tab(self, key):
		del self.interfaces[key]

		self.interfaces = {index: self.interfaces[key] for index, key in enumerate(self.interfaces.keys())}

	def add_tab(self):		
		tabName = CustomDialog()

		if tabName.exec_() and tabName.get_text():
			self.tabWidget.addTab(self.create_layout(), tabName.get_text())

	def create_layout(self):
		addSumTab = self.tabWidget.count()

		layout = QWidget()
		layout.setObjectName(f"tab_{addSumTab}")

		verticalLayout = QVBoxLayout(layout)
		verticalLayout.setObjectName(f"verticalLayout_{addSumTab}")

		scrollArea = QScrollArea(layout)
		scrollArea.setWidgetResizable(True)
		scrollArea.setObjectName(f"scrollArea_{addSumTab}")

		scrollAreaWidgetContents = QWidget()
		scrollAreaWidgetContents.setGeometry(QRect(0, 0, 456, 413))
		scrollAreaWidgetContents.setObjectName(f"scrollAreaWidgetContents_{addSumTab}")

		gridLayout = QGridLayout(scrollAreaWidgetContents)
		gridLayout.setObjectName(f"gridLayout_{addSumTab}")

		pushButton_1 = QPushButton("+", scrollAreaWidgetContents)
		pushButton_1.setObjectName(f"pushButton_{addSumTab}")
		gridLayout.addWidget(pushButton_1, 0, 0, 1, 1)

		# update interfaces
		self.interfaces[addSumTab] = [gridLayout, pushButton_1, False, 0]
		
		scrollArea.setWidget(scrollAreaWidgetContents)
		
		verticalLayout.addWidget(scrollArea)

		return layout


def main():
	app = QApplication(sys.argv)

	app.setStyle("Fusion")

	window = MainWindow()
	window.show()

	app.exec()


if __name__ == "__main__":
	main()