"""
Data Processing Module for JALNETRA
Handles data loading, filtering, and analysis
"""

import pandas as pd
import numpy as np
import streamlit as st

class DataProcessor:
    """Handle all data processing operations"""
    
    def __init__(self, csv_path='groundwater_data.csv'):
        self.df = self._load_data(csv_path)
    
    def _load_data(self, csv_path):
        """Load data from CSV"""
        try:
            df = pd.read_csv(csv_path)
            return df
        except FileNotFoundError:
            st.error(f"❌ {csv_path} not found!")
            return None
    
    def get_data(self):
        """Return the dataframe"""
        return self.df
    
    def filter_by_state(self, state):
        """Filter data by state"""
        return self.df[self.df['State'] == state]
    
    def filter_by_district(self, district):
        """Filter data by district"""
        return self.df[self.df['District'] == district]
    
    def filter_by_taluka(self, taluka):
        """Filter data by taluka"""
        return self.df[self.df['Taluka'] == taluka]
    
    def filter_by_year(self, year):
        """Filter data by year"""
        return self.df[self.df['Year'] == year]
    
    def filter_by_category(self, category):
        """Filter data by category"""
        return self.df[self.df['Category'] == category]
    
    def multi_filter(self, states=None, districts=None, talukas=None, 
                    years=None, categories=None):
        """Apply multiple filters"""
        filtered_df = self.df.copy()
        
        if states:
            filtered_df = filtered_df[filtered_df['State'].isin(states)]
        
        if districts:
            filtered_df = filtered_df[filtered_df['District'].isin(districts)]
        
        if talukas:
            filtered_df = filtered_df[filtered_df['Taluka'].isin(talukas)]
        
        if years:
            filtered_df = filtered_df[filtered_df['Year'].isin(years)]
        
        if categories:
            filtered_df = filtered_df[filtered_df['Category'].isin(categories)]
        
        return filtered_df
    
    def search_data(self, search_term):
        """Search data across all columns"""
        mask = self.df.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False)
        ).any(axis=1)
        return self.df[mask]
    
    def get_unique_values(self, column):
        """Get unique values of a column"""
        return sorted(list(self.df[column].unique()))
    
    def get_statistics(self, df=None):
        """Get statistical summary"""
        data = df if df is not None else self.df
        
        stats = {
            'total_records': len(data),
            'states': data['State'].nunique(),
            'districts': data['District'].nunique(),
            'talukas': data['Taluka'].nunique(),
            'years': data['Year'].nunique(),
            'avg_pre_monsoon': data['Pre-Monsoon Level'].mean(),
            'avg_post_monsoon': data['Post-Monsoon Level'].mean(),
            'avg_recharge': data['Recharge'].mean(),
            'avg_extraction': data['Extraction'].mean(),
            'max_pre_monsoon': data['Pre-Monsoon Level'].max(),
            'min_pre_monsoon': data['Pre-Monsoon Level'].min(),
        }
        
        return stats
    
    def get_district_statistics(self, district):
        """Get statistics for a district"""
        district_data = self.df[self.df['District'] == district]
        
        if len(district_data) == 0:
            return None
        
        return {
            'district': district,
            'records': len(district_data),
            'talukas': district_data['Taluka'].nunique(),
            'avg_pre_monsoon': district_data['Pre-Monsoon Level'].mean(),
            'avg_post_monsoon': district_data['Post-Monsoon Level'].mean(),
            'avg_extraction': district_data['Extraction'].mean(),
            'avg_recharge': district_data['Recharge'].mean(),
            'categories': district_data['Category'].value_counts().to_dict()
        }
    
    def get_taluka_statistics(self, taluka):
        """Get statistics for a taluka"""
        taluka_data = self.df[self.df['Taluka'] == taluka]
        
        if len(taluka_data) == 0:
            return None
        
        return {
            'taluka': taluka,
            'records': len(taluka_data),
            'districts': taluka_data['District'].nunique(),
            'avg_pre_monsoon': taluka_data['Pre-Monsoon Level'].mean(),
            'avg_post_monsoon': taluka_data['Post-Monsoon Level'].mean(),
            'avg_extraction': taluka_data['Extraction'].mean(),
            'avg_recharge': taluka_data['Recharge'].mean(),
            'categories': taluka_data['Category'].value_counts().to_dict()
        }
    
    def get_category_distribution(self, df=None):
        """Get category distribution"""
        data = df if df is not None else self.df
        return data['Category'].value_counts()
    
    def get_year_trend(self, df=None):
        """Get year-wise trend"""
        data = df if df is not None else self.df
        
        trend = data.groupby('Year').agg({
            'Pre-Monsoon Level': 'mean',
            'Post-Monsoon Level': 'mean',
            'Recharge': 'mean',
            'Extraction': 'mean'
        }).reset_index()
        
        return trend
    
    def export_to_csv(self, data, filename):
        """Export data to CSV"""
        try:
            data.to_csv(filename, index=False)
            return True, f"Data exported to {filename}"
        except Exception as e:
            return False, f"Error exporting data: {str(e)}"
    
    def export_to_excel(self, data, filename):
        """Export data to Excel"""
        try:
            data.to_excel(filename, index=False)
            return True, f"Data exported to {filename}"
        except Exception as e:
            return False, f"Error exporting data: {str(e)}"
