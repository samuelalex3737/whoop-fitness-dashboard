"""
🔴 LIVE DATA GENERATOR SERVICE
==============================
Generates synthetic WHOOP fitness data in real-time
Simulates live data streaming from multiple users' WHOOP devices

Author: Samuel
Date: January 2026
"""

import pandas as pd
import numpy as np
import time
import os
import random
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================
LIVE_DATA_PATH = '/app/data/live_data.csv'
GENERATION_INTERVAL = 3  # Generate new data every 3 seconds
MAX_LIVE_RECORDS = 500   # Keep last 500 records for performance
NUM_ACTIVE_USERS = 25    # Simulate 25 active users

# ============================================================================
# SYNTHETIC DATA GENERATORS
# ============================================================================

class WHOOPDataGenerator:
    """Generates realistic WHOOP fitness data."""
    
    def __init__(self):
        self.users = self._create_user_profiles()
        self.activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 
                               'HIIT', 'Yoga', 'CrossFit', 'Cardio', 'Stretching', 
                               'Walking', 'Sports']
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                             'Friday', 'Saturday', 'Sunday']
        self.workout_times = ['Morning', 'Afternoon', 'Evening', 'Night']
        
    def _create_user_profiles(self):
        """Create persistent user profiles for realistic data."""
        users = {}
        genders = ['Male', 'Female', 'Other']
        fitness_levels = ['Beginner', 'Intermediate', 'Advanced', 'Elite']
        sports = ['Running', 'Cycling', 'CrossFit', 'Swimming', 'Weight Training', 
                  'Basketball', 'Soccer', 'Tennis', 'Golf', 'Mixed Training']
        
        for i in range(NUM_ACTIVE_USERS):
            user_id = f"LIVE_{i+1:05d}"
            fitness = random.choice(fitness_levels)
            
            # Base stats vary by fitness level
            base_recovery = {'Beginner': 55, 'Intermediate': 62, 'Advanced': 70, 'Elite': 78}
            base_hrv = {'Beginner': 45, 'Intermediate': 65, 'Advanced': 85, 'Elite': 110}
            
            users[user_id] = {
                'user_id': user_id,
                'age': random.randint(18, 65),
                'gender': random.choice(genders),
                'weight_kg': round(random.uniform(50, 100), 1),
                'height_cm': round(random.uniform(155, 195), 1),
                'fitness_level': fitness,
                'primary_sport': random.choice(sports),
                'base_recovery': base_recovery[fitness],
                'base_hrv': base_hrv[fitness],
                'base_rhr': random.randint(50, 75),
                'training_consistency': random.uniform(0.5, 0.95),  # How often they workout
            }
        return users
    
    def _get_current_context(self):
        """Get current time context for realistic data."""
        now = datetime.now()
        hour = now.hour
        
        # Determine workout probability based on time
        if 5 <= hour < 9:
            workout_prob = 0.4
            time_of_day = 'Morning'
        elif 11 <= hour < 14:
            workout_prob = 0.25
            time_of_day = 'Afternoon'
        elif 17 <= hour < 21:
            workout_prob = 0.5
            time_of_day = 'Evening'
        else:
            workout_prob = 0.1
            time_of_day = 'Night'
            
        return {
            'datetime': now,
            'day_of_week': self.days_of_week[now.weekday()],
            'workout_prob': workout_prob,
            'time_of_day': time_of_day,
            'hour': hour
        }
    
    def generate_live_record(self, user_profile):
        """Generate a single live data record for a user."""
        context = self._get_current_context()
        user = user_profile
        
        # Simulate whether user is working out
        is_workout = random.random() < (context['workout_prob'] * user['training_consistency'])
        
        # Recovery score with daily variation
        recovery_base = user['base_recovery']
        recovery_variation = random.gauss(0, 10)
        recovery_score = np.clip(recovery_base + recovery_variation, 1, 100)
        
        # Sleep data (simulated from last night)
        sleep_hours = round(random.gauss(7, 1.2), 2)
        sleep_hours = np.clip(sleep_hours, 4, 10)
        sleep_efficiency = round(random.gauss(82, 8), 1)
        sleep_efficiency = np.clip(sleep_efficiency, 50, 100)
        sleep_performance = round(random.gauss(85, 10), 1)
        sleep_performance = np.clip(sleep_performance, 40, 100)
        
        # Sleep stages
        deep_pct = random.uniform(0.15, 0.25)
        rem_pct = random.uniform(0.20, 0.28)
        light_pct = 1 - deep_pct - rem_pct
        
        light_sleep = round(sleep_hours * light_pct, 2)
        rem_sleep = round(sleep_hours * rem_pct, 2)
        deep_sleep = round(sleep_hours * deep_pct, 2)
        
        # HRV and vitals
        hrv = round(user['base_hrv'] + random.gauss(0, 15), 1)
        hrv = max(20, hrv)
        resting_hr = user['base_rhr'] + random.randint(-5, 8)
        respiratory_rate = round(random.gauss(14, 1.5), 1)
        skin_temp_dev = round(random.gauss(0, 0.5), 2)
        
        # Day strain (accumulated)
        if is_workout:
            day_strain = round(random.gauss(14, 3), 2)
        else:
            day_strain = round(random.gauss(6, 2), 2)
        day_strain = np.clip(day_strain, 0, 21)
        
        # Workout data
        if is_workout:
            activity_type = random.choice(self.activity_types)
            activity_duration = random.randint(20, 90)
            activity_strain = round(random.gauss(12, 4), 1)
            activity_strain = np.clip(activity_strain, 2, 20)
            
            # Heart rate zones
            avg_hr = random.randint(120, 165)
            max_hr = avg_hr + random.randint(15, 40)
            
            # Calories based on duration and intensity
            calories_per_min = random.uniform(8, 15)
            activity_calories = round(activity_duration * calories_per_min)
            
            # HR zone distribution
            total_zone_time = activity_duration
            z5 = round(total_zone_time * random.uniform(0.05, 0.15))
            z4 = round(total_zone_time * random.uniform(0.15, 0.25))
            z3 = round(total_zone_time * random.uniform(0.25, 0.35))
            z2 = round(total_zone_time * random.uniform(0.15, 0.25))
            z1 = total_zone_time - z5 - z4 - z3 - z2
            
            workout_completed = 1
            workout_time = context['time_of_day']
        else:
            activity_type = 'Rest Day'
            activity_duration = 0
            activity_strain = 0
            avg_hr = 0
            max_hr = 0
            activity_calories = 0
            z1 = z2 = z3 = z4 = z5 = 0
            workout_completed = 0
            workout_time = 'N/A'
        
        # Total calories burned
        bmr = 1800 + (user['weight_kg'] - 70) * 10
        total_calories = round(bmr + activity_calories + random.randint(-200, 300))
        
        return {
            'user_id': user['user_id'],
            'date': context['datetime'].strftime('%Y-%m-%d'),
            'timestamp': context['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'day_of_week': context['day_of_week'],
            'age': user['age'],
            'gender': user['gender'],
            'weight_kg': user['weight_kg'],
            'height_cm': user['height_cm'],
            'fitness_level': user['fitness_level'],
            'primary_sport': user['primary_sport'],
            'recovery_score': round(recovery_score, 1),
            'day_strain': day_strain,
            'sleep_hours': sleep_hours,
            'sleep_efficiency': sleep_efficiency,
            'sleep_performance': sleep_performance,
            'light_sleep_hours': light_sleep,
            'rem_sleep_hours': rem_sleep,
            'deep_sleep_hours': deep_sleep,
            'wake_ups': random.randint(0, 4),
            'time_to_fall_asleep_min': random.randint(5, 45),
            'hrv': hrv,
            'resting_heart_rate': resting_hr,
            'hrv_baseline': round(user['base_hrv'], 1),
            'rhr_baseline': user['base_rhr'],
            'respiratory_rate': respiratory_rate,
            'skin_temp_deviation': skin_temp_dev,
            'calories_burned': total_calories,
            'workout_completed': workout_completed,
            'activity_type': activity_type,
            'activity_duration_min': activity_duration,
            'activity_strain': activity_strain,
            'avg_heart_rate': avg_hr,
            'max_heart_rate': max_hr,
            'activity_calories': activity_calories,
            'hr_zone_1_min': z1,
            'hr_zone_2_min': z2,
            'hr_zone_3_min': z3,
            'hr_zone_4_min': z4,
            'hr_zone_5_min': z5,
            'workout_time_of_day': workout_time,
            'is_live': True
        }
    
    def generate_batch(self, num_records=5):
        """Generate a batch of live records from random users."""
        records = []
        selected_users = random.sample(list(self.users.values()), 
                                        min(num_records, len(self.users)))
        
        for user in selected_users:
            record = self.generate_live_record(user)
            records.append(record)
            
        return pd.DataFrame(records)


def initialize_live_data_file():
    """Create empty live data file with headers."""
    columns = [
        'user_id', 'date', 'timestamp', 'day_of_week', 'age', 'gender', 
        'weight_kg', 'height_cm', 'fitness_level', 'primary_sport',
        'recovery_score', 'day_strain', 'sleep_hours', 'sleep_efficiency',
        'sleep_performance', 'light_sleep_hours', 'rem_sleep_hours', 
        'deep_sleep_hours', 'wake_ups', 'time_to_fall_asleep_min',
        'hrv', 'resting_heart_rate', 'hrv_baseline', 'rhr_baseline',
        'respiratory_rate', 'skin_temp_deviation', 'calories_burned',
        'workout_completed', 'activity_type', 'activity_duration_min',
        'activity_strain', 'avg_heart_rate', 'max_heart_rate', 
        'activity_calories', 'hr_zone_1_min', 'hr_zone_2_min', 
        'hr_zone_3_min', 'hr_zone_4_min', 'hr_zone_5_min',
        'workout_time_of_day', 'is_live'
    ]
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(LIVE_DATA_PATH), exist_ok=True)
    
    df = pd.DataFrame(columns=columns)
    df.to_csv(LIVE_DATA_PATH, index=False)
    logger.info(f"Initialized live data file at {LIVE_DATA_PATH}")


def append_live_data(generator):
    """Append new live data records to the file."""
    # Generate 2-5 new records
    num_new = random.randint(2, 5)
    new_data = generator.generate_batch(num_new)
    
    try:
        # Read existing data
        if os.path.exists(LIVE_DATA_PATH):
            existing = pd.read_csv(LIVE_DATA_PATH)
            combined = pd.concat([existing, new_data], ignore_index=True)
            
            # Keep only the last MAX_LIVE_RECORDS
            if len(combined) > MAX_LIVE_RECORDS:
                combined = combined.tail(MAX_LIVE_RECORDS)
        else:
            combined = new_data
        
        # Write back
        combined.to_csv(LIVE_DATA_PATH, index=False)
        
        # Log stats
        workouts = new_data[new_data['workout_completed'] == 1]
        logger.info(
            f"📊 Generated {len(new_data)} records | "
            f"🏋️ {len(workouts)} workouts | "
            f"📈 Avg Recovery: {new_data['recovery_score'].mean():.1f}% | "
            f"💪 Avg Strain: {new_data['day_strain'].mean():.1f} | "
            f"📁 Total: {len(combined)} records"
        )
        
    except Exception as e:
        logger.error(f"Error appending live data: {e}")


def main():
    """Main loop for continuous data generation."""
    logger.info("=" * 60)
    logger.info("🔴 WHOOP LIVE DATA GENERATOR STARTING")
    logger.info("=" * 60)
    logger.info(f"📍 Output: {LIVE_DATA_PATH}")
    logger.info(f"⏱️  Interval: {GENERATION_INTERVAL} seconds")
    logger.info(f"👥 Active Users: {NUM_ACTIVE_USERS}")
    logger.info(f"📊 Max Records: {MAX_LIVE_RECORDS}")
    logger.info("=" * 60)
    
    # Initialize
    initialize_live_data_file()
    generator = WHOOPDataGenerator()
    
    logger.info(f"✅ Created {len(generator.users)} user profiles")
    logger.info("🚀 Starting live data generation loop...")
    logger.info("")
    
    cycle = 0
    while True:
        try:
            cycle += 1
            append_live_data(generator)
            time.sleep(GENERATION_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n⏹️  Stopping data generator...")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
