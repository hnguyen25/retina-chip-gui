
def openSessionParams():
    session_dialog = QDialog()
    uic.loadUi("./src/gui/startup.ui", session_dialog)
    session_dialog.setWindowTitle("Set Session Parameters...")
    session_dialog.exec()