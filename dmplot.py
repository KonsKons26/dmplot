import math
import matplotlib.pyplot as plt


class MultiPlot:
    def __init__(self, dataset, shape=None, perfect_shape=False, square_shape=False, long=True, figsize=None):
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
        return {f"Plot {i + 1}": ds for i, ds in enumerate(dataset)}

    def _get_factors(self):
        n = self.n
        return sorted(list(set(
            factor for i in range(1, int(n**0.5) + 1) if n % i == 0
            for factor in (i, n//i))), reverse=False)

    def _find_next_perfect_square(self, n):
        if int(math.sqrt(n)) ** 2 == n:
            return n
        else:
            return self._find_next_perfect_square(n + 1)

    def _find_previous_perfect_square(self, n):
        if int(math.sqrt(n)) ** 2 == n:
            return n
        else:
            return self._find_previous_perfect_square(n - 1)

    def _find_nearest_perfect_square(self):
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
                    f"Can't create perfect square shape figure with given params -> n:{n} and nearest_perfect_square:{nearest_sq}, dataset must have a perfect square len()")
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

    def dynamic_plot(self, plot_fn):
        rows, cols = self.shape
        figsize = self.figsize

        fig, axs = plt.subplots(rows, cols, figsize=figsize)
        axes = axs.ravel()

        for i, (title, data) in enumerate(self.dataset.items()):
            ax = axes[i]
            plot_fn(ax, data)
            ax.set_title(title)

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
        ax.imshow(data, cmap='grey')

    @ staticmethod
    def boxplot(ax, data):
        ax.boxplot(data)

    @ staticmethod
    def violinplot(ax, data):
        ax.violinplot(data)
