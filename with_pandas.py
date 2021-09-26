import pandas as pd
from IPython.display import display


url = "https://cristinasewell.github.io/html_and_css/assets/data.html"

tables = pd.read_html(url)

display(tables)

df = tables[0]
display(df.head())

df.columns = df.columns.get_level_values(0)

display(df.columns)