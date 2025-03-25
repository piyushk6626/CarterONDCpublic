"""
Database operations for the Cart-ONDC application.

This module handles all interactions with the SQLite database including initialization,
data storage, retrieval, and management of different store types.
"""

import sqlite3
import os
from pathlib import Path

class DatabaseManager:
    """Manages SQLite database operations for the application."""
    
    def __init__(self, db_path='database.db'):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database tables if they don't exist."""
        self._create_kiriana_table()
        self._create_clothing_table()
        self._create_handicraft_table()
        self._create_restaurant_table()
        self._create_verification_table()
    
    def _create_kiriana_table(self):
        """Create the Kiriana store table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS kiriana (
            name TEXT,
            dob TEXT,
            pancard TEXT,
            gst_number TEXT,
            address TEXT,
            business_name TEXT,
            trade_license TEXT,
            udyam TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            upi_id TEXT,
            phoneNumber TEXT PRIMARY KEY)''')
        conn.commit()
        conn.close()
    
    def _create_clothing_table(self):
        """Create the Clothing store table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS clothing (
            name TEXT,
            dob TEXT,
            pancard TEXT,
            gst_number TEXT,
            address TEXT,
            business_name TEXT,
            trade_license TEXT,
            udyam TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            upi_id TEXT,
            phoneNumber TEXT PRIMARY KEY)''')
        conn.commit()
        conn.close()
    
    def _create_handicraft_table(self):
        """Create the Handicraft store table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS handicraft (
            name TEXT,
            dob TEXT,
            pancard TEXT,
            gst_number TEXT,
            address TEXT,
            business_name TEXT,
            trade_license TEXT,
            udyam TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            upi_id TEXT,
            phoneNumber TEXT PRIMARY KEY)''')
        conn.commit()
        conn.close()
    
    def _create_restaurant_table(self):
        """Create the Restaurant table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS restaurant (
            name TEXT,
            dob TEXT,
            pancard TEXT,
            gst_number TEXT,
            address TEXT,
            business_name TEXT,
            trade_license TEXT,
            udyam TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            upi_id TEXT,
            fssai_number TEXT,
            phoneNumber TEXT PRIMARY KEY)''')
        conn.commit()
        conn.close()
    
    def _create_verification_table(self):
        """Create the verification status table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS verification (
            phoneNumber TEXT PRIMARY KEY,
            verified BOOLEAN,
            store_type TEXT)''')
        conn.commit()
        conn.close()
    
    def store_kiriana_data(self, data):
        """
        Store Kiriana store registration data.
        
        Args:
            data (dict): The store data containing all required fields
            
        Returns:
            bool: True if data was stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO kiriana (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                     (data.get('name'), data.get('dob'), data.get('pancard'), data.get('gst_number'), 
                      data.get('address'), data.get('business_name'), data.get('trade_license'), 
                      data.get('udyam'), data.get('account_number'), data.get('ifsc_code'), 
                      data.get('upi_id'), data.get('phoneNumber')))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing Kiriana data: {e}")
            return False
    
    def store_clothing_data(self, data):
        """
        Store Clothing store registration data.
        
        Args:
            data (dict): The store data containing all required fields
            
        Returns:
            bool: True if data was stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO clothing (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                     (data.get('name'), data.get('dob'), data.get('pancard'), data.get('gst_number'), 
                      data.get('address'), data.get('business_name'), data.get('trade_license'), 
                      data.get('udyam'), data.get('account_number'), data.get('ifsc_code'), 
                      data.get('upi_id'), data.get('phoneNumber')))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing Clothing data: {e}")
            return False
    
    def store_handicraft_data(self, data):
        """
        Store Handicraft store registration data.
        
        Args:
            data (dict): The store data containing all required fields
            
        Returns:
            bool: True if data was stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO handicraft (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                     (data.get('name'), data.get('dob'), data.get('pancard'), data.get('gst_number'), 
                      data.get('address'), data.get('business_name'), data.get('trade_license'), 
                      data.get('udyam'), data.get('account_number'), data.get('ifsc_code'), 
                      data.get('upi_id'), data.get('phoneNumber')))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing Handicraft data: {e}")
            return False
    
    def store_restaurant_data(self, data):
        """
        Store Restaurant registration data.
        
        Args:
            data (dict): The store data containing all required fields
            
        Returns:
            bool: True if data was stored successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO restaurant (name, dob, pancard, gst_number, address, business_name, trade_license, udyam, account_number, ifsc_code, upi_id, fssai_number, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                     (data.get('name'), data.get('dob'), data.get('pancard'), data.get('gst_number'), 
                      data.get('address'), data.get('business_name'), data.get('trade_license'), 
                      data.get('udyam'), data.get('account_number'), data.get('ifsc_code'), 
                      data.get('upi_id'), data.get('fssai_number'), data.get('phoneNumber')))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing Restaurant data: {e}")
            return False
    
    def is_verified(self, phone_number):
        """
        Check if a phone number is verified.
        
        Args:
            phone_number (str): The phone number to check
            
        Returns:
            bool: True if the phone number is verified, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT verified FROM verification WHERE phoneNumber = ?", (phone_number,))
            result = c.fetchone()
            conn.close()
            
            if result:
                return bool(result[0])
            return False
        except Exception as e:
            print(f"Error checking verification status: {e}")
            return False
    
    def set_verified(self, phone_number, verified=True, store_type=None):
        """
        Set the verification status of a phone number.
        
        Args:
            phone_number (str): The phone number to set the status for
            verified (bool): The verification status
            store_type (str): The type of store associated with this phone number
            
        Returns:
            bool: True if the status was set successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Check if phone number exists
            c.execute("SELECT phoneNumber FROM verification WHERE phoneNumber = ?", (phone_number,))
            result = c.fetchone()
            
            if result:
                # Update existing record
                c.execute("UPDATE verification SET verified = ?, store_type = ? WHERE phoneNumber = ?", 
                         (verified, store_type, phone_number))
            else:
                # Insert new record
                c.execute("INSERT INTO verification (phoneNumber, verified, store_type) VALUES (?, ?, ?)", 
                         (phone_number, verified, store_type))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error setting verification status: {e}")
            return False

# Singleton instance to be imported
db_manager = DatabaseManager() 