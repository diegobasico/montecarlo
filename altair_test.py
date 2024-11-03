import pandas as pd

import altair as alt


data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
chart = alt.Chart(data).mark_bar().encode(
    x='a',
    y='average(b)',
)
chart
