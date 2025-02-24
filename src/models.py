import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple

class ImpactPredictor:
    def __init__(self):
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def generate_synthetic_data(self, n_samples=1000) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate synthetic data for model training"""
        np.random.seed(42)
        X = pd.DataFrame({
            'size': np.random.uniform(10, 1000, n_samples),
            'condition': np.random.uniform(1, 10, n_samples),
            'transport_score': np.random.uniform(1, 10, n_samples),
            'location_score': np.random.uniform(1, 10, n_samples),
            'community_score': np.random.uniform(1, 10, n_samples),
            'energy_score': np.random.uniform(1, 10, n_samples),
            'accessibility_index': np.random.uniform(0, 100, n_samples),
            'renovation_potential': np.random.uniform(0, 100, n_samples),
            'community_impact': np.random.uniform(0, 100, n_samples),
            'sustainability_score': np.random.uniform(0, 100, n_samples)
        })
        
        # Generate synthetic target variables
        y = pd.DataFrame({
            'social_impact': 0.3 * X['community_score'] + 0.3 * X['transport_score'] + 0.4 * X['location_score'],
            'environmental_impact': 0.4 * X['energy_score'] + 0.3 * X['condition'] + 0.3 * X['transport_score'],
            'financial_impact': 0.4 * X['location_score'] + 0.3 * X['condition'] + 0.3 * X['size'] / 100
        })
        
        return X, y
    
    def fit(self) -> None:
        """Train the models on synthetic data"""
        X, y = self.generate_synthetic_data()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.rf_model.fit(X_scaled, y)
        
        # Train XGBoost
        self.xgb_model.fit(X_scaled, y)
        
        self.is_fitted = True
        
    def predict_impact(self, features: pd.DataFrame) -> Dict:
        """Make predictions with trained models"""
        if not self.is_fitted:
            self.fit()
            
        features_scaled = self.scaler.transform(features)
        
        # Get predictions from both models
        rf_pred = self.rf_model.predict(features_scaled)
        xgb_pred = self.xgb_model.predict(features_scaled)
        
        # Ensemble predictions
        predictions = np.stack([rf_pred, xgb_pred])
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return {
            'prediction': mean_pred,
            'uncertainty': std_pred,
            'individual_predictions': predictions
        }