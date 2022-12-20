from datetime import datetime, timedelta
from meteostat import Daily
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.write(
    """# Streamlit Example with Palermo Meteorological Data  
_*by Alessandro Romancino for Computational Physics Course*_

[Code on Github](https://github.com/alex180500/computational-seminar)"""
)

with st.sidebar:
    if st.button("Merry Christmas"):
        st.snow()

tab1, tab2 = st.tabs(["Palermo Weather", "Actually Useful Stuff"])

with tab1:
    today = datetime.now()
    yesterday = today - timedelta(days=4)

    data = Daily("16405", yesterday, today)
    data = data.fetch().tail(2)
    value = data.iloc[1]
    delta = data.iloc[1] - data.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{value['tavg']:.1f} °C", f"{delta['tavg']:.1f} °C")
    col2.metric("Wind", f"{value['wspd']:.1f} km/h", f"{delta['wspd']:.1f} km/h")
    col3.metric("Pressure", f"{value['pres']:.1f} hPa", f"{delta['pres']:.1f} hPa")

with tab2:
    ord = st.number_input(
        "Select maximum order", min_value=0, max_value=4, step=1, format="%d"
    )
    options = ["Display only the selected order", "Display all derivatives"]
    all_bool = st.radio("Display options", options, label_visibility="collapsed")
    mpl_bool = st.checkbox("Use matplotlib :bar_chart:", value=True)

    x, dx = np.linspace(-np.pi, np.pi, 1000, retstep=True)
    func = np.sin(x)

    derivatives = np.zeros((ord + 1, x.size))
    for i in range(ord + 1):
        derivatives[i] = func
        func = np.gradient(func, dx)

    if mpl_bool:
        fig, ax = plt.subplots()
        ax.set_xlim(-np.pi, np.pi)
        ax.set_ylim(-1, 1)

        if all_bool == options[0]:
            ax.plot(x, derivatives[-1])
        else:
            for y in derivatives:
                ax.plot(x, y)

        st.pyplot(fig)
    else:
        df = pd.DataFrame(derivatives.T, columns=range(ord + 1), index=x)

        if all_bool == options[0]:
            st.line_chart(df.T.iloc[-1])
        else:
            st.line_chart(df)
