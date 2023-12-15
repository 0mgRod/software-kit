import requests
import zipfile
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog

# List of programs with their GitHub repo URLs and installation directories
programs_to_install = [
    {
        "name": "Program 1",
        "url": "https://github.com/username/repo1/archive/main.zip",
        "install_dir": "C:/Program Files/Program1"
    },
    {
        "name": "Program 2",
        "url": "https://github.com/username/repo2/archive/main.zip",
        "install_dir": "D:/Projects/Program2"
    }
    # Add more programs similarly
]

class ProgramInstaller(QWidget):
    def __init__(self, programs):
        super().__init__()
        self.programs = programs
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Program Installer')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.url_label = QLabel('Select Program:')
        self.url_input = QLineEdit()
        self.url_input.setReadOnly(True)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.install_dir_label = QLabel('Installation Directory:')
        self.install_dir_input = QLineEdit()
        self.install_dir_button = QPushButton('Browse')
        self.install_dir_button.clicked.connect(self.browse_install_dir)
        layout.addWidget(self.install_dir_label)
        layout.addWidget(self.install_dir_input)
        layout.addWidget(self.install_dir_button)

        self.desktop_icon_checkbox = QCheckBox('Create Desktop Icon')
        layout.addWidget(self.desktop_icon_checkbox)

        self.install_button = QPushButton('Install')
        self.install_button.clicked.connect(self.install_program)
        layout.addWidget(self.install_button)

        self.populate_programs_dropdown()  # Populate programs dropdown
        self.setLayout(layout)

    def browse_install_dir(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Installation Directory')
        if directory:
            self.install_dir_input.setText(directory)

    def populate_programs_dropdown(self):
        for program in self.programs:
            self.url_input.addItem(program['name'])

    def download_and_install(self, selected_program, install_dir, create_desktop_icon):
        program = next((p for p in self.programs if p['name'] == selected_program), None)
        if program:
            response = requests.get(program['url'])
            file_name = os.path.basename(program['url'])
            zip_file_path = f'temp_{file_name}'

            with open(zip_file_path, 'wb') as file:
                file.write(response.content)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)

            os.remove(zip_file_path)

            if create_desktop_icon:
                # Code to create desktop shortcut (not implemented)

    def install_program(self):
        selected_program = self.url_input.currentText()
        install_dir = self.install_dir_input.text()
        create_desktop_icon = self.desktop_icon_checkbox.isChecked()

        if install_dir and selected_program:
            self.download_and_install(selected_program, install_dir, create_desktop_icon)
            print("Installation complete.")
        else:
            print("Please provide a valid installation directory.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgramInstaller(programs_to_install)
    window.show()
    sys.exit(app.exec_())