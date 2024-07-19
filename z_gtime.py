import swisseph as swe
from datetime import datetime, timedelta
import math
import matplotlib.pyplot as plt
import numpy as np

def get_utc_offset(date, time, place):
    # Function to get UTC offset for given date, time, and place
    # Note: Implement using an appropriate library or API
    return -4  # Placeholder for UTC offset (e.g., EDT for New York)

def get_julian_day(year, month, day, hour):
    # Convert the date and time to Julian Day
    return swe.julday(year, month, day, hour)

def get_sidereal_time(julian_day, longitude):
    # Calculate Greenwich Sidereal Time (GST)
    gst = swe.sidtime(julian_day)
    # Convert GST to Local Sidereal Time (LST)
    lst = gst + (longitude / 15.0)
    return lst % 24

def calculate_house_positions(lst, latitude):
    # Calculate the positions of the houses using Placidus house system
    # Returns a list of house cusps (angles)
    houses = swe.houses(lst, latitude, 'P')
    return houses[0]

def calculate_planetary_positions(julian_day):
    # Calculate the positions of the planets
    planets = {}
    for planet in range(swe.SUN, swe.PLUTO + 1):
        position = swe.calc_ut(julian_day, planet, swe.FLG_SWIEPH)[0]
        planets[swe.get_planet_name(planet)] = position[0] % 360
    return planets

def organize_houses(planets, houses):
    # Organize planets into houses
    planet_houses = {}
    for planet, position in planets.items():
        for i in range(1, 13):
            if houses[i - 1] <= position < houses[i % 12]:
                planet_houses[planet] = i
                break
    return planet_houses

def plot_houses_and_planets(houses, planet_houses):
    # Create a plot to display houses and planets
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)  # Counter-clockwise rotation
    ax.set_theta_offset(np.pi / 2.0)  # Set 0 degrees (Ascendant) at the top

    # Plot the house cusps
    for i, cusp in enumerate(houses):
        ax.plot([np.deg2rad(cusp), np.deg2rad(cusp)], [0, 1], label=f'House {i+1}')
    
    # Plot the planets
    planet_colors = plt.cm.tab20(np.linspace(0, 1, len(planet_houses)))
    for planet, house in planet_houses.items():
        cusp_start = np.deg2rad(houses[house - 1])
        cusp_end = np.deg2rad(houses[house % 12])
        cusp_mid = (cusp_start + cusp_end) / 2.0
        ax.text(cusp_mid, 0.5, planet, color=planet_colors[house - 1], ha='center', va='center')

    # Add labels and title
    ax.set_xticks(np.linspace(0, 2 * np.pi, 12, endpoint=False))
    ax.set_xticklabels([f'House {i+1}' for i in range(12)])
    ax.set_yticklabels([])
    ax.set_title('Astrological Houses and Planets')

    plt.legend()
    plt.show()

def main():
    # Step 1: Get user input for date, time, and place of birth
    date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
    time_of_birth = input("Enter your time of birth (HH:MM): ")
    place_of_birth = input("Enter your place of birth (City, Country): ")
    
    # For demonstration purposes, use a fixed UTC offset and latitude/longitude
    # In a real implementation, you would get these values using an appropriate library or API
    utc_offset = get_utc_offset(date_of_birth, time_of_birth, place_of_birth)
    latitude = 40.7128  # Latitude for New York, USA
    longitude = -74.0060  # Longitude for New York, USA

    # Step 2: Parse the date and time of birth
    dob = datetime.strptime(date_of_birth + ' ' + time_of_birth, '%Y-%m-%d %H:%M')
    dob_utc = dob - timedelta(hours=utc_offset)
    year, month, day, hour = dob_utc.year, dob_utc.month, dob_utc.day, dob_utc.hour + dob_utc.minute / 60.0

    # Step 3: Calculate Julian Day
    julian_day = get_julian_day(year, month, day, hour)

    # Step 4: Calculate Local Sidereal Time
    lst = get_sidereal_time(julian_day, longitude)

    # Step 5: Calculate house positions
    houses = calculate_house_positions(lst, latitude)

    # Step 6: Calculate planetary positions
    planets = calculate_planetary_positions(julian_day)

    # Step 7: Organize planets into houses
    planet_houses = organize_houses(planets, houses)

    # Output the results
    print("Planetary Positions:")
    for planet, position in planets.items():
        print(f"{planet}: {position:.2f}°")
    
    print("\nPlanetary Houses:")
    for planet, house in planet_houses.items():
        print(f"{planet} is in House {house}")

    # Step 8: Plot the results
    plot_houses_and_planets(houses, planet_houses)

if __name__ == "__main__":
    main()
