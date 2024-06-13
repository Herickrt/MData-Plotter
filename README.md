# MData-Plotter
MData-Plotter is a program for generating graphs, which gives the user the option to customize in a simple way.The program has a simple interface, with the aim of being practical for users.

For now, the program is run using the 'python3' command in the Linux terminal.

The main interface has a text box to indicate how many files will be submitted (Per hour, a maximum of 6).

About compatible file types:

- The files compatible with the program are .txt, .dat and .xy;
- Decimal numbers must be separated by dots;
- Columns are separated by space;

After submitting the data, a pop-up for customizing the lines will appear. There you can customize the line color, point marker, axis name, graph name and interval for each axis (optional).

About graph customization:
- Colors can be submitted in English (e.g. Blue) or in hexadecimal code (e.g. #0000FF).
- As the program was developed using Matplot, for plotting graphs, at the end of the customization pop-up there is the option "Matplot Códigos de Marcador", to see what types of markers are available for the points.
- There is the option to invert the file data columns, causing them to be automatically swapped at plot time.
- There is the option for you to define the maximum and minimum value of each axis, in addition to defining the range. If you don't want it, the graph will be generated with values ​​based on the data provided.

After submitting the options, you can plot your graph.
