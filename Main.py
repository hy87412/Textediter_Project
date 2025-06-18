import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction,
                             QFileDialog, QMessageBox, QInputDialog)
from PyQt5.QtGui import QIcon, QFont


class Textediter(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = self.load_settings()
        self.font_size = settings["font_size"]
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setFont(QFont("Consolas", self.font_size))

        self.create_actions()
        self.create_menu()

        self.statusBar().showMessage("Ready")
        self.text_edit.textChanged.connect(self.update_status_bar)

        self.setWindowTitle("Textediter")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QTextEdit {
                    background-color: #1e1e1e;
                    color: #dcdcdc;
                    border: none;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #3c3f41;
                }
                QMenu {
                    background-color: #3c3f41;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #505357;
                }
                QStatusBar{
                    color: white;
                }
            """)
        self.show()

    def create_actions(self):
        self.new_action = QAction("new file", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.exit_action = QAction("quit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)

        self.fontsize_action = QAction("set font size", self)
        self.fontsize_action.triggered.connect(self.set_font_size)



    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("file")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        settings_menu = self.menuBar().addMenu("settings")
        settings_menu.addAction(self.fontsize_action)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "open file")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_edit.setPlainText(text)
            except Exception as e:
                QMessageBox.warning(self, "error", f"can't open this file : {e}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "save file")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    text = self.text_edit.toPlainText()
                    file.write(text)
            except Exception as e:
                QMessageBox.warning(self, "error", f"can't save this file : {e}")

    def set_font_size(self):
        size, ok = QInputDialog.getInt(self, "Set Font Size", "Enter font size:", value=self.font_size, min=8, max=48)
        if ok:
            self.font_size = size
            self.text_edit.setFont(QFont("Consolas", self.font_size))
            self.save_settings()
            self.statusBar().showMessage(f"Font size set to {size}")

    def load_settings(self):
        default_settings = {"font_size"}
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    return settings
            except Exception:
                return default_settings
        else:
            return default_settings

    def save_settings(self):
        settings = {"font_size": self.font_size}
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"failed to save settings : {e}")

    def update_status_bar(self):
        text = self.text_edit.toPlainText()
        byte_count = len(text.encode('utf-8'))
        self.statusBar().showMessage(f"byte : {byte_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Textediter()
    sys.exit(app.exec_())