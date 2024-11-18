import math
import matplotlib.pyplot as plt


class MultiPlot:
    def __init__(
        self,
        dataset,
        shape=None,
        perfect_shape=False,
        square_shape=False,
        long=True,
        figsize=None
    ):
        """
        Type checks and init
        """

        if not (isinstance(dataset, list) or isinstance(dataset, dict)):
            raise TypeError(
                f"'dataset' must be of type 'list' or 'dict', you provided {type(dataset)}."
            )
        if shape:
            if not (isinstance(shape, tuple) or isinstance(shape, list)):
                raise TypeError(
                    f"'shape' must be of type 'tuple' or 'list', you provided {type(shape)}."
                )
            if len(shape) != 2:
                raise ValueError(
                    f"'shape' must have length = 2, you provided a shape with length = {len(shape)}."
                )
            if any(s == 0 for s in shape):
                raise ValueError(
                    f"Having a shape with a side equal to 0 makes no sense! You provided the shape {shape}"
                )
        if not isinstance(perfect_shape, bool):
            raise TypeError(
                f"'perfect_shape' must be of type 'bool', you provided {type(perfect_shape)}."
            )
        if not isinstance(square_shape, bool):
            raise TypeError(
                f"'square_shape' must be of type 'bool', you provided {type(square_shape)}."
            )
        if not isinstance(long, bool):
            raise TypeError(
                f"'long' must be of type 'bool', you provided {type(long)}."
            )
        if not figsize:
            if long:
                self.figsize = (12, 10)
            else:
                self.figsize = (10, 12)
        else:
            if not isinstance(figsize, tuple):
                raise TypeError(
                    f"'figsize' must be of type 'tuple', you provided {type(figsize)}."
                )
            else:
                self.figsize = figsize
        if isinstance(dataset, dict):
            self.dataset = dataset
        if isinstance(dataset, list):
            self.dataset = self._make_dataset_dict(dataset)
        self.n = len(self.dataset)
        self.perfect_shape = True if perfect_shape else False
        self.square_shape = True if square_shape else False
        self.long = True if long else False
        self.factors = self._get_factors()
        self.next_perfect_square = self._find_next_perfect_square(self.n)
        self.previous_perfect_square = self._find_previous_perfect_square(
            self.n)
        self.nearest_perfect_square = self._find_nearest_perfect_square()
        if not shape:
            self.shape = self._get_shape()
        else:
            self.shape = self._check_shape(shape)

    def _make_dataset_dict(self, dataset):
        """
        Creates a dict from the dataset in case the provided dataset was a list,
        each key will be used as the suptitle of it's corresponding value (dataset)
        """

        return {f"Plot {i + 1}": ds for i, ds in enumerate(dataset)}

    def _get_factors(self):
        """
        Finds all factors of a number
        """

        n = self.n
        return sorted(list(set(
            factor for i in range(1, int(n**0.5) + 1) if n % i == 0
            for factor in (i, n//i))), reverse=False)

    def _find_next_perfect_square(self, n):
        """
        Finds the next perfect sqare number
        """

        if int(math.sqrt(n)) ** 2 == n:
            return n
        else:
            return self._find_next_perfect_square(n + 1)

    def _find_previous_perfect_square(self, n):
        """
        Finds the previous perfect sqare number
        """

        if int(math.sqrt(n)) ** 2 == n:
            return n
        else:
            return self._find_previous_perfect_square(n - 1)

    def _find_nearest_perfect_square(self):
        """
        Finds the nearest (either previous or next) perfect square number
        """

        n = self.n
        prev_perf_sq = self.previous_perfect_square
        next_perf_sq = self.next_perfect_square
        p_dist = n - prev_perf_sq
        n_dist = next_perf_sq - n
        if n == prev_perf_sq == next_perf_sq:
            return n
        elif p_dist > n_dist:
            return next_perf_sq
        elif p_dist < n_dist:
            return prev_perf_sq

    def _get_shape(self):
        """
        Calculates the best shape based on provided parameters
        """

        n = self.n
        nearest_sq = self.nearest_perfect_square
        prev_sq = self.previous_perfect_square
        next_sq = self.next_perfect_square
        factors = self.factors
        if self.square_shape and self.perfect_shape:
            if n == nearest_sq:
                side = int(math.sqrt(n))
                return (side, side)
            else:
                raise ValueError(
                    f"""Can't create perfect square shape figure with given params -> n:{n} and
                    nearest_perfect_square:{nearest_sq}, dataset must have a perfect square len()""")
        elif self.perfect_shape:
            if len(factors) % 2 == 0:
                s1 = factors[:int(len(factors) / 2)][-1]
                s2 = factors[int(len(factors) / 2):][::-1][-1]
            else:
                s1 = factors[:int(len(factors) / 2) + 1][-1]
                s2 = factors[int(len(factors) / 2):][::-1][-1]
            if self.long:
                rows = s2
                cols = s1
                return (rows, cols)
            else:
                rows = s1
                cols = s2
                return (rows, cols)
        elif self.square_shape:
            if self.long:
                cols = int(math.sqrt(prev_sq))
                rows = cols + int(n - (cols * cols))
            else:
                rows = cols = int(math.sqrt(next_sq))
            return (rows, cols)
        else:
            raise TypeError(
                "If 'perfect_shape' and 'square_shape' are set to False, please provide a custom shape."
            )

    def _check_shape(self, shape):
        """
        Check wether the provided shape fits the rest of the passed arguements
        """

        n = self.n
        s1 = shape[0]
        s2 = shape[1]
        if s1 == s2:
            rows = cols = s1
        if self.long:
            if s1 > s2:
                rows = s1
                cols = s2
            else:
                rows = s2
                cols = s1
        else:
            if s1 > s2:
                rows = s2
                cols = s1
            else:
                rows = s1
                cols = s2
        if n > s1 * s2:
            raise ValueError(
                f"Can't fit dataset of length {n} in a figure with {rows} rows and {cols} columns! ({rows} x {cols} = {rows*cols})"
            )
        return (rows, cols)

    def dynamic_plot(
        self,
        plot_fn,
        single_legend=False,
        multiple_legends=False,
        legend_kwargs=None,
        **kwargs
    ):
        """
        Generate a grid of subplots using a provided plotting function, with options to
        customize legend behavior.

        This method creates subplots based on the shape of the dataset and applies a plotting function
        to each subplot. 
        The legend can be applied in two ways:
            - `single_legend`: Adds a legend to the last subplot only.
            - `multiple_legends`: Adds a legend to each subplot individually.
        
        You can customize the appearance of the legend using `legend_kwargs`, which should be a
        dictionary of keyword arguments to be passed directly to `ax.legend()`. If `legend_kwargs`
        is not provided, default legend settings will be applied.
        
        Parameters:
        -----------
        plot_fn : function
            A function that takes an axis (`ax`) and the data for a particular plot, and plots
            on the axis.  This function should accept `**kwargs` arguments for additional
            customizations.
        
        single_legend : bool, optional, default: False
            If True, adds a legend to the last subplot in the grid. This option is ignored
            if `multiple_legends` is True.
        
        multiple_legends : bool, optional, default: False
            If True, adds a legend to each subplot. This takes precedence over `single_legend`.

        legend_kwargs : dict, optional, default: None
            A dictionary of keyword arguments to be passed to `ax.legend()` for customizing
            the appearance of the legend(s) (e.g., location, font size, labels). If not provided, 
            default legend settings will be applied.
        
        **kwargs : keyword arguments, optional
            Additional keyword arguments passed to the `plot_fn` for further customization of the plot.

        Returns:
        --------
        fig : matplotlib.figure.Figure
            The figure object containing all subplots.
        
        axes : numpy.ndarray
            A 1D array of axes corresponding to the subplots, with one axis per item in the dataset.
        """

        # If multiple_legends set to True, set single_legend to False
        if multiple_legends: 
            single_legend = False

        # Get the shape of the subplots and size for the figure
        rows, cols = self.shape
        figsize = self.figsize

        # Initialize the figure and axes
        fig, axs = plt.subplots(rows, cols, figsize=figsize)
        axes = axs.ravel()

        # Initialize empty lists to collect the handles and labels for a single legend
        if single_legend:
            handles, labels = [], []

        # Iterate over each ax and plot using the provided function and specified kwargs
        for i, (title, data) in enumerate(self.dataset.items()):
            ax = axes[i]
            plot_fn(ax, data, **kwargs)
            ax.set_title(title)

            # Generate separate legend for each subplot if specified
            if multiple_legends:
                if legend_kwargs:
                    ax.legend(**legend_kwargs)
                else:
                    ax.legend()

            # Collect the unique handles and labels for each subplot
            if single_legend:
                for handle, label in zip(*ax.get_legend_handles_labels()):
                    if label not in labels:
                        handles.append(handle)
                        labels.append(label)

        # Generate a single legend with unique handles and labels
        if single_legend:
            if legend_kwargs:
                fig.legend(handles, labels, **legend_kwargs)
            else:
                fig.legend(handles, labels)

        # Remove unused axes
        for ax in axes[len(self.dataset):]:
            ax.remove()

        return fig, axes


class PlotFunctions:
    @ staticmethod
    def plot(ax, data):
        ax.plot(data)

    @ staticmethod
    def scatterplot(ax, data):
        ax.scatter(data[0], data[1])

    @ staticmethod
    def barplot(ax, data):
        ax.bar(data[0], data[1])

    @ staticmethod
    def histplot(ax, data):
        ax.hist(data)

    @ staticmethod
    def imshow(ax, data):
        ax.imshow(data, cmap='gray')

    @ staticmethod
    def boxplot(ax, data):
        ax.boxplot(data)

    @ staticmethod
    def violinplot(ax, data):
        ax.violinplot(data)
