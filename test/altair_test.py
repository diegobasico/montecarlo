import numpy as np
import pandas as pd
import altair as alt


def binned_dataframe(left, mode, right, size):

    trng = np.random.default_rng().triangular(left, mode, right, size)
    df = pd.DataFrame(trng, columns=['values'])
    return df


def distribution_plot(df, step):
    
    chart = alt.Chart(df).transform_density(
        'values',
        as_=['values', 'density']
    ).mark_area().encode(
    # x=alt.X('values:Q', bin=alt.Bin(maxbins=step), title='Values'),
    x=alt.X('values:Q', title='Values'),
    y=alt.Y('density:Q', title='Density'),
    tooltip=['values:Q', 'density:Q']
    ).properties(
        width=600,
        height=400,
        title='Triangular Distribution'
    )

    return chart


def main():
    left = 1104172.66
    mode = 1120365.85
    right = 1159748.99
    size = 100000
    step = 500
    df = binned_dataframe(left, mode, right, size)
    print(df)

    chart = distribution_plot(df, step)
    chart.save('test/example.html')

main()
