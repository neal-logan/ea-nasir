import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from sklearn.preprocessing import KBinsDiscretizer
import datetime
import random

random_seed = 42

def train():
    random.seed(a=random_seed, version=2)


def get_next_trading_date(
        df : pd.DataFrame,
        current_date : np.datetime64,
        date_column : str = 'DATE',
        trading_day_column : str = 'copper_TRADING_DAY') -> np.datetime64:
    check_date = current_date + datetime.timedelta(days=1)
    while df.loc[df[date_column] == check_date, trading_day_column] is not True:
        check_date = check_date + datetime.timedelta(days=1)
    return check_date

class MarketEnvironment:
    def __init__(
              self,
              df : pd.DataFrame,
              date_column : str = 'DATE',
              trading_day_column : str = 'copper_TRADING_DAY'):
        
        self.df = df.sort_values(date_column)
        self.date_column = date_column
        self.trading_day_column = trading_day_column

# https://en.wikipedia.org/wiki/Reinforcement_learning
class PortfolioAgent:
    def __init__(
            self, 

            # column names for 
            traded_current_column : str, 
            traded_fc_column : str,

            # start state
            start_date : np.datetime64 = pd.to_datetime('2007-01-01', format='ISO8601'),
            asset_start_index : int = 3,
            
            # learning and exploring
            learning_rate : float = 0.1,
            exploration_chance : float = 0.3,
            reward : float = 0.0,

            # state and action rules
            rebalance_limit : float = 0.11,
            asset_balance_steps : list = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
            fc_delta_breakpoints : list = [-0.045, -0.024 -0.011,-0.003,0.003,0.011,0.024,0.045]):

        # start state
        self.current_date = start_date
        self.asset_balance_index = asset_start_index

        # learning and exploration
        self.learning_rate = learning_rate
        self.exploration_chance = exploration_chance

        # state and action rules
        self.rebalance_limit = rebalance_limit
        self.asset_balance_steps = asset_balance_steps
        self.fc_delta_breakpints = fc_delta_breakpoints # discretization of expected changes in price
        self.fc_delta_steps : list = [x for x in range(len(fc_delta_breakpoints)+1)]    

        # Build the Q-learning matrix
        # dict[(int,int) -> dict[int -> float]]
        # outer dictionary maps state(current portfolio state, 
        # market forecast) to action (a rebalanced portfolio state)
        # inner dictionary maps action to weight
        self.state_action_weight_matrix = {}
        number_asset_balance_steps = len(asset_balance_steps)
        for asset_bal_state_index, fc_delta_step in enumerate(range(number_asset_balance_steps),
                                                         self.fc_delta_steps):
            # Start a new set of action_weight mappings for this
            # combination of current portfolio state and market conditions
            action_weight = {}
            for asset_bal_action_index in range(number_asset_balance_steps):
                
                # Add the action-weight mapping only if it's within the legal
                # rebalancing limit. Initialize all weights to 0
                if abs(asset_balance_steps[asset_bal_action_index] 
                       - asset_balance_steps[asset_bal_state_index]) < rebalance_limit: 
                    action_weight[asset_bal_action_index] = 0
            
            self.state_action_weight_matrix[asset_bal_state_index,fc_delta_step] = action_weight.copy()

        
    def get_state(self, market) -> tuple[int,int]:
        
        columns = [self.traded_current_column, self.traded_fc_column]
        fc_delta = market.df[market.df['DATE'] == self.current_date, [columns]]

        fc_delta_step = 0
        for breakpoint in self.fc_delta_breakpoints:
            if breakpoint < fc_delta:
                fc_delta_step = fc_delta_step + 1

        return (self.asset_balance_index, fc_delta_step)

    # TODO add random-weighted decision option?
    def get_decision(
            self, 
            exploring : bool) -> list[np.float64]:

        state = self.get_state()

        if exploring and random.random < self.explore_chance:
            # Choose randomly among legal actions
            choice = random.choice(list(self.state_action_weight_matrix[state].items()))
        else: 
            # Get highest-weighted choice
            choice = None
            highest_weight = None

            #Shuffle to avoid bias in case of ties
            shuffled_actions = random.shuffle(self.state_action_weight_matrix[state].items())
            
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

    # applied during 
    def update_weights(
            
            price_change : str):

        (next_price - current_price)*allocation

        # Calculate reward as rate of return on overall portfolio
        return 
    
    # one cycle of decision-making
    # includes training if necessary
    def step(
        self,
        action : int, 
        
        learning : bool,
        exploring : bool):
        
        # get the decision

        # 


