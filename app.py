import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import time
from streamz.dataframe import PeriodicDataFrame
from pycaret.regression import *





df_main = pd.DataFrame()
charge = 100
x = 0
ele_fact = 0
e = 0
ele_fact = 0
route = np.random.choice(['Munich East', 'Munich North', 'FTMRoute (2x)', 'FTMRoute',
       'Munich Northeast', 'Highway', 'Munich South', 'FTMRoute reverse'])
Weather = np.random.choice(['sunny', 'slightly cloudy', 'rainy', 'cloudy',
       'dark, little rainy', 'dark', 'sunrise', 'sunset'])

current_model = load_model('current_model')
voltage_model = load_model('voltate_model')
trottle_model = load_model('trottle_model')
torque_model = load_model('torque_model')
Distance_model = load_model('Distance_model')
bat_drain_model = load_model('battery_drained_model')
temp_model = load_model('temperature_model')


'''for i in range(1000):
    charge = 100
    '''

def reset():
    global charge
    charge = 100
    global df_main
    df_main = pd.DataFrame()
    global route
    route = np.random.choice(['Munich East', 'Munich North', 'FTMRoute (2x)', 'FTMRoute',
       'Munich Northeast', 'Highway', 'Munich South', 'FTMRoute reverse'])
    global Weather
    Weather = np.random.choice(['sunny', 'slightly cloudy', 'rainy', 'cloudy',
       'dark, little rainy', 'dark', 'sunrise', 'sunset'])


def get_acceleration():
    global df_main
    if df_main.iloc[-1]['Acceleration [m/s^2]'] <= 30:
        Acc = np.random.randint(2, 9)

    elif df_main.iloc[-1]['Acceleration [m/s^2]'] > 30 and df_main.iloc[-1]['Acceleration [m/s^2]'] <= 60:
        Acc = np.random.randint(-2,6)

    elif df_main.iloc[-1]['Acceleration [m/s^2]'] > 60 and df_main.iloc[-1]['Acceleration [m/s^2]'] <= 90:
        Acc = np.random.randint(-4, 2)

    else:
        Acc = np.random.randint(-6, 0)
    return Acc

def get_elevation():
    global df_main
    global ele_fact
    ele = 0
    if df_main.iloc[-1]['Time [s]'] - e > np.random.randint(50,200):
        ele_fact = np.random.randint(-30, 50)
    if ele_fact != 0:
        if ele_fact > 0:
            ele = df_main.iloc[-1]['Elevation [m]'] + 1
            ele_fac = ele_fac - 1
        else:
            ele = df_main.iloc[-1]['Elevation [m]'] - 1
            ele_fac = ele_fac + 1
    return ele




def get_data():
    global df_main
    global route
    global Weather  
    if df_main.shape[0] != 0:
        Acceleration = get_acceleration()
        Elevation = get_elevation()
        speed = df_main.iloc[-1]['Acceleration [m/s^2]'] + Acceleration
        if speed < 0:
            speed = 0
        distance_m = speed*0.27777778
        time_s = df_main.iloc[-1]['Time [s]'] + 1
        d = pd.DataFrame({'Route/Area': [route], 'Weather': [Weather],
                                              'Distance [km]': [distance_m/1000], 'Duration [min]': [time_s/60],
                                              'Speed [km/h]':[speed]})
        d['Route/Area'] = [['FTMRoute','FTMRoute (2x)','FTMRoute reverse','Highway','Munich East','Munich North','Munich Northeast','Munich South'].index(d['Route/Area'][0])]
        d['Weather'] = [['cloudy','dark','dark, little rainy', 'rainy', 'slightly cloudy', 'sunny','sunrise','sunset'].index(d['Weather'][0])]
        battery_drained = predict_model(bat_drain_model,data = d)

        m = pd.DataFrame({'Time [s]': [time_s], 'Velocity [km/h]': [speed],
                                              'Elevation [m]': [Elevation],
                                              'Battery Drained': [battery_drained], 'Distance [m]': [distance_m],
                                              'Acceleration [m/s^2]': [Acceleration]})
        
        

        battery_current = predict_model(current_model,m)
        battery_Voltage = predict_model(voltage_model,m)
        trottle = predict_model(trottle_model,m)
        torque = predict_model(torque_model,m)

        df_main = pd.concat[df_main, pd.DataFrame({'Time [s]': [time_s], 'Velocity [km/h]': [speed],'Elevation [m]':[Elevation],
                                               'Throttle [%]':[trottle],'Motor Torque [Nm]':[torque],'Battery Voltage [V]':[battery_Voltage],
                                               'Battery Current [A]':[battery_current],'Route/Area':[route],'Weather':[Weather],
                                                 'Battery Drained':[battery_drained], 'Distance [m]':[distance_m], 'Acceleration [m/s^2]':[Acceleration]})]
        
    else:
        Elevation = np.random.randint(200,500)
        global e 
        e = 0
        Acceleration = 0
        speed = 0
        distance_m = 0
        time_s = 0
        battery_current = 0
        battery_Voltage = 0
        trottle = 0
        torque = 0
        battery_drained = 0

        df_main = pd.DataFrame({'Time [s]': [time_s], 'Velocity [km/h]': [speed],'Elevation [m]':[Elevation],
                                               'Throttle [%]':[trottle],'Motor Torque [Nm]':[torque],'Battery Voltage [V]':[battery_Voltage],
                                               'Battery Current [A]':[battery_current],'Route/Area':[route],'Weather':[Weather], 'Battery Drained':[battery_drained], 'Distance [m]':[distance_m], 'Acceleration [m/s^2]':[Acceleration]})
        

    return 1




def start():
    global x
    x = 1
    while(x == 1):
        g = get_data()

def stop():
    global x
    x = 0




st.set_page_config(
    page_title="BMW - EV Real-Time Monitoring Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title('BMW - EV Real-Time Monitoring Dashboard')

df = px.data.gapminder()

st.markdown(
    """
    <style>
    .stButton>button {
        float: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("START"):
    start()
if st.button("STOP"):
    stop()


tab1, tab2 = st.tabs(["Distance Predictor", "Battery Temperature Maintanance"])

with tab1:
    st.write('Range of Vechicle with different Speed')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('Speed: 50 km/h')

    with col2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 300,
            title = {'text': "Speed"},
            gauge = {
                'axis': {'range': [None, 300]},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 100], 'color': 'cyan'},
                    {'range': [150, 250], 'color': 'royalblue'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 270
                }
            }
        ))



        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.write(df_main)



with tab2:
    st.write("This is Tab 2")
