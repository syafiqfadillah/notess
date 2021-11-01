import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, 
	QPushButton, QGridLayout, QTextEdit, QDialog, QTabWidget, QFileDialog
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

		self.actionSave_As.triggered.connect(self.save_as_data)
		self.actionSave_As.triggered.connect(self.save_enabled)

		self.actionLoad.triggered.connect(self.load_data)
		self.actionLoad.triggered.connect(self.saves_enabled)

		self.actionAdd_Tab.triggered.connect(self.add_tab)
		self.actionAdd_Tab.triggered.connect(self.save_as_enabled)

		self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
		self.tabWidget.tabCloseRequested.connect(self.delete_data_tab)
		self.tabWidget.tabCloseRequested.connect(self.saves_disabled)

	@staticmethod
	def check_folder_exist(name):
		return name not in os.listdir(os.getcwd())

	def add_note(self, index, text_default=""):
		layout = self.interfaces[index][0]

		layout.addWidget(QTextEdit(text_default), self.interfaces[index][-1], 0)

		self.interfaces[index][-1] += 1

		layout.addWidget(layout.itemAt(self.interfaces[index][-1]-1).widget(), self.interfaces[index][-1], 0)

	def save_data(self):
		for key in self.interfaces.keys():

			if self.tabWidget.tabText(key) not in os.listdir(self.current_path):
				self.create_folder(f"{self.current_path}\\{self.tabWidget.tabText(key)}")

			layout = self.interfaces[key][0]

			for widget_index in range(layout.count()):
				widget = layout.itemAt(widget_index).widget()
				if not isinstance(widget, QPushButton):
					with open(f"{self.current_path}/{self.tabWidget.tabText(key)}/text_{widget_index}.txt", "w") as e:
						e.write(f"{widget.toPlainText()}\n")

	def save_as_data(self):
		self.current_path = QFileDialog.getExistingDirectory(self, 'Select Folder')

		if self.current_path:
			self.create_folder(self.current_path.split("/")[-1])

			self.save_data()

	def load_data(self):
		self.current_path = QFileDialog.getExistingDirectory(self, 'Select Folder')

		if self.current_path:
			for index, folder in enumerate(os.listdir(self.current_path)):
				self.tabWidget.addTab(self.create_layout(), folder)
				for file in os.listdir(f"{self.current_path}\\{folder}"):
					with open(f"{self.current_path}\\{folder}\\{file}", "r") as w:
						self.add_note(index, w.read())

	def save_as_enabled(self):
		if self.tabWidget.count() > 0:
			self.actionSave_As.setEnabled(True)

	def save_enabled(self):
		self.actionSave.setEnabled(True)

	def saves_enabled(self):
		self.save_as_enabled()
		self.save_enabled()

	def saves_disabled(self):
		if not self.tabWidget.count():
			self.actionSave.setEnabled(False)
			self.actionSave_As.setEnabled(False)

	def create_folder(self, name):
		if self.check_folder_exist(name.split("\\")[-1]):
			os.mkdir(name)

	def delete_data_tab(self, key):
		del self.interfaces[key]

		self.interfaces = {index: self.interfaces[key] for index, key in enumerate(self.interfaces.keys())}

	def add_tab(self):		
		addTab = CustomDialog()

		if addTab.exec_() and addTab.get_text():
			self.tabWidget.addTab(self.create_layout(), addTab.get_text())

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
		pushButton_1.clicked.connect(lambda: self.add_note(self.tabWidget.currentIndex()))
		gridLayout.addWidget(pushButton_1, 0, 0, 1, 1)

		# update interfaces
		self.interfaces[addSumTab] = [gridLayout, pushButton_1, 0]
		
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