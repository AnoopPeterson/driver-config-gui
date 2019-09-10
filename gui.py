import sys, json, os
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLineEdit, QComboBox, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import pyqtSlot

class MainWin(QWidget):

	top_offset = 100
	left_offset = 100
	width = 500
	height = 500

	json_data = {'wooo': 'test'}

	def __init__(self):
		super().__init__()
		self.json_data = self.load_json()
		self.init_gui()

	def init_gui(self):
		self.names = self.pull_names(self.json_data)

		# -- ADD NEW BUTTON CONFIG -- #

		# Init the basic window frame
		self.setWindowTitle('Driver/Gunner Profile Configuration')
		self.setGeometry(self.top_offset, self.left_offset, self.width, self.height)

		# Init controller select dropdown
		self.controller_type = QComboBox(self)
		self.controller_type.addItems(['Driver', 'Gunner'])

		# Init name dropdown
		self.controller_name = QComboBox(self)
		self.controller_name.addItems(self.names)
		
		# Init remote select dropdown
		self.remote_type = QComboBox(self)
		self.remote_type.addItems(['Xbox', 'Joystick'])

		# Init button mapping textbox -  I have decided to use 1 textbox, and leave the instructions inside the template
		self.map_name = QLineEdit(self)
		self.map_name.setText('Add new action')

		# Init submit button
		self.submit = QPushButton('Submit', self)
		self.new_map_info = [self.controller_type, self.controller_name, self.remote_type, self.map_name, self.submit]
		self.submit.clicked.connect(lambda: self.submit_new_config(self.new_map_info))


		# -- ADD NEW DRIVER CONFIG -- #

		# Init new driver type dropdown
		self.new_controller_type = QComboBox(self)
		self.new_controller_type.addItems(['Driver', 'Gunner'])

		# Init driver name textbox
		self.new_controller_name = QLineEdit(self)
		self.new_controller_name.setText('Enter new member\'s name') 

		# Init submit button
		self.add_new_driver = QPushButton('Submit', self)
		self.new_driver_info = [self.new_controller_type, self.new_controller_name, self.add_new_driver]
		self.add_new_driver.clicked.connect(lambda: self.submit_new_controller(self.new_driver_info))

		# Init save changes button:
		self.save_all_changes = QPushButton('Save All Changes', self)
		self.save_all_changes.clicked.connect(self.save_changes)
		self.grid = QGridLayout()
		self.grid.addWidget(self.widget_group(self.new_map_info, 'Add new Button Configuration'), 0, 0)
		self.grid.addWidget(self.widget_group(self.new_driver_info, 'Add new Member'), 1, 0)
		self.grid.addWidget(self.save_all_changes, 2, 0)
		self.setLayout(self.grid)

		self.show()

	# -- FUNCTIONS -- #

	# Wrapper function for loading JSON file
	def load_json(self):
		path = os.path.join(os.getcwd(), 'button_mappings.json')
		with open(path, 'r') as f:
			json_data = json.load(f)

		return json_data

	# Pulls out names for adding to dropdown list
	def pull_names(self, json_dict : dict):
		names = []
		for controller_type in json_dict:
			for name in json_dict[controller_type]:
				names.append(name)
		return names

	# Easy way of adding any number and type of widgets to grid layout
	def widget_group(self, widget_array : list, title : str):
		widget_group = QGroupBox(title)
		vbox = QVBoxLayout()
		
		for widget in widget_array:
			vbox.addWidget(widget)

		widget_group.setLayout(vbox)

		return widget_group

	@pyqtSlot(list)
	# Adds new drive team member
	def submit_new_controller(self, controller_info : list):
		# This is essentially a $_POST['type'] situation from PHP put into python
		POST = []

		# Formats the text values to make json file consistent
		for widget in controller_info:
			if type(widget) == QComboBox:
				widget_val = str(widget.currentText()).lower()
			if type(widget) == QLineEdit:
				widget_val = str(widget.text()).lower()

			# Won't append default values to POST
			if widget_val != "enter new member's name":
				POST.append(widget_val)

		# Adds driver info and basic driver info into dictionary based off controller type, IF all values are non-default
		if len(POST) >= 1:
			self.json_data[POST[0]][POST[1]] = {
				'xbox' : [],
				'joystick' : []
			}
		else:
			QMessageBox.about(self, 'Error when adding new member', 'Please enter a name for your member.')

	@pyqtSlot(list)

	# -- Submits new custom mapping.
	def submit_new_config(self, config_info : list):

		# This is essentially a $_POST['type'] situation from PHP put into python		
		POST = []

		# Formats user inputs to make json file easier to read
		for widget in config_info:
			if type(widget) == QComboBox:
				widget_val = str(widget.currentText()).lower()
			if type(widget) == QLineEdit:
				widget_val = str(widget.text()).lower()

			# Won't append default value to POST
			if widget_val != 'add new action': 
				POST.append(widget_val)

		# Adds new config to dictionary based off driver type, name, and type of HID, IF all values are non-default AND if action query is correctly formatted
		if len(POST) > 3 :
			map_vals = tuple(POST[3].split(': '))
			if len(map_vals) == 2:
				for map_tuple in self.json_data[POST[0]][POST[1]][POST[2]]:
					if map_tuple == map_vals:
						QMessageBox.about(self, 'Error when adding new configuration', 'That configuration already exists.')
						break
				self.json_data[POST[0]][POST[1]][POST[2]].append(map_vals)
			else:
				QMessageBox.about(self, 'Error when addding new configuration', 'Invalid format. \n Correct form: action_name: button_id')
		else:
			QMessageBox.about(self, 'Error when addding new configuration', 'Please enter action name and button id.')



	@pyqtSlot()
	# Saves all changes
	def save_changes(self):
		with open('button_mappings.json', 'w') as f:
			json.dump(self.json_data, f)
		QMessageBox.about(self, 'Save All Changes', 'Changes Saved.')

def main():
	app = QApplication(sys.argv)
	win = MainWin()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()