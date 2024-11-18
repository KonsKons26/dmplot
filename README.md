# dmplot: A Python Package for Dynamic Multiple Plot Generation

**dmplot** is a Python package designed to facilitate the creation of multiple subplots arranged in a grid-like fashion without having to stress over making the subplots fit in a grid. It provides a simple interface for generating various types of plots from datasets, with customizable layouts, simple preset plotting functions and the ability to use custom plotting functions.

**CHECK OUT THE NOTEBOOK FOR A SIMPLE GUIDE AND EXAMPLES!!!!**


## Features

- Automatically creates a grid layout for multiple subplots.
- Flexible customization of grid shape (square, long, or perfect fit).
- Predefined plotting functions for quick use.
- Support for custom plotting functions.
- Easy legend customization across subplots or for the entire figure.

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

## Example Usecase

```python
import numpy as np
import matplotlib.pyplot as plt
from dmplot import MultiPlot, PlotFunctions

n = 6
dataset = [np.random.standard_exponential(10_000) for _ in range(n)]
mp = MultiPlot(dataset, perfect_shape=True, figsize=(8, 6))
fig, axes = mp.dynamic_plot(PlotFunctions.plot)

colors = "rgbykm"
[line.set_color(colors[i]) for i, ax in enumerate(axes) for line in ax.get_lines()]

plt.tight_layout()
plt.show()
```