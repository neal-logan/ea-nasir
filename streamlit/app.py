import streamlit as st
import numpy as np
import time

def main():
    if 'time_step' not in st.session_state:
        st.session_state.time_step = 0
        st.session_state.running = False
        st.session_state.max_steps = 100

    st.title('Ea Nasir: Honest Copper Trader')
        
    st.subheader('Time Controls')
    # Time progress bar
    progress = st.progress(st.session_state.time_step / st.session_state.max_steps)
    
    # Create a row of buttons using columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button('Reset'):
            st.session_state.time_step = 0
            st.session_state.running = False
    
    with col2:
        if st.button('Step'):
            st.session_state.running = False    
            if st.session_state.time_step < st.session_state.max_steps:
                st.session_state.time_step += 1
    
    with col3:
        if st.session_state.running:
            if st.button('Play'):
                st.session_state.running = not st.session_state.running
        else:
            if st.button('Pause'):
                st.session_state.running = not st.session_state.running
    
    with col4:
        speed = st.select_slider('Speed', options=[0.1, 0.25, 0.5, 1.0, 2.0], value=1.0)
    
    # Display current time step
    st.write(f'Time Step: {st.session_state.time_step}')
    
    st.subheader('Net Assets')

    # Simulated data (replace with your actual time series data)
    data = np.sin(np.linspace(0, st.session_state.time_step/10, st.session_state.time_step + 1))
    st.line_chart(data)
    
    # Automatic advancement
    if st.session_state.running:
        if st.session_state.time_step < st.session_state.max_steps:
            time.sleep(1 / speed)
            st.session_state.time_step += 1
            st.experimental_rerun()

if __name__ == '__main__':
    main()