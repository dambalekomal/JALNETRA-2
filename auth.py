"""
Authentication Module for JALNETRA Dashboard
Handles OTP generation, verification, and session management
"""

import smtplib
import random
import string
import time
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

class OTPManager:
    """Manages OTP generation and verification"""
    
    def __init__(self):
        self.otp_storage = {}
        self.otp_expiry = 300  # 5 minutes
        
    def generate_otp(self, length=6):
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    def send_otp_email(self, email, otp):
        """Send OTP to user email"""
        try:
            # Email configuration
            sender_email = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
            sender_password = os.getenv("SENDER_PASSWORD", "your-app-password")
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "JALNETRA - OTP Verification"
            message["From"] = sender_email
            message["To"] = email
            
            # HTML email body
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #667eea; margin: 0;">💧 JALNETRA</h1>
                            <p style="color: #666; margin: 5px 0;">Groundwater Assessment Dashboard</p>
                        </div>
                        
                        <h2 style="color: #333; text-align: center;">Email Verification</h2>
                        
                        <p style="color: #555; font-size: 16px;">Hello,</p>
                        <p style="color: #555; font-size: 16px;">Your OTP for JALNETRA Dashboard access is:</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px;">
                                <h1 style="color: white; letter-spacing: 10px; margin: 0;">{otp}</h1>
                            </div>
                        </div>
                        
                        <p style="color: #555; font-size: 14px; text-align: center;">This OTP is valid for 5 minutes only.</p>
                        <p style="color: #555; font-size: 14px; text-align: center;">Do not share this OTP with anyone.</p>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                        
                        <p style="color: #999; font-size: 12px; text-align: center;">© 2026 JALNETRA. All rights reserved.</p>
                    </div>
                </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, message.as_string())
            
            return True, "OTP sent successfully"
        
        except Exception as e:
            return False, f"Error sending OTP: {str(e)}"
    
    def store_otp(self, email, otp):
        """Store OTP with timestamp"""
        self.otp_storage[email] = {
            'otp': otp,
            'timestamp': time.time()
        }
    
    def verify_otp(self, email, otp):
        """Verify OTP"""
        if email not in self.otp_storage:
            return False, "OTP not found. Please request a new OTP."
        
        stored_data = self.otp_storage[email]
        current_time = time.time()
        
        # Check if OTP expired
        if current_time - stored_data['timestamp'] > self.otp_expiry:
            del self.otp_storage[email]
            return False, "OTP expired. Please request a new OTP."
        
        # Verify OTP
        if stored_data['otp'] == otp:
            del self.otp_storage[email]
            return True, "OTP verified successfully"
        else:
            return False, "Invalid OTP. Please try again."


class AuthenticationHandler:
    """Handles user authentication and session management"""
    
    def __init__(self):
        self.otp_manager = OTPManager()
    
    def initialize_session(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        if 'otp_sent' not in st.session_state:
            st.session_state.otp_sent = False
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_user_email(self):
        """Get authenticated user's email"""
        return st.session_state.get('user_email', None)
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.otp_sent = False
        st.session_state.login_time = None
    
    def login_with_otp(self, email):
        """Send OTP to email"""
        otp = self.otp_manager.generate_otp()
        self.otp_manager.store_otp(email, otp)
        success, message = self.otp_manager.send_otp_email(email, otp)
        
        if success:
            st.session_state.otp_sent = True
            st.session_state.user_email = email
        
        return success, message
    
    def verify_otp(self, email, otp):
        """Verify OTP and authenticate user"""
        success, message = self.otp_manager.verify_otp(email, otp)
        
        if success:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.login_time = time.time()
        
        return success, message


def show_login_page():
    """Display login page UI"""
    
    # Custom CSS for login page
    st.markdown("""
        <style>
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .login-card {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 450px;
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .login-icon {
                font-size: 3em;
                margin-bottom: 10px;
            }
            
            .login-title {
                font-size: 2em;
                color: #667eea;
                margin: 0;
                font-weight: bold;
            }
            
            .login-subtitle {
                color: #999;
                margin: 5px 0 0 0;
                font-size: 0.9em;
            }
            
            .divider {
                border: none;
                border-top: 1px solid #eee;
                margin: 20px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Login container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
                <div class="login-container">
                    <div class="login-card">
                        <div class="login-header">
                            <div class="login-icon">💧</div>
                            <h1 class="login-title">JALNETRA</h1>
                            <p class="login-subtitle">Groundwater Management System</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Email input
            email = st.text_input(
                "📧 Email Address",
                placeholder="Enter your email",
                key="login_email"
            )
            
            if not st.session_state.get('otp_sent', False):
                # Send OTP button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Send OTP", use_container_width=True, type="primary"):
                        if email and "@" in email:
                            auth_handler = AuthenticationHandler()
                            success, message = auth_handler.login_with_otp(email)
                            
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Please enter a valid email address")
            
            else:
                # OTP verification section
                st.info(f"📧 OTP sent to {st.session_state.user_email}")
                
                otp_input = st.text_input(
                    "Enter 6-digit OTP",
                    placeholder="000000",
                    max_chars=6,
                    key="otp_input"
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Verify OTP", use_container_width=True, type="primary"):
                        if len(otp_input) == 6 and otp_input.isdigit():
                            auth_handler = AuthenticationHandler()
                            success, message = auth_handler.verify_otp(
                                st.session_state.user_email,
                                otp_input
                            )
                            
                            if success:
                                st.success(message)
                                st.balloons()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Please enter a valid 6-digit OTP")
                
                # Resend OTP option
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Resend OTP", use_container_width=True):
                        st.session_state.otp_sent = False
                        st.rerun()
            
            st.markdown("---")
            st.markdown("""
                <div style="text-align: center; color: #999; font-size: 0.85em;">
                    <p>🔐 Secure OTP-based authentication</p>
                    <p>© 2026 JALNETRA. All rights reserved.</p>
                </div>
            """, unsafe_allow_html=True)
