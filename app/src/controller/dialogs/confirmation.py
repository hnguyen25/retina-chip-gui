from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel

class ConfirmationToStartNewSession(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New Session...")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Do you want to start a new session? This will reset the current visualization.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
