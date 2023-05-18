light_theme_colors = {
    "background": '#FFFFFF',
    "button": "#ECEFF4",
    'dark1': '#2E3440',
    'dark2': '#3B4252',
    'dark3': '#434C5E',
    'dark4': '#4C566A',
    'light1': '#ECEFF4',
    'light2': '#E5E9F0', # '#'
    'light3': '#D8DEE9', # '#'
    'blue1': '#5E81AC',
    'blue2': '#81A1C1',
    'blue3': '#88C0D0',
    'blue4': '#8FBCBB',
    'red': '#BF616A',
    'orange': '#D08770',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'purple': '#B48EAD',
    'spikeHighlighting' : '#FFEF00',
    'tracePlotting' : 'k'
}

dark_theme_colors = {
    "background_color": '#1e2030',
    "background_borders": '#222436',
    "font_color": '#ffffff',
    "button": '#4C566A',

    'spikeHighlighting' : '#EBCB8B',
    'tracePlotting': '#08F7FE',
    'dark1': '#2E3440',
    'dark2': '#3B4252',
    'dark3': '#434C5E',
    'dark4': '#4C566A',
    'light1': '#ECEFF4',
    'light2': '#E5E9F0',  # '#'
    'light3': '#D8DEE9',  # '#'
    'blue1': '#5E81AC',
    'blue2': '#81A1C1',
    'blue3': '#88C0D0',
    'blue4': '#8FBCBB',
    'red': '#BF616A',
    'orange': '#D08770',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'purple': '#B48EAD',
    'spikeHighlighting': '#FFEF00',
    'tracePlotting': 'k'
}
themes = {
    'light': light_theme_colors,
    'dark': dark_theme_colors
}

def update_theme(app, new_theme):
    print('update_theme()')
    app.settings["current_theme"] = new_theme
    background_color = themes[new_theme]["background_color"]
    background_border = themes[new_theme]["background_borders"]
    app.setStyleSheet("background-color: " + background_border)

    for chart in app.charts.keys():
        chart_type = type(app.charts[chart])
        if str(chart_type) == "<class 'pyqtgraph.widgets.PlotWidget.PlotWidget'>":
            app.charts[chart].setBackground(background_color)
        elif chart_type is list:
            for chart in app.charts[chart]:
                chart.setBackground(background_color)

    for window in app.external_windows:
        window.update_theme(app.settings["current_theme"], themes)

def toggle_dark_mode(app):
    if app.settings["current_theme"] == "light":
        app.update_theme("dark")
    elif app.settings["current_theme"] == "dark":
        app.update_theme("light")