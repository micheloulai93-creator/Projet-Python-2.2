class Action:
    """Modèle représentant une action"""
    
    def __init__(self, action_id, cost, profit_pct):
        self.id = action_id
        self.cost = int(cost)
        self.profit_pct = float(profit_pct)
        self.profit = self.cost * self.profit_pct
    
    def __repr__(self):
        return f"Action({self.id}, cost={self.cost}, profit={self.profit:.0f})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cost': self.cost,
            'profit_pct': self.profit_pct,
            'profit': self.profit
        }