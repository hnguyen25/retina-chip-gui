## 5.17.2022 (Huy)
- Made window assignment backend much more modular. Setting up charts no longer hard-coded.
- Created frontend for Litke-like minimap visualization
- Made new noise+spike finding (6x6) GUI layouts in Qt Designer, connected into GUI loading page
- Added extra documentation about getting started in wiki

## 5.12.2022 (Huy)
- Reverted to colored circles for array map, color bar correctly linked with it
- Hover over array map gives the correct values
- Created spike rate plot
- Spike rate based on average incoming spike count in each data chunk
- Developed four new GUI panes:
- **New session preferences:** initial settings to start analyzing datarun
  - streamlined way of choosing to load offline/realtime data
  - set spike threshold value from the beginning of session
  - choose file directory on startup
    
- **Individual Channel Analysis:** for looking at plots for individual channels
  - Convenient lookup of channels by number/row/col
- **Electrode List Analysis:** for displaying numerical data of electrodes in a sorted list
- **GUI preferences:** for persistent settings for the GUI not affected by datarun
- Set up github + github pages