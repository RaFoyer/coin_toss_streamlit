# app.py

"""
This module simulates tossing a coin with Streamlit.
It allows the user to specify the number of trials for the coin toss experiment,
displays the mean results dynamically, and tracks the experiments conducted during the session.
"""

import time
import pandas as pd
import scipy.stats
import streamlit as st

# Initialize stateful variables if they are not already present in the session state
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

chart = st.line_chart([0.5])

def toss_coin(n):
    """
    Simulates tossing a coin n times and calculates the mean outcome of getting heads.

    Args:
        n (int): The number of trials to run.

    Returns:
        float: The mean outcome of getting heads in the trials.
    """
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean_outcome = None
    outcome_no = 0
    outcome_1_count = 0

    for outcome in trial_outcomes:
        outcome_no += 1
        if outcome == 1:
            outcome_1_count += 1
        mean_outcome = outcome_1_count / outcome_no
        chart.add_rows([mean_outcome])
        time.sleep(0.05)

    return mean_outcome

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    experiment_mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            experiment_mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
