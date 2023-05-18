def pause_trace_updating(plot_widget, i):
    print("pause!!!", i)
    plot_widget.getPlotItem().axes['left']['item'].showLabel(show=False)
    plot_widget.setBackground("white")
