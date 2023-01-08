def OnRewind(app):
    print('<<')
    pass

def OnPlay(app):
    print('play')
    app.is_paused = not app.is_paused
    if app.is_paused is True:
        app.statusBar().showMessage("Paused!")
    else:
        app.statusBar().showMessage("Un-paused!")
    pass


def OnFastForward(app):
    print('>>')
    pass