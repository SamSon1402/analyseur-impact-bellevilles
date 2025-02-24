import pandas as pd
from typing import Dict

class FeatureEngine:
    def create_features(self, data: Dict) -> pd.DataFrame:
        """Create feature matrix from input data"""
        base_features = pd.DataFrame({
            'size': [data['size']],
            'condition': [data['condition']],
            'transport_score': [data['transport_score']],
            'location_score': [data['location_score']],
            'community_score': [data['community_score']],
            'energy_score': [data['energy_score']]
        })
        
        # Calculate derived features
        derived_features = pd.DataFrame({
            'accessibility_index': base_features['transport_score'] * base_features['location_score'] / 10,
            'renovation_potential': (10 - base_features['condition']) * base_features['size'] / 100,
            'community_impact': base_features['community_score'] * base_features['location_score'] / 10,
            'sustainability_score': base_features['energy_score'] * base_features['transport_score'] / 10
        })
        
        return pd.concat([base_features, derived_features], axis=1)