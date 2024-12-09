import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from sklearn.preprocessing import KBinsDiscretizer
import datetime
import random

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
            explore_chance : float = 0.3,

            # state and action rules
            rebalance_limit_steps : int = 2,
            asset_balance_steps : list = [x/10.0 for x in range(11)],
            random_seed : int = 42):

        # learning and exploration
        self.learning_rate = learning_rate
        self.explore_chance = explore_chance

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
        self.current_step = 0

        self.portfolio_value = [np.NaN for x in range(len(data))]
        self.portfolio_value[0] = 1000000

        random.seed = random_seed

        # Build the policy-learning matrix
        # dict[(int,int) -> dict[int -> float]]
        # Outer dictionary maps state(current portfolio state, 
        # market forecast) to action (a rebalanced portfolio state)
        # Inner dictionary maps action to weight
        self.state_action_weight_matrix = {}

        unique_pred_bins = data[price_delta_pred_bins_col].nunique()

        for current_asset_balance_ind in range(len(asset_balance_steps)):
            for fc_delta_bin in range(unique_pred_bins):
                
                state = (current_asset_balance_ind,fc_delta_bin)

                action_dict = {}
                # Start a new set of action_weight mappings for this
                # combination of current portfolio state and market conditions
                for action in self.get_legal_actions_provisional(current_asset_balance_ind):
                    action_dict[action] = 0
                self.state_action_weight_matrix[state] = action_dict

    

    def get_current_state_for_decision(self)->tuple[int,int]:
        return (self.asset_balance_at_open_ind[self.current_step], #Current asset balance
                self.data[self.price_delta_pred_bins_col].iat[self.current_step+1])  #Predicted next price delta

    def get_legal_actions_provisional(self, asset_bal)->int:
        return [x for x in range(len(self.asset_balance_steps)) 
                if abs(x - asset_bal) <= self.rebalance_limit_steps]
    
    def get_legal_actions(self)->int:
        return [x for x in range(len(self.asset_balance_steps)) 
                    if abs(x - self.asset_balance_at_open_ind[self.current_step]) 
                    <= self.rebalance_limit_steps]

    def get_best_action(self)->int:

        action_weight_matrix = self.state_action_weight_matrix[self.get_current_state_for_decision()]
        highest_weights = None
        best_actions = []

        # Get highest weight and best actions
        for action,weight in action_weight_matrix.items():
            if highest_weights is None:
                best_actions.append(action)
                highest_weight = weight
            elif weight == highest_weight:
                best_actions.append(action)
            elif weight > highest_weight:
                best_actions = [action]
                highest_weight = weight
            else:
                pass

        # Randomly select from the best actions
        return random.choice(best_actions)


    def get_prev_states_lookback(self,num_steps : int)-> list[tuple[int,int]]:
        prev_states = []
        for i in range (max(self.current_step-num_steps,0), self.current_step):
            prev_states.append((self.asset_balance_at_open_ind[i], 
                self.data[self.price_delta_pred_bins_col].iat[i]))        
        return prev_states

    def get_prev_actions_lookback(self, num_steps : int)-> list[int]:
        prev_actions = []
        for i in range (max(self.current_step-num_steps,0), self.current_step):
            prev_actions.append(self.asset_balance_at_open_ind[i+1])
        return prev_actions

    def update_weights_indiscriminate_lookback(self, num_steps : int):
        prev_states = self.get_prev_states_lookback(num_steps)
        prev_actions = self.get_prev_actions_lookback(num_steps)

        # print(prev_states)
        # print(prev_actions)

        # Reward based on daily change in value of portfolio
        reward = (self.data[self.price_delta_col].iat[self.current_step]
                  * self.asset_balance_steps[self.asset_balance_at_open_ind[self.current_step]])
        
        weight_update = reward * self.learning_rate
        
        # print(str(weight_update))

        for i in range(len(prev_states)):
            new_val = self.state_action_weight_matrix[prev_states[i]][prev_actions[i]] + weight_update
            self.state_action_weight_matrix[prev_states[i]][prev_actions[i]] = new_val

    def step(self, 
            exploring : bool,
            learning : bool,
            learning_lookback_steps: int = 5):

        # STOP If we're out of data for simulation
        if self.current_step + 1 >= len(self.data):
            # probably need to throw an error or something
            return False

        # Make decision
        if exploring and random.random() < self.explore_chance:
            self.asset_balance_at_open_ind[self.current_step+1] = random.choice(self.get_legal_actions()) # Choose randomly among legal actions
        else: 
            self.asset_balance_at_open_ind[self.current_step+1] = self.get_best_action()  # Get highest-weighted choice
        
        # Iterate to next step and learn from decision
        self.current_step = self.current_step + 1

        # Update portfolio value
        commodity_value = (self.portfolio_value[self.current_step-1]
                                 * self.asset_balance_steps[self.asset_balance_at_open_ind[self.current_step]] 
                                 * self.data[self.price_delta_col].iat[self.current_step])

        cash_value = (self.portfolio_value[self.current_step-1]
                                 * 1 - self.asset_balance_steps[self.asset_balance_at_open_ind[self.current_step]]) 

        self.portfolio_value[self.current_step] = commodity_value + cash_value

        # Learn from previous actions
        if learning:
            self.update_weights_indiscriminate_lookback(num_steps=learning_lookback_steps)

        return True

    def print_model(self):
        for state,action_weight_matrix in self.state_action_weight_matrix.items():
            print('State (Current Portfolio Balance, Prediction Bin):  ' + str(state) + ' -> ')
            for action,weight in action_weight_matrix.items():
                print('     Action (New Portfolio Weight)->Weight:  ' + str(action) + ' -> ' + str(weight))

