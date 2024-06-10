# dmplot: A Python Package for Dynamic Multiple Plot Generation

MultiPlot is a Python package designed to facilitate the creation of multiple plots arranged in a grid-like fashion without having to stress over making the subplots fit in a grid. It provides a simple interface for generating various types of plots from datasets, with customizable layouts, simple preset plotting functions and the ability to use custom plotting functions.

**CHECK OUT THE NOTEBOOK FOR A SIMPLE GUIDE!!!!**

## MultiPlot attributes

- dataset:
  - \<list> of array like data or
  - \<dict> of {key (will be used as the title of the subplot): array like data} pairs
- shape:
  - \<tuple> describing the shape of the grid (rows x columns)
- perfect_shape:
  - \<bool>, if True, the resulting gird will have no empty spaces.
- square_shape:
  - \<bool>, if True, the grid will try to form a square shape (rows = columns)
- long:
  - \<bool>, if True, rows > columns, if False, rows < columns
- figsize:
  - \<tuple>, if not specified, will be set to (12, 10) if long=True, or (10, 12) if long=False.

## PlotFunctions class

Containts several simple plotting functions to save you from the hassle of creating your own plot functions. Passed inside the dynamic_plot() method of the MultiPlot class.

- plot(ax, data)
- scatterplot(ax, data)
- barplot(ax, data)
- histplot(ax, data)
- imshow(ax, data)
- boxplot(ax, data)
- violinplot(ax, data)