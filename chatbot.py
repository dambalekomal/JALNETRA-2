"""
NLP-Based Chatbot Module for JALNETRA
Provides intelligent natural language query processing for groundwater data
"""

import pandas as pd
import re
from difflib import get_close_matches
import streamlit as st

class GroundwaterChatbot:
    """NLP-based chatbot for groundwater data queries"""
    
    def __init__(self, df):
        self.df = df
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Build knowledge base from dataset"""
        kb = {
            'states': list(self.df['State'].unique()),
            'districts': list(self.df['District'].unique()),
            'talukas': list(self.df['Taluka'].unique()),
            'years': sorted(list(self.df['Year'].unique())),
            'categories': list(self.df['Category'].unique()),
            'metrics': ['pre-monsoon level', 'post-monsoon level', 'recharge', 'extraction', 'stage of extraction']
        }
        return kb
    
    def extract_entities(self, query):
        """Extract entities from user query"""
        query_lower = query.lower()
        entities = {
            'state': None,
            'district': None,
            'taluka': None,
            'year': None,
            'category': None,
            'metric': None
        }
        
        # Extract state
        for state in self.knowledge_base['states']:
            if state.lower() in query_lower:
                entities['state'] = state
                break
        
        # Extract district
        for district in self.knowledge_base['districts']:
            if district.lower() in query_lower:
                entities['district'] = district
                break
        
        # Extract taluka
        for taluka in self.knowledge_base['talukas']:
            if taluka.lower() in query_lower:
                entities['taluka'] = taluka
                break
        
        # Extract year
        years_in_query = re.findall(r'\b(20\d{2}|19\d{2})\b', query)
        if years_in_query:
            entities['year'] = int(years_in_query[0])
        
        # Extract category
        for category in self.knowledge_base['categories']:
            if category.lower() in query_lower:
                entities['category'] = category
                break
        
        # Extract metric
        for metric in self.knowledge_base['metrics']:
            if metric in query_lower:
                entities['metric'] = metric
                break
        
        return entities
    
    def is_groundwater_related(self, query):
        """Check if query is related to groundwater"""
        groundwater_keywords = [
            'groundwater', 'water level', 'recharge', 'extraction', 'monsoon',
            'taluka', 'district', 'state', 'well', 'aquifer', 'borewell',
            'groundwater status', 'water table', 'extraction stage', 'category',
            'pre-monsoon', 'post-monsoon', 'safe', 'critical', 'exploited'
        ]
        
        query_lower = query.lower()
        
        # Check if query contains groundwater entities
        for entity_list in [self.knowledge_base['states'], 
                           self.knowledge_base['districts'], 
                           self.knowledge_base['talukas']]:
            for entity in entity_list:
                if entity.lower() in query_lower:
                    return True
        
        # Check keywords
        for keyword in groundwater_keywords:
            if keyword in query_lower:
                return True
        
        return False
    
    def get_district_extraction(self, district):
        """Get extraction data for a district"""
        district_data = self.df[self.df['District'] == district]
        if len(district_data) == 0:
            return None
        
        avg_extraction = district_data['Extraction'].mean()
        latest_year = district_data['Year'].max()
        
        return {
            'district': district,
            'avg_extraction': avg_extraction,
            'latest_year': latest_year
        }
    
    def get_taluka_recharge(self, taluka):
        """Get recharge data for a taluka"""
        taluka_data = self.df[self.df['Taluka'] == taluka]
        if len(taluka_data) == 0:
            return None
        
        avg_recharge = taluka_data['Recharge'].mean()
        latest_year = taluka_data['Year'].max()
        
        return {
            'taluka': taluka,
            'avg_recharge': avg_recharge,
            'latest_year': latest_year
        }
    
    def compare_monsoon_levels(self, location_type, location_name):
        """Compare pre and post monsoon levels"""
        if location_type == 'district':
            data = self.df[self.df['District'] == location_name]
        elif location_type == 'taluka':
            data = self.df[self.df['Taluka'] == location_name]
        else:
            return None
        
        if len(data) == 0:
            return None
        
        avg_pre = data['Pre-Monsoon Level'].mean()
        avg_post = data['Post-Monsoon Level'].mean()
        difference = avg_post - avg_pre
        
        return {
            'pre_monsoon': avg_pre,
            'post_monsoon': avg_post,
            'difference': difference
        }
    
    def get_highest_metric(self, metric_type):
        """Find district or taluka with highest metric"""
        if metric_type.lower() in ['extraction', 'extract']:
            grouped = self.df.groupby('District')['Extraction'].mean()
            highest_district = grouped.idxmax()
            highest_value = grouped.max()
            return f"highest extraction in {highest_district} with average {highest_value:.2f}"
        
        elif metric_type.lower() in ['recharge', 'recharge rate']:
            grouped = self.df.groupby('Taluka')['Recharge'].mean()
            highest_taluka = grouped.idxmax()
            highest_value = grouped.max()
            return f"highest recharge in {highest_taluka} with average {highest_value:.2f}"
        
        elif metric_type.lower() in ['water level', 'groundwater level']:
            grouped = self.df.groupby('District')[['Pre-Monsoon Level', 'Post-Monsoon Level']].mean().mean(axis=1)
            highest_district = grouped.idxmax()
            highest_value = grouped.max()
            return f"highest groundwater level in {highest_district} with average {highest_value:.2f} meters"
    
    def get_year_status(self, year):
        """Get groundwater status for a specific year"""
        year_data = self.df[self.df['Year'] == year]
        if len(year_data) == 0:
            return None
        
        status = {
            'year': year,
            'total_records': len(year_data),
            'avg_pre_monsoon': year_data['Pre-Monsoon Level'].mean(),
            'avg_post_monsoon': year_data['Post-Monsoon Level'].mean(),
            'categories': year_data['Category'].value_counts().to_dict()
        }
        
        return status
    
    def process_query(self, query):
        """Process user query and generate response"""
        
        # Check if query is groundwater related
        if not self.is_groundwater_related(query):
            return "❌ This question is not related to the groundwater assessment dataset. Please ask questions about groundwater levels, extraction, recharge, districts, talukas, or water categories."
        
        query_lower = query.lower()
        
        # Query type 1: Extraction in a location
        if any(word in query_lower for word in ['extraction', 'extract', 'extracted']) and \
           any(word in query_lower for word in ['gangapur', 'pune', 'nashik'] + self.knowledge_base['talukas']):
            for taluka in self.knowledge_base['talukas']:
                if taluka.lower() in query_lower:
                    taluka_data = self.df[self.df['Taluka'] == taluka]
                    if len(taluka_data) > 0:
                        avg_extraction = taluka_data['Extraction'].mean()
                        return f"📊 In {taluka}, the average groundwater extraction is {avg_extraction:.2f} units."
            
            for district in self.knowledge_base['districts']:
                if district.lower() in query_lower:
                    district_data = self.df[self.df['District'] == district]
                    if len(district_data) > 0:
                        avg_extraction = district_data['Extraction'].mean()
                        return f"📊 In {district}, the average groundwater extraction is {avg_extraction:.2f} units."
        
        # Query type 2: Highest recharge
        if 'highest recharge' in query_lower or 'maximum recharge' in query_lower:
            grouped = self.df.groupby('Taluka')['Recharge'].mean()
            highest_taluka = grouped.idxmax()
            highest_value = grouped.max()
            return f"💧 {highest_taluka} has the {self.get_highest_metric('recharge')}."
        
        # Query type 3: Compare monsoon levels
        if 'compare' in query_lower and ('monsoon' in query_lower or 'level' in query_lower):
            for district in self.knowledge_base['districts']:
                if district.lower() in query_lower:
                    comparison = self.compare_monsoon_levels('district', district)
                    if comparison:
                        return f"📈 In {district}:\n- Pre-Monsoon Level: {comparison['pre_monsoon']:.2f}m\n- Post-Monsoon Level: {comparison['post_monsoon']:.2f}m\n- Difference: {comparison['difference']:.2f}m"
            
            for taluka in self.knowledge_base['talukas']:
                if taluka.lower() in query_lower:
                    comparison = self.compare_monsoon_levels('taluka', taluka)
                    if comparison:
                        return f"📈 In {taluka}:\n- Pre-Monsoon Level: {comparison['pre_monsoon']:.2f}m\n- Post-Monsoon Level: {comparison['post_monsoon']:.2f}m\n- Difference: {comparison['difference']:.2f}m"
        
        # Query type 4: Year-specific status
        for year in self.knowledge_base['years']:
            if str(year) in query_lower:
                year_status = self.get_year_status(year)
                if year_status:
                    response = f"📅 Groundwater Status in {year}:\n"
                    response += f"- Total Records: {year_status['total_records']}\n"
                    response += f"- Avg Pre-Monsoon Level: {year_status['avg_pre_monsoon']:.2f}m\n"
                    response += f"- Avg Post-Monsoon Level: {year_status['avg_post_monsoon']:.2f}m\n"
                    response += f"- Categories: {', '.join([f'{k}: {v}' for k, v in year_status['categories'].items()])}"
                    return response
        
        # Query type 5: Highest extraction
        if 'highest extraction' in query_lower or 'maximum extraction' in query_lower:
            grouped = self.df.groupby('District')['Extraction'].mean()
            highest_district = grouped.idxmax()
            highest_value = grouped.max()
            return f"⚠️ {highest_district} has the highest extraction with average {highest_value:.2f} units."
        
        # Query type 6: District info
        for district in self.knowledge_base['districts']:
            if district.lower() in query_lower and any(word in query_lower for word in ['district', 'information', 'info', 'tell me', 'about']):
                district_data = self.df[self.df['District'] == district]
                if len(district_data) > 0:
                    response = f"📍 {district} District:\n"
                    response += f"- Records: {len(district_data)}\n"
                    response += f"- Avg Pre-Monsoon Level: {district_data['Pre-Monsoon Level'].mean():.2f}m\n"
                    response += f"- Avg Extraction: {district_data['Extraction'].mean():.2f}\n"
                    response += f"- Avg Recharge: {district_data['Recharge'].mean():.2f}"
                    return response
        
        # Default response
        return "🤖 I can help you with groundwater data queries! Try asking about:\n" \
               "- Extraction in specific locations\n" \
               "- Highest recharge areas\n" \
               "- Monsoon level comparisons\n" \
               "- Data for specific years\n" \
               "- District or Taluka information"


class MultilingualChatbot(GroundwaterChatbot):
    """Extended chatbot with multilingual support"""
    
    def __init__(self, df):
        super().__init__(df)
        self.translations = self._build_translations()
    
    def _build_translations(self):
        """Build translation dictionary"""
        return {
            'extraction': {
                'en': 'extraction',
                'hi': 'खनन',
                'mr': 'खनन'
            },
            'recharge': {
                'en': 'recharge',
                'hi': 'पुनः भरण',
                'mr': 'पुनः भरण'
            },
            'water level': {
                'en': 'water level',
                'hi': 'जल स्तर',
                'mr': 'जल स्तर'
            },
            'monsoon': {
                'en': 'monsoon',
                'hi': 'मानसून',
                'mr': 'मॉनसून'
            }
        }
    
    def process_multilingual_query(self, query, language='en'):
        """Process query in specified language"""
        # For now, convert to English and process
        response = self.process_query(query)
        return response
