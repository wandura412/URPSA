import platform
import subprocess
from PyQt5 import QtWidgets, QtGui
import sys
import os
CONFIG_FILE = "config.txt"
# Base Section class
class Section:
    def __init__(self, title, fields, parent_layout):
        self.group_box = QtWidgets.QGroupBox(title)
        self.layout = QtWidgets.QFormLayout()
        self.inputs = {}

        for field in fields:
            label, default, field_type = field["label"], field.get("default", ""), field.get("type", str)
            if field_type == "multiline":
                widget = QtWidgets.QPlainTextEdit()
                widget.setPlainText(default)
            elif field_type == "combo":
                widget = QtWidgets.QComboBox()
                widget.addItems(default)
            else:
                widget = QtWidgets.QLineEdit()
                widget.setText(default)
                if field_type == int:
                    widget.setValidator(QtGui.QIntValidator())
                elif field_type == float:
                    widget.setValidator(QtGui.QDoubleValidator())
            self.inputs[label] = widget
            self.layout.addRow(label, widget)

        self.group_box.setLayout(self.layout)
        parent_layout.addWidget(self.group_box)

    def get_values(self):
        values = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QtWidgets.QPlainTextEdit):
                values[key] = widget.toPlainText()
            elif isinstance(widget, QtWidgets.QComboBox):
                values[key] = widget.currentText()
            else:
                values[key] = widget.text()
        return values



class ConfigApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration Input")

        self.setGeometry(100, 100, 600, 600)

        self.scroll_area = QtWidgets.QScrollArea()
        self.tabs = QtWidgets.QTabWidget()
        self.scroll_area.setWidget(self.tabs)
        self.scroll_area.setWidgetResizable(True)
        self.sections = {}

        # General Tab
        self.general_tab = QtWidgets.QWidget()
        self.general_layout = QtWidgets.QVBoxLayout()

        self.sections["project"] = Section("project", [
            {"label": "Project Name", "default": "CH4-"}
        ], self.general_layout)

        self.sections["gaussian"] = Section("gaussian", [
            {"label": "Number of Cores", "default": "8", "type": int},
            {"label": "Memory", "default": "8GB"},
            {"label": "Method", "default": "#N opt(maxcycle=600,AddGIC) PM6 scf(maxcyc=600,xqc) nosymm"}
        ], self.general_layout)

        self.sections["molecules"] = Section("molecules", [

            {"label": "charge", "default": "-1", "type": int},
            {"label": "multiplicity", "default": "1", "type": int},
            {"label": "number_of_molecules", "default": "5", "type": int},
            {"label": "Molecule Data", "default": """0 = C 0.000 0.000 0.0000

1 = C 0.000 0.000 0.000

2 = C 0.000 0.0000 0.0000

3 = C 0.0000 0.00 0.000

4 = H 0.000 0.000 0.000 """, "type": "multiline"}
        ], self.general_layout)

        self.general_tab.setLayout(self.general_layout)
        self.tabs.addTab(self.general_tab, "General")

        # Advanced Tab
        self.advanced_tab = QtWidgets.QWidget()
        self.advanced_layout = QtWidgets.QVBoxLayout()

        self.sections["controls"] = Section("controls", [
            {"label": "Update with Optimized Coordinates", "default": "True"},
            {"label": "Step Size", "default": "0.1", "type": float},
            {"label": "Step Count", "default": "40", "type": int},
            {"label": "Stop Distance Factor", "default": "0.8", "type": float},
            {"label": "Stress Release", "default": "0:1:-1"},
            {"label": "Sphere Radius", "default": "3", "type": float},
            {"label": "N Iterations", "default": "10", "type": int},
            {"label": "Spherical Placement", "default": ["statistically_even", "random", "custom"], "type": "combo"},
            {"label": "Add COM Constraints", "default": "True"},
            {"label": "Add Spherical Constraints", "default": "False"},
            {"label": "Dynamic Fragment Replacement", "default": "False"},
            {"label": "Cutoff Energy Gap", "default": "3.0", "type": float},
            {"label": "Energy Surpass Options", "default": ["exit", "continue"], "type": "combo"},
            {"label": "Optimize the Final Particle", "default": "True"},
            {"label": "Convergence Error", "default": ["exit", "warn"], "type": "combo"},
            {"label": "unsuccessful_pathway", "default": ["archive", "delete"], "type": "combo"}
        ], self.advanced_layout)

        self.sections["Additional"] = Section("Additional", [
            {"label": "Additional Data", "default": "", "type": "multiline"}
        ], self.advanced_layout)

        self.advanced_tab.setLayout(self.advanced_layout)
        self.tabs.addTab(self.advanced_tab, "Advanced")

        # Preview Tab
        self.preview_tab = QtWidgets.QWidget()
        self.preview_layout = QtWidgets.QVBoxLayout()
        self.preview_text = QtWidgets.QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_layout.addWidget(self.preview_text)

        # Browse and Run Section
        self.browse_layout = QtWidgets.QHBoxLayout()
        self.file_path_input = QtWidgets.QLineEdit()
        self.file_path_input.setPlaceholderText("Select repeated.py")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_repeated_file)
        self.browse_layout.addWidget(self.file_path_input)
        self.browse_layout.addWidget(self.browse_button)
        self.preview_layout.addLayout(self.browse_layout)

        # Run Calculation Button
        self.run_button = QtWidgets.QPushButton("Run Calculation")
        self.run_button.clicked.connect(self.run_calculation)
        self.preview_layout.addWidget(self.run_button)

        self.save_button = QtWidgets.QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.preview_layout.addWidget(self.save_button)

        self.preview_tab.setLayout(self.preview_layout)
        self.tabs.addTab(self.preview_tab, "Preview")

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)

        # Submit button
        # self.submit_button = QtWidgets.QPushButton("Submit")
        # self.submit_button.clicked.connect(self.submit)
        # self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

        self.tabs.currentChanged.connect(self.show_preview)

    def submit(self):
        config_lines = []
        for section_name, section_obj in self.sections.items():

            config_lines.append(f"[{section_name}]")

            for key, value in section_obj.get_values().items():

                if section_name == "Additional" and value == "":
                        continue
                elif section_name == "molecules" and key == "Molecule Data":
                    config_lines.append(f"{value}")
                    continue
                config_lines.append(f"{key.replace(' ', '_').lower()} = {value}")


            config_lines.append("")
        self.preview_text.setText("\n".join(config_lines))

    def show_preview(self, index):
        if self.tabs.tabText(index) == "Preview":
            self.submit()

    def save_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Configuration File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.preview_text.toPlainText())
            self.input_file_path = file_path


    def select_repeated_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select repeated.py", "", "Python Files (*.py)")
        if file_path:
            self.file_path_input.setText(file_path)
            self.repeated_script_path = file_path
            self.save_repeated_file_path(file_path)

    def run_calculation(self):
        if not hasattr(self, 'input_file_path'):
            QtWidgets.QMessageBox.warning(self, "Error", "Please save the input file before running the calculation.")
            return

        if not hasattr(self, 'repeated_script_path'):
            QtWidgets.QMessageBox.warning(self, "Error", "Please select the repeated.py script before running the calculation.")
            return
        command = f'cd {self.input_file_path} && python3 "{self.repeated_script_path}" "{self.input_file_path}"'

        # have to change this self.repeated_script_path as it is comming from self.input_file_path

        if platform.system() == "Linux":
            if "g16" not in os.environ:
                print(f"path to g16 cant be found")

            subprocess.run(
                ['gnome-terminal', '--', 'bash', '-c', command])

        else:
            print("operating system is not Linux")


    def save_repeated_file_path(self, path):
        with open(CONFIG_FILE, "w") as file:
            file.write(path)

    def load_repeated_file_path(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                path = file.read().strip()
                self.file_path_input.setText(path)
                self.repeated_script_path = path


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ConfigApp()
    window.show()
    sys.exit(app.exec_())
