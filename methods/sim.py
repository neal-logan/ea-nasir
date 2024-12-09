import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from sklearn.preprocessing import KBinsDiscretizer
import datetime
import random

random_seed = 42

# def train():
#     random.seed(a=random_seed, version=2)

# def get_next_trading_date(
#         df : pd.DataFrame,
#         current_date : np.datetime64,
#         date_column : str = 'DATE',
#         trading_day_column : str = 'copper_TRADING_DAY') -> np.datetime64:
#     check_date = current_date + datetime.timedelta(days=1)
#     while df.loc[df[date_column] == check_date, trading_day_column] is not True:
#         check_date = check_date + datetime.timedelta(days=1)
#     return check_date

# class MarketEnvironment:
#     def __init__(
#               self,
#               df : pd.DataFrame,
#               date_column : str = 'DATE',
#               trading_day_column : str = 'copper_TRADING_DAY'):
        
#         self.df = df.sort_values(date_column)
#         self.date_column = date_column
#         self.trading_day_column = trading_day_column




# https://en.wikipedia.org/wiki/Reinforcement_learning
class PortfolioAgent:
    def __init__(
            self, 
            data : pd.DataFrame,
            date_col : str,
            price_delta_pred_bins_col : str, 
            price_delta_col : str,
            
            # Hyperparameters: learning and exploring
            learning_rate : float = 0.05,
            exploration_chance : float = 0.3,

            # state and action rules
            rebalance_limit_steps : int = 2,
            asset_balance_steps : list = [x/10.0 for x in range(11)],):

        # learning and exploration
        self.learning_rate = learning_rate
        self.exploration_chance = exploration_chance

        # state and action rules
        self.rebalance_limit_steps = rebalance_limit_steps
        self.asset_balance_steps = asset_balance_steps

        # Data
        self.data = data[[date_col,price_delta_pred_bins_col,price_delta_col]]
        self.date_col = date_col # For display and coordination, mainly
        self.price_delta_pred_bins_col = price_delta_pred_bins_col # For making decisions
        self.price_delta_col = price_delta_col # Used to calculate reward
        
        # States over time
        self.asset_balance_at_open_ind = [np.NaN for x in range(len(data))]
        self.asset_balance_at_open_ind[0] = 0
        self.asset_balance_decision_ind = [np.NaN for x in range(len(data))]
        self.current_step = 0

        self.portfolio_value = 1000000

        # Build the policy-learning matrix
        # dict[(int,int) -> dict[int -> float]]
        # Outer dictionary maps state(current portfolio state, 
        # market forecast) to action (a rebalanced portfolio state)
        # Inner dictionary maps action to weight
        self.state_action_weight_matrix = {}

        for current_asset_balance_ind, fc_delta_bin in enumerate(
            range(len(asset_balance_steps)),
            data[price_delta_pred_bins_col].nunique()):
            
            # Start a new set of action_weight mappings for this
            # combination of current portfolio state and market conditions
            for action in self.get_legal_actions_provisional(current_asset_balance_ind):
                self.state_action_weight_matrix[current_asset_balance_ind,fc_delta_bin] = {action : 0.0}

    

    def get_current_state(self)->tuple[int,int]:
        return (self.asset_balance_at_open_ind[self.current_step], self.data.loc[self.current_step])

    def get_legal_actions_provisional(self, asset_bal)->int:
        return [x for x in range(len(self.asset_balance_steps)) 
                if abs(x - asset_bal)<self.rebalance_limit_steps]
    
    def get_legal_actions(self)->int:
        return [x for x in range(len(self.asset_balance_steps)) 
                if abs(x - self.asset_balance_at_open_ind)<self.rebalance_limit_steps]

    def get_best_action(self)->int:
        choice = None
        highest_weight = None

        # Shuffle to avoid bias in case of ties
        shuffled_actions = random.shuffle(self.state_action_weight_matrix[self.get_current_state()].items())
        
        # Get highest weight with bias toward first in shuffled_actions dict
        for action,weight in shuffled_actions:
            if choice is None:
                choice = action
                highest_weight = weight
            elif weight > highest_weight:
                choice = action
                highest_weight = weight
            else:
                pass
        return choice


    def get_prev_states_lookback(self,num_steps : int)-> list[tuple[int,int]]:
        prev_states = []
        for i in range (max(self.current_step-num_steps,0), self.current_step):
            prev_states.append((self.asset_balance_at_open_ind[i], 
                self.data[self.price_delta_pred_bins_col].loc[i]))
        return prev_states

    def get_prev_actions_lookback(self, num_steps : int)-> list[int]:
        prev_actions = []
        for i in range (max(self.current_step-num_steps,0), self.current_step):
            prev_actions.append(self.asset_balance_decision_ind)

    def update_weights_indiscriminate_lookback(self, num_steps : int):
        prev_states = self.get_prev_states_lookback(num_steps)
        prev_actions = self.get_prev_actions_lookback(num_steps)

        # Reward based on daily change in value of portfolio
        reward = self.data[self.price_delta_col] * self.asset_balance_steps[self.asset_balance_at_open_ind]
        
        weight_update = reward * self.learning_rate
        
        for i in range(len(prev_states)):
            self.state_action_weight_matrix[prev_states[i]][prev_actions[i]] += weight_update

    def step(self, 
            exploring : bool,
            learning : bool,
            learning_lookback_steps: int = 5):

        # STOP If we're out of data for simulation
        if self.current_step >= len(self.data):
            # probably need to throw an error or something
            return

        # Update portfolio value
        wealth += wealth * self.asset_balance_steps[self.asset_balance_at_open_ind] * self.data[self.price_delta_col]

        # Decide
        if exploring and random.random < self.explore_chance:
            self.asset_balance_decision_ind = random.choice(self.get_legal_actions()) # Choose randomly among legal actions
        else: 
            self.asset_balance_decision_ind = self.get_best_action()  # Get highest-weighted choice
        

        # Learn from previous actions
        if learning:
            self.update_weights_indiscriminate_lookback(num_steps=learning_lookback_steps)

        # Iterate steps
        self.current_step = self.current_step + 1





    
    
    # one cycle of decision-making
    # includes training if necessary
    def step(self,
        action : int, 
        learning : bool,
        exploring : bool):

        # get the decision
        return None        
        

