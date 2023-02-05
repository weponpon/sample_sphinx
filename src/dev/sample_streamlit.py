import streamlit as st
import folium
from streamlit_folium import folium_static

import numpy as np
import pandas as pd
from PIL import Image
from streamlit_card import card

"""
## [Streamlit](https://docs.streamlit.io/)ではマークダウンを使用できます
###この記法の詳細は[こちら](https://docs.streamlit.io/library/api-reference/write-magic/magic)
他にも[API reference](https://docs.streamlit.io/library/api-reference)に色んな機能が載っています
```python
print("hello world!")
"""

st.title("foliumを使用したバージョン")
base_loc = [35.6769883,139.7588499]
m = folium.Map(location=base_loc, zoom_start=9)

folium_static(m)


hasClicked_0 = card(
  title="Hello World!",
  text="Some description",
  image="http://placekitten.com/200/300"
  # url="https://github.com/gamcoh/st-card"
)
