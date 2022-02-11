import pandas as pd
import numpy as np
import PIL.Image
from pathlib import Path
import streamlit as st
st.set_page_config(page_title="Demo Display App", layout = "wide", initial_sidebar_state = "collapsed")

st.markdown("# Style Gen Demo Application")
columns = st.columns([1, 1, 1])
fs = list(Path("./dress/").glob("**/*"))

for f, c in zip(fs, columns):
    c.image(PIL.Image.open(f).resize((500, 500)))