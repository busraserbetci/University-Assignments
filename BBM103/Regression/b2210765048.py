import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Union, List, Tuple

plt.style.use('fivethirtyeight')
blue = "#008fd5"
red = "#fa5138"
yellow = "#e6ae38"

desc = """
Please write the #TODO parts of the code to answer the questions. (80 points)
DO NOT change any code or comment or the name of the file or any variable name.
"""

def standard_units(any_numbers: Union[List[float], np.ndarray]) -> Union[List[float], np.ndarray]:
    """
    Convert any array of numbers to standard units.

    Parameters:
    any_numbers (array-like): An array of numerical values.

    Returns:
    array-like: An array of values in standard units.
    """
    return (any_numbers - np.mean(any_numbers)) / np.std(any_numbers)

def correlation(x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> float:
    """
    Calculate the Pearson correlation coefficient between two arrays.

    Parameters:
    x (array-like): First array of numbers.
    y (array-like): Second array of numbers.

    Returns:
    float: Pearson correlation coefficient, r, the mean of the products of column values in standard units.
    """
    return np.mean(standard_units(x) * standard_units(y))


def slope(x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> float:
    """
    Calculate the slope of the regression line.

    Parameters:
    x (array-like): Independent variable (predictor).
    y (array-like): Dependent variable (response).

    Returns:
    float: Slope of the regression line.
    """
    return correlation(x, y) * (np.std(y) / np.std(x))


def intercept(x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> float:
    """
    Calculate the intercept of the regression line.

    Parameters:
    x (array-like): Independent variable (predictor).
    y (array-like): Dependent variable (response).

    Returns:
    float: Intercept of the regression line.
    """
    return np.mean(y) - slope(x, y) * np.mean(x)


def fit(x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> Union[List[float], np.ndarray]:
    """
    Return the height of the regression line at each x value.

    Parameters:
    x (array-like): Independent variable (predictor).
    y (array-like): Dependent variable (response).

    Returns:
    array-like: Predicted values using the linear regression model.
    """
    # Fit a linear regression model
    coefficients = np.polyfit(x, y, 1)
    return np.polyval(coefficients, x)


def cubic_fit(x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> Union[List[float], np.ndarray]:
    """
    Return the height of the regression line for the cubic model at each x value.

    Parameters:
    x (array-like): Independent variable (predictor).
    y (array-like): Dependent variable (response).

    Returns:
    array-like: Predicted values using the cubic regression model.
    """
    coefficients = np.polyfit(x, y, 3)
    return np.polyval(coefficients, x)

def df_sample(table_df: pd.DataFrame) -> List[List[float]]:
    """
    Generate a sample of rows from the dataset. DO NOT change the random state.

    Parameters:
    table_df (DataFrame): The data.
    
    Returns:
    list: Randomly sampled rows (as a list element) containing "Number of Movies" and "Total Gross".
    """
    sampled_rows = table_df[["Number of Movies", "Total Gross"]].sample(n = 4, random_state= 45)
    sample = sampled_rows.values.tolist()
    return sample

def setup_plot(xlims = (5, 82), ylims = (2365, 4950)) -> None:
    """
    Set up the plot with specified x and y limits, figure size and x and y labels.

    Parameters:
    xlims (tuple, optional): x-axis limits (min, max). Default is (5, 82).
    ylims (tuple, optional): y-axis limits (min, max). Default is (2365, 4950).

    Returns:
    None
    """
    plt.figure(figsize=(5, 5))
    plt.xlabel("Number of Movies")
    plt.ylabel("Total Gross")
    plt.xlim(xlims)
    plt.ylim(ylims)


def plot_gross(table_df: pd.DataFrame, x: Union[List[float], np.ndarray]) -> None:
    """
    Plot the Total Gross scatter. Use the variable blue as color and label.

    Parameters:
    table_df (DataFrame): The data.
    x (array): x-values for plotting.

    Returns:
    None
    """
    y = table_df["Total Gross"]
    plt.scatter(x, y, color=blue, label="Total Gross")


def plot_linear_scatter(table_df: pd.DataFrame, x: Union[List[float], np.ndarray]) -> None:
    """
    Plot the Linear Model scatter. Use the variable red as color and label.

    Parameters:
    table_df (DataFrame): The data
    x (array): x-values for plotting.

    Returns:
    None
    """
    y = fit(x, table_df["Total Gross"])
    plt.scatter(x, y, color=red, label="Linear Model")


def plot_linear_line(xlims: Tuple[float, float], param_slope: float, param_intercept: float) ->None:
    """
    Calculate the corresponding y values for the line ends using the given slope and x-axis limits.
    Plot the Linear Model line.

    Parameters:
    xlims (tuple): x-axis limits (min, max) for the line plot.
    param_slope (float): Slope parameter for the Linear Model.
    param_intercept (float): Intercept parameter for the Linear Model.
    
    Returns:
    None
    """
    # y_lims = np.array([2420.232079301933, 3851.5023607222956]) # Known min, max for line plot.
    # Calculate the corresponding y values for the line ends using the given slope and x-axis limits.
    y_lims = param_slope * np.array(xlims) + param_intercept
    plt.plot(xlims, y_lims, color=red, label="Linear Model", lw=2)


def plot_cubic_scatter(table_df: pd.DataFrame, x: Union[List[float], np.ndarray]) -> None:
    """
    Plot the Cubic Model scatter. Use the variable yellow as color and label.

    Parameters:
    table_df (DataFrame): The data
    x (array): x-values for plotting.

    Returns:
    None
    """
    y = cubic_fit(x, table_df["Total Gross"])
    plt.scatter(x, y, color=yellow, label="Cubic Model")


def plot_cubic_line(xlims: Tuple[float, float], 
                    param_a: float, param_b: float, param_c: float, param_d: float) -> None:
    """
    Plot the Cubic Model line. Use the variable yellow as color and label.

    Parameters:
    xlims (tuple): x-axis limits (min, max) for the line plot.
    param_a (float): Coefficient 'a' for the Cubic Model.
    param_b (float): Coefficient 'b' for the Cubic Model.
    param_c (float): Coefficient 'c' for the Cubic Model.
    param_d (float): Coefficient 'd' for the Cubic Model.

    Returns:
    None
    """
    # Generate points for the cubic model line
    x_cubic = np.linspace(xlims[0], xlims[1], 100)
    y_cubic = param_a * (x_cubic ** 3) + param_b * (x_cubic ** 2) + param_c * x_cubic + param_d  # Evaluate the cubic model
    plt.plot(x_cubic, y_cubic, color=yellow, label="Cubic Model", lw=2)


def plot_linear_error(table_df: pd.DataFrame, param_slope: float, param_intercept: float) -> None:
    """
    Plot errors for the Linear Model by visualizing vertical lines representing the differences 
    between the actual data points and the corresponding points on the Linear Model line. 
    The errors are shown for a sample of data points randomly chosen from the dataset using df_sample().
    Use the color 'darkred', line width 2 and label.

    Parameters:
    table_df (DataFrame): The data.
    param_slope (float): Slope parameter for the Linear Model.
    param_intercept (float): Intercept parameter for the Linear Model.

    Returns:
    None
    """
    sample = df_sample(table_df)
    for x1, y1 in sample:
        plt.plot([x1, x1], [y1, param_slope * x1 + param_intercept], color='darkred', lw=2)
    plt.plot([], [], color='darkred', lw=2, label="Error")


def plot_cubic_error(table_df: pd.DataFrame, param_a: float, param_b: float, param_c: float, param_d: float) -> None:
    """
    Plot errors for the Cubic Model by visualizing vertical lines representing the differences 
    between the actual data points and the corresponding points on the Linear Model line. 
    The errors are shown for a sample of data points randomly chosen from the dataset using df_sample().
    Use the color 'darkred', line width 2 and label.

    Parameters:
    table_df (DataFrame): The data.
    param_a (float): Coefficient 'a' for the Cubic Model.
    param_b (float): Coefficient 'b' for the Cubic Model.
    param_c (float): Coefficient 'c' for the Cubic Model.
    param_d (float): Coefficient 'd' for the Cubic Model.

    Returns:
    None
    """
    sample = df_sample(table_df)
    for x1, y1 in sample:
        y_cubic_error = param_a * (x1 ** 3) + param_b * (x1 ** 2) + param_c * x1 + param_d
        plt.plot([x1, x1], [y1, y_cubic_error], color='darkred', lw=2)
    plt.plot([], [], color='darkred', lw=2, label="Cubic Error")


def handle_legend(count_true_values: float) -> None:
    """
    Handle the legend for the plot to the top right corner, if number of True values of the flags are more than one.
    Show the plot.
    
    Parameters:
    count_true_values (float): Number of True values of the flags.

    Returns:
    None
    """
    if count_true_values > 1:
        plt.legend(bbox_to_anchor = (1, 1))

    plt.show()


def plotting_selector(table_df: pd.DataFrame, if_plot_gross = True, if_plot_linear = False, if_plot_cubic = False, 
                      if_plot_linear_line = False, if_plot_cubic_line = False,
                      if_plot_linear_error = False, if_plot_cubic_error = False,
                      param_slope = 19.8788, param_intercept = 2281.0808,
                      param_a = -0.026360, param_b = 3.464395, param_c = -114.299361, param_d = 3773.465262) -> None:
    
    """
    A function to selectively plot various elements related to the dataset.

    Parameters:
    table_df (DataFrame): The data.
    if_plot_gross (bool, optional): Whether to plot the Total Gross scatter. Default is True.
    if_plot_linear (bool, optional): Whether to plot the Linear Model scatter. Default is False.
    if_plot_cubic (bool, optional): Whether to plot the Cubic Model scatter. Default is False.
    if_plot_linear_line (bool, optional): Whether to plot the Linear Model line. Default is False.
    if_plot_cubic_line (bool, optional): Whether to plot the Cubic Model line. Default is False.
    if_plot_linear_error (bool, optional): Whether to plot errors for the Linear Model. Default is False.
    if_plot_cubic_error (bool, optional): Whether to plot errors for the Cubic Model. Default is False.
    param_slope (float, optional): Slope parameter for the Linear Model. Default is the calculated slope.
    param_intercept (float, optional): Intercept parameter for the Linear Model. Default is the calculated intercept.
    param_a (float, optional): Coefficient 'a' for the Cubic Model. Default is the calculated 'a'.
    param_b (float, optional): Coefficient 'b' for the Cubic Model. Default is the calculated 'b'.
    param_c (float, optional): Coefficient 'c' for the Cubic Model. Default is the calculated 'c'.
    param_d (float, optional): Coefficient 'd' for the Cubic Model. Default is the calculated 'd'.

    Returns:
    None

    This function selectively plots various elements related to the dataset based on the provided parameters.
    """
    
    x = table_df["Number of Movies"]
    xlims = np.array([5, 82])

    setup_plot(xlims=xlims, ylims=(2365, 4950))

    if if_plot_gross:
        plot_gross(table_df, x)

    if if_plot_linear:
        plot_linear_scatter(table_df, x)

    if if_plot_cubic:
        plot_cubic_scatter(table_df, x)

    if if_plot_linear_line:
        plot_linear_line(xlims, param_slope, param_intercept)

    if if_plot_cubic_line:
        plot_cubic_line(xlims, param_a, param_b, param_c, param_d)

    if if_plot_linear_error:
        plot_linear_error(table_df, param_slope, param_intercept)

    if if_plot_cubic_error:
        plot_cubic_error(table_df, param_a, param_b, param_c, param_d)
    
    
    # Count the number of True values, if more than one plot exist then we need a legend
    count_true_values = sum([if_plot_gross, if_plot_linear, if_plot_cubic, 
                             if_plot_linear_line, if_plot_cubic_line,
                             if_plot_linear_error, if_plot_cubic_error])
    
    handle_legend(count_true_values)


def linear_rmse(table_df: pd.DataFrame, param_slope: float, param_intercept:float) -> None:
    """
    Calculate and display the root mean squared error (RMSE) for the linear regression model.
    You will use a precision of six decimal places while displaying.
    Additionally, it plots the linear model line and error lines based on the given slope and intercept.

    Parameters:
    table_df (DataFrame): The data.
    param_slope (float): Slope parameter for the linear model.
    param_intercept (float): Intercept parameter for the linear model.

    Returns:
    None

    This function calculates the RMSE for the linear regression model using the provided slope and intercept.
    It then plots the linear model line and error lines based on the given parameters.
    """
    x = table_df["Number of Movies"]
    y = table_df["Total Gross"]
    fitted = param_slope * x + param_intercept
    mse = np.mean((y - fitted) ** 2)
    print("Root mean squared error:", round(mse ** 0.5, 6))
    plotting_selector(table_df, if_plot_linear_line=True, if_plot_linear_error=True,
                      param_slope=param_slope, param_intercept=param_intercept)


def cubic_rmse(table_df: pd.DataFrame, a: float, b: float, c: float, d: float) -> None:
    """
    Calculate and display the root mean squared error (RMSE) for the cubic regression model.
    You will use a precision of six decimal places while displaying.
    Additionally, it plots the cubic model line and error lines based on the given cubic coefficients.

    Parameters:
    table_df (DataFrame): The data.
    a (float): Coefficient 'a' for the cubic model.
    b (float): Coefficient 'b' for the cubic model.
    c (float): Coefficient 'c' for the cubic model.
    d (float): Coefficient 'd' for the cubic model.

    Returns:
    None

    This function calculates the RMSE for the cubic regression model using the provided coefficients.
    It then plots the cubic model line and error lines based on the given coefficients.
    """
    x = table_df["Number of Movies"]
    y = table_df["Total Gross"]
    fitted = a * x**3 + b * x**2 + c * x + d
    mse = np.mean((y - fitted) ** 2)
    print("Root mean squared error:", mse ** 0.5)
    plotting_selector(table_df, if_plot_cubic_line = True, if_plot_cubic_error = True)


def read_csv(csv_file: str) -> pd.DataFrame:
    """
    Reads an actors CSV file, processes the DataFrame, and prints the length
    and the first few rows of the DataFrame. While processing select the columns
    "Number of Movies" and "Total Gross" and the two into a copy of another DataFrame


    Parameters:
    csv_file (str): Path to the CSV file.

    Returns:
    pandas.DataFrame: A new DataFrame (not a slice) containing selected columns.

    Example Prints:
    Len: 10
        Number of Movies	Total Gross
    0	41	4871.7
    1	69	4772.8
    2	61	4468.3
    3	44	4340.8
    4	53	3947.3
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Select the columns "Number of Movies" and "Total Gross"
    selected_columns = df[["Number of Movies", "Total Gross"]].copy()

    # Print the length and the first few rows of the DataFrame
    print("Len:", len(selected_columns))
    print(selected_columns.head())

    return selected_columns


def print_and_return_slope_and_intercept(table_df: pd.DataFrame) -> Union[float, float]:
    """
    This function calculates and prints the slope and intercept of a linear regression line
    using the least squares method for a given DataFrame. Calculate the slope and intercept.
    Print the slope and intercept values with a precision of four decimal places.

    Parameters:
    table_df (pandas.DataFrame): DataFrame containing 'Number of Movies' and 'Total Gross' columns.

    Returns:
    slope (float) : the slope of a linear regression line.
    intercept (float): the intercept of a linear regression line.

    Example:
    print_slope_and_intercept(table_df)
    Slope: 300.0000, Intercept: 20000.0000
    """
    x = table_df["Number of Movies"]
    y = table_df["Total Gross"]

    slope_value, intercept_value = np.polyfit(x, y, 1)
    print("Slope: %.4f, Intercept: %.4f" %(slope_value, intercept_value))

    return slope_value, intercept_value


def print_and_return_coefficients(table_df: pd.DataFrame) -> Union[float, float, float, float]:
    """
    This function calculates and prints the coefficients of a cubic regression line
    using the least squares method for a given DataFrame. Calculate the coefficients a, b, c, d.
    Print the the a, b, c, d values with a precision of six decimal places.

    Parameters:
    table_df (pandas.DataFrame): DataFrame containing 'Number of Movies' and 'Total Gross' columns.

    Returns:
    a (float): Coefficient 'a' for the cubic regression line.
    b (float): Coefficient 'b' for the cubic regression line.
    c (float): Coefficient 'c' for the cubic regression line.
    d (float): Coefficient 'd' for the cubic regression line.

    Example:
    print_coefficients(table_df)
    a: -0.026360, b: 3.464395, c: -114.299361, d: 3773.465262
    """
    x = table_df["Number of Movies"]
    y = table_df["Total Gross"]

    # Fit a cubic regression line using numpy's polyfit
    coefficients = np.polyfit(x, y, 3)

    # Extract coefficients
    a, b, c, d = coefficients

    # Print coefficients with precision of six decimal places
    print(f"a: {a:.6f}, b: {b:.6f}, c: {c:.6f}, d: {d:.6f}")

    return coefficients


def prediction_and_error_columns(table_df: pd.DataFrame) -> None:
    """
    Adds prediction and error columns named as Linear Prediction, Cubic Prediction, Linear Error, Cubic Error
    to the provided DataFrame based on linear and cubic fits.

    Parameters:
    table_df (pandas.DataFrame): DataFrame containing 'Number of Movies', 'Total Gross' columns.

    Returns:
    None
    """
    # Calculate predictions and errors for linear model
    linear_pred = fit(table_df["Number of Movies"], table_df["Total Gross"])
    linear_error = table_df["Total Gross"] - linear_pred

    # Calculate predictions and errors for cubic model
    cubic_pred = cubic_fit(table_df["Number of Movies"], table_df["Total Gross"])
    cubic_error = table_df["Total Gross"] - cubic_pred

    # Add columns to the DataFrame
    table_df["Linear Prediction"] = linear_pred
    table_df["Cubic Prediction"] = cubic_pred
    table_df["Linear Error"] = linear_error
    table_df["Cubic Error"] = cubic_error
