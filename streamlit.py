import streamlit as st
import numpy as np
import time
import methods.sim as sim
import pandas as pd



def main():
    
    if 'agent' not in st.session_state:
        st.session_state.agent = sim.PortfolioAgent(
            data = dev_df[columns],
            date_col= 'DATE',
            price_delta_pred_bins_col = 'COPPER_OPEN_NOMINAL_PROPDELTA_PRED_BIN',
            price_delta_col = 'COPPER_OPEN_NOMINAL_PROPDELTA_PRED',
            learning_rate = 1, 
            explore_chance = 0.3, #Chance to take a random (legal) action
            rebalance_limit_steps = 2,  # Determine how far asset balances can be changed with each action
            asset_balance_steps = [x/10.0 for x in range(11)],)  # Possible asset balances; 0 is all cash, 1 is all copper futures

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