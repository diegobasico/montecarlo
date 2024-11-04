import numpy as np
import pandas as pd
import altair as alt


def binned_dataframe(left, mode, right, size):

    trng = np.random.default_rng().triangular(left, mode, right, size)
    df = pd.DataFrame(trng, columns=['values'])
    return df


def histogram(df, step):
    
    chart = alt.Chart(df).transform_density(
        'values',
        as_=['values', 'density']
    ).mark_area().encode(
    x=alt.X('values:Q', bin=alt.Bin(maxbins=step), title='Values'),
    y=alt.Y('density:Q', title='Density')
    ).properties(
        width=600,
        height=400,
        title='Triangular Distribution Histogram'
    )

    return chart


def main():
    left = -1
    mode = 1
    right = 2
    size = 100000
    step = 500
    df = binned_dataframe(left, mode, right, size)
    print(df)

    chart = histogram(df, step)
    chart.save('example.html')

main()
