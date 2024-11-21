from pathlib import Path
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import altair as alt


def triangular_cdf(x, a, b, c):
    if x < a:
        return 0
    elif x <= c:
        return (x - a)**2 / ((c - a) * (b - a))
    elif x <= b:
        return 1 - (b - x)**2 / ((b - c) * (b - a))
    else:
        return 1


def determine_size(path, reliability, confidence_interval):
    sizes = []
    with open(path, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(sep=',')
            left = float(data[-1])
            mode = float(data[-2])
            right = float(data[-3])
            sigma = np.sqrt(left**2 + right**2 + mode**2 -
                              left*right - left*mode - right*mode)/(3*np.sqrt(2))
            mu = (left + mode + right) / 3
            percentile = 1 - (1 - reliability)/2
            x_values = np.linspace(left, right, int(10e6))
            cdf_values = [triangular_cdf(x, left, mode, right) for x in x_values]
            x_percentile = x_values[np.argmax(np.array(cdf_values) >= percentile)]
            z_score = (x_percentile - mu) / sigma
            size = int(np.ceil((z_score*sigma/confidence_interval)**2))
            sizes.append(size)

    return np.max(sizes)


def randomize_EAC(path, size):
    df = pd.DataFrame()
    with open(path, 'r+') as file:
        lines = file.readlines()
        for phase, line in enumerate(lines, start=1):
            data = line.split(sep=',')
            left = float(data[-1])
            mode = float(data[-2])
            right = float(data[-3])
            trng = np.random.default_rng().triangular(left, mode, right, size)
            df[f'fase_{phase}'] = trng

    return df.round(0)


def distribution_plot(df, maxbins):

    x_param = alt.X('EAC:Q', bin=alt.Bin(maxbins=maxbins), title='EAC')
    y_param = alt.Y('count():Q', title='SPI')

    chart = alt.Chart(df).mark_bar(
        # color="lightblue",
        # interpolate="step",
        # line=True
    ).encode(
        x=x_param,
        y=y_param,
        tooltip=[x_param, y_param]
    ).properties(
        width=600,
        height=400,
        title='Gráfico 1'
    )

    return chart


def add_redline(df, chart):

    x_param = alt.X('mean(EAC):Q')

    redline = alt.Chart(df).mark_rule(
        color="red"
    ).encode(
        x=x_param,
        tooltip=[x_param]
    )

    chart_with_redline = (chart + redline).properties(
        width=600,
        height=400,
        title='Gráfico 1'
    )
    return chart_with_redline


def main():

    data_path = '/mnt/c/Users/Diego/Desktop/mc/data.txt'

    size = determine_size(data_path, 0.95, 1)
    print(f'Iteraciones determinadas: {size}')

    df = randomize_EAC(data_path, size)
    df = pd.DataFrame(df.sum(axis=1), columns=['EAC'])
    print(round(df['EAC'].min(), 2))
    print(round(df['EAC'].max(), 2))

    triang_chart = distribution_plot(df, 50)
    chart = add_redline(df, triang_chart)
    chart.save('montecarlo.html')

main()
