



action_set = [
    'buy_copper', 
    'sell_copper',
    'no_action'
]





class Simulation:

    def __init__(self):
        """Docstring"""
    
   

    # Convert forecasts into useable, discrete features
    # Each price prediction converts to direction+magnitude 0 means +/- 0.5% , and confidence
    simulation_features = {}

    def generate_action_options(
            agent_state : Agent_State,

    ):

        




    past_states = {} # {ISO date->{}}







    
class Agent_State:
    """
    An agent consists of:
    Assets inventory for each previous timestep
    Model weights for each previous timestep
    """
    
    def __init__(self,
        initial_money : int = 1000000,
        initial_copper_futures : int = 1000):
        """Docstring"""
        
        self.assets = {
            "USD": initial_money,
            "HG": initial_copper_futures
        }





    def net_worth(self):
        """"""
        
    
    @property
    def some_property(self):
        """
        Description of the property.
        
        Returns:
            The computed property value
        """
        return self.param1
    
    
    
    @staticmethod
    def static_method():
        """
        Description of the static method.
        
        Returns:
            What the static method returns
        """
        pass