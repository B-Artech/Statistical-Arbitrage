import json
from datetime import datetime


class PositionManager:
    """
        Manager to handle open positions
    """
    
    def __init__(
        self,
        sym1,
        sym1_side,
        sym1_size,
        sym1_price,
        sym2,
        sym2_side,
        sym2_size,
        sym2_price,
        z_score,
        half_life,
        hedge_ratio
        ):
        
        self.sym1= sym1
        self.sym1_side = sym1_side
        self.sym1_size = sym1_size
        self.sym1_price = sym1_price
        self.sym2= sym2
        self.sym2_side = sym2_side
        self.sym2_size = sym2_size
        self.sym2_price = sym2_price
        self.z_score = z_score
        self.hlf_life = half_life
        self.hedge_ratio = hedge_ratio
        self.timestamp = datetime.now().isoformat()
        
    def to_dict(self):
        """ Convert Data to Dictionary"""
        return {
            "sym1": self.sym1,
            "sym1_side": self.sym1_side,
            "sym1_size": self.sym1_size,
            "sym1_price": self.sym1_price,
            "sym2": self.sym2,
            "sym2_side": self.sym2_side,
            "sym2_size": self.sym2_size,
            "sym2_price": self.sym2_price,
            "z_score": self.z_score,
            "half_life": self.hlf_life,
            "hedge_ratio": self.hedge_ratio,
            "timestamp": self.timestamp
        }
        
    def save_to_json(self, file='open_positions.json'):
        with open(file, 'r') as f:
            positions = json.load(f)
        positions.append(self.to_dict())
        with open(file, 'w') as f:
            json.dump(positions, f)