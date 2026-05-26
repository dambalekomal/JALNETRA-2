"""
Machine Learning Prediction Module for JALNETRA
Uses Random Forest for groundwater level and trend predictions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

class GroundwaterPredictor:
    """Machine Learning predictor for groundwater metrics"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.models = {}
        self.encoders = {}
        self.feature_columns = ['State_encoded', 'District_encoded', 'Taluka_encoded', 'Year']
        self._prepare_data()
        self._train_models()
    
    def _prepare_data(self):
        """Prepare data for ML models"""
        # Encode categorical variables
        for col in ['State', 'District', 'Taluka']:
            le = LabelEncoder()
            self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
            self.encoders[col] = le
    
    def _train_models(self):
        """Train Random Forest models for different metrics"""
        metrics = {
            'Pre-Monsoon Level': 'pre_monsoon',
            'Post-Monsoon Level': 'post_monsoon',
            'Recharge': 'recharge',
            'Extraction': 'extraction'
        }
        
        for metric, model_name in metrics.items():
            try:
                X = self.df[self.feature_columns]
                y = self.df[metric]
                
                # Remove any NaN values
                mask = ~(X.isna().any(axis=1) | y.isna())
                X = X[mask]
                y = y[mask]
                
                if len(X) > 0:
                    model = RandomForestRegressor(
                        n_estimators=100,
                        max_depth=10,
                        random_state=42,
                        n_jobs=-1
                    )
                    model.fit(X, y)
                    self.models[model_name] = model
            except Exception as e:
                st.error(f"Error training model for {metric}: {str(e)}")
    
    def predict_groundwater_level(self, state, district, taluka, year):
        """Predict groundwater level for given parameters"""
        try:
            # Encode categorical variables
            state_encoded = self.encoders['State'].transform([state])[0]
            district_encoded = self.encoders['District'].transform([district])[0]
            taluka_encoded = self.encoders['Taluka'].transform([taluka])[0]
            
            # Create feature array
            features = np.array([[state_encoded, district_encoded, taluka_encoded, year]])
            
            predictions = {}
            
            if 'pre_monsoon' in self.models:
                predictions['pre_monsoon'] = self.models['pre_monsoon'].predict(features)[0]
            
            if 'post_monsoon' in self.models:
                predictions['post_monsoon'] = self.models['post_monsoon'].predict(features)[0]
            
            if 'recharge' in self.models:
                predictions['recharge'] = self.models['recharge'].predict(features)[0]
            
            if 'extraction' in self.models:
                predictions['extraction'] = self.models['extraction'].predict(features)[0]
            
            return predictions
        
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")
            return None
    
    def predict_trend(self, state, district, taluka, years_ahead=5):
        """Predict trend for multiple years ahead"""
        try:
            current_year = int(self.df['Year'].max())
            future_years = list(range(current_year + 1, current_year + years_ahead + 1))
            
            trends = {
                'years': future_years,
                'pre_monsoon': [],
                'post_monsoon': [],
                'recharge': [],
                'extraction': []
            }
            
            for year in future_years:
                pred = self.predict_groundwater_level(state, district, taluka, year)
                if pred:
                    trends['pre_monsoon'].append(pred.get('pre_monsoon', 0))
                    trends['post_monsoon'].append(pred.get('post_monsoon', 0))
                    trends['recharge'].append(pred.get('recharge', 0))
                    trends['extraction'].append(pred.get('extraction', 0))
            
            return trends
        
        except Exception as e:
            st.error(f"Error predicting trend: {str(e)}")
            return None
    
    def get_extraction_stage_category(self, extraction, recharge):
        """Determine groundwater category based on extraction stage"""
        if recharge == 0:
            return 'Critical'
        
        extraction_stage = (extraction / recharge) * 100
        
        if extraction_stage <= 70:
            return 'Safe'
        elif extraction_stage <= 90:
            return 'Semi-Critical'
        elif extraction_stage <= 100:
            return 'Critical'
        else:
            return 'Over-Exploited'
    
    def get_model_features_importance(self, metric_name='pre_monsoon'):
        """Get feature importance from trained model"""
        if metric_name not in self.models:
            return None
        
        model = self.models[metric_name]
        importances = model.feature_importances_
        
        features_importance = {
            'State': importances[0],
            'District': importances[1],
            'Taluka': importances[2],
            'Year': importances[3]
        }
        
        return features_importance
    
    def predict_future_scenario(self, state, district, taluka):
        """Create a comprehensive future prediction scenario"""
        try:
            current_year = int(self.df['Year'].max())
            
            # Get historical data
            historical = self.df[
                (self.df['State'] == state) &
                (self.df['District'] == district) &
                (self.df['Taluka'] == taluka)
            ].sort_values('Year')
            
            # Get predictions
            trend = self.predict_trend(state, district, taluka, years_ahead=5)
            
            scenario = {
                'historical_years': historical['Year'].tolist() if len(historical) > 0 else [],
                'historical_pre_monsoon': historical['Pre-Monsoon Level'].tolist() if len(historical) > 0 else [],
                'historical_post_monsoon': historical['Post-Monsoon Level'].tolist() if len(historical) > 0 else [],
                'forecast': trend
            }
            
            return scenario
        
        except Exception as e:
            st.error(f"Error creating scenario: {str(e)}")
            return None


def create_prediction_chart(scenario, title="Groundwater Level Prediction"):
    """Create interactive prediction chart using Plotly"""
    
    if not scenario or not scenario.get('forecast'):
        return None
    
    fig = go.Figure()
    
    # Add historical data
    if scenario['historical_years']:
        fig.add_trace(go.Scatter(
            x=scenario['historical_years'],
            y=scenario['historical_pre_monsoon'],
            mode='lines+markers',
            name='Historical Pre-Monsoon',
            line=dict(color='#FF6B6B', width=2),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=scenario['historical_years'],
            y=scenario['historical_post_monsoon'],
            mode='lines+markers',
            name='Historical Post-Monsoon',
            line=dict(color='#4ECDC4', width=2),
            marker=dict(size=6)
        ))
    
    # Add forecast
    forecast_years = scenario['forecast']['years']
    
    fig.add_trace(go.Scatter(
        x=forecast_years,
        y=scenario['forecast']['pre_monsoon'],
        mode='lines+markers',
        name='Predicted Pre-Monsoon',
        line=dict(color='#FF6B6B', width=2, dash='dash'),
        marker=dict(size=6, symbol='diamond')
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_years,
        y=scenario['forecast']['post_monsoon'],
        mode='lines+markers',
        name='Predicted Post-Monsoon',
        line=dict(color='#4ECDC4', width=2, dash='dash'),
        marker=dict(size=6, symbol='diamond')
    ))
    
    # Add a vertical line to separate historical and forecast
    if scenario['historical_years']:
        last_historical = scenario['historical_years'][-1]
        fig.add_vline(
            x=last_historical + 0.5,
            line_dash="dash",
            line_color="gray",
            annotation_text="Forecast Start",
            annotation_position="top right"
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Water Level (meters)",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400,
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='gray',
            borderwidth=1
        )
    )
    
    return fig
