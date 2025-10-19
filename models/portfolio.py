class Portfolio:
    """Modèle représentant un portefeuille d'actions"""
    
    def __init__(self, actions=None):
        self.actions = actions or []
        self.total_cost = sum(action.cost for action in self.actions)
        self.total_profit = sum(action.profit for action in self.actions)
    
    def add_action(self, action):
        self.actions.append(action)
        self.total_cost += action.cost
        self.total_profit += action.profit
    
    def __repr__(self):
        return f"Portfolio(cost={self.total_cost}, profit={self.total_profit:.0f}, actions={len(self.actions)})"