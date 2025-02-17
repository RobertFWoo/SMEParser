import re
from datetime import datetime, timedelta

data = """
Sun, Moon & Earth - 6.1     © 1998-2015 Juergen Giesen
User: replace
  Location:  User Input
  Latitude:  31.766666666666666° N = 31° 46.0' N
  Longitude: 36.2° E = 36° 12.0' E
  Date/Time: Mon Jan 19 16:58:00 GMT-06:00 2026
  UT:        Mon Jan 19 14:58:00 UT 2026
  Time Zone: UT + 2:00 h
  Jul. Day:  2461060.123611111
  Equation of Time        = -10:45 min  = prev. day  -18.5 s
  Local Sidereal Time     = 19.7172° = 19° 43.0' = 1h 18m 52.1s
  Greenwich Sidereal Time = 343.5172° = 343° 31.0' = 22h 54m 4.1s
  SUN:
    Right Asc. RA = 301.7072° = 20h 06m 49.7s
    Ecl. Long. L  = 299.5451° = 299° 32.7' (Capricornus 29° 32.7')
    Distance from Earth = 0.98394 AU,  Diameter = 32.51'
    Declin.= 20.2453° S = 20° 14.7' S
    GHA    = 41.8° = 41° 48.3'
    LHA    = 78.0° = 78° 00.3'
    Alt.= -1.06° = -1° 3.7'
    Az.= 246.4°  (WSW)
    Begin astr. twilight  05:09   01:25 h before rise
    Begin naut. twilight  05:38   00:56 h before rise
    Begin civil twilight  06:08   00:26 h before rise
    Sunrise               06:34   Azim. = 113.5°(ESE), Moon Azim. null
                                  daz = 0.0°,  dalt null
    Transit               11:46   Altit.= 37.8°
    Sunset                16:58   Azim. = 246.6° (WSW), Moon Azim. null
                                  daz = 0.0°,  dalt null
    End civil twilight    17:24   00:26 h after set
    End naut. twilight    17:54   00:56 h after set
    End astr. twilight    18:23   01:25 h after set
    Minimum altitude at   23:46   -78.7°
    Length of Day:   10 h 23.1 min = length of prev. day  + 1.2 min
  MOON:
    Prev. New Moon: Sun 2026 Jan 18 at 19:51 UT
    Moon Age 0.7966 d = 00 d 19 h 07 m 
    waxing crescent
    Next New Moon:  Tue 2026 Feb 17 at 12:03 UT
    Illum. Frac.  = 0.6 % (+)
    Bright limb angle   = -142° to zenith
    Distance from Earth = 392633 km,  Diameter = 30.49'
    Declin.= 20.6244° S = 20° 37' S
    Right Asc. RA = 311.3956° = 20h 45m 34.9s
    Ecl. Long. L  = 308.7411° = 308° 44.5' (Aquarius 8° 44.5')
    GHA    = 31.61° = 31° 36.5'
    LHA    = 67.81° = 67° 48.5'
    Alt.= 5.8°
    Az.= 240.7°  (WSW)
    Rise     07:07   Azim. = 116.6° (ESE)
    Transit  12:17   Altit.= 36.0°
    Set      17:34   Azim. = 245.6° (WSW)   Above horizon:   10:27 hours
    Geocentric Elong. = 9.56°
"""

# Function to extract information using regular expressions
def extract_info(regex, text, flags=0):
    match = re.search(regex, text, flags)
    return match.group(1) if match else None

# Extracting information
latitude = float(extract_info(r'Latitude:\s*([\d.]+)° N', data))
longitude = float(extract_info(r'Longitude:\s*([\d.]+)° E', data))
datetime_str = extract_info(r'Date/Time:\s*([A-Za-z]+\s[A-Za-z]+\s\d+\s\d+:\d+:\d+\sGMT[+-]\d+:\d+\s\d+)', data)
datetime_obj = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S GMT%z %Y')
time_zone = extract_info(r'Time Zone:\s*(UT\s*[+-]\s*\d+:\d+\s*h)', data)

# Extracting information about the Sun
sun_altitude = float(extract_info(r'SUN:.*?Alt\.\s*=\s*([-\d.]+)°', data, re.DOTALL))
sun_azimuth = float(extract_info(r'SUN:.*?Az\.\s*=\s*([\d.]+)°', data, re.DOTALL))

# Extracting information about the Moon
moon_age_days = float(extract_info(r'Moon Age\s*([\d.]+)\s*d', data))
moon_age_hours = int((moon_age_days * 24) % 24)
moon_age_minutes = int((moon_age_days * 24 * 60) % 60)
moon_age = f"{int(moon_age_days)} days, {moon_age_hours} hours, {moon_age_minutes} minutes"
illumination_fraction = f"{float(extract_info(r'Illum\. Frac\.\s*=\s*([\d.]+)', data))}%"
moon_distance_km = int(extract_info(r'Distance from Earth = ([\d,]+) km', data).replace(',', ''))
# Assuming average apogee of 405,500 km and perigee of 363,300 km for the Moon
moon_distance_percentage = 100 - ((moon_distance_km - 363300) / (405500 - 363300) * 100)
moon_distance = f"{moon_distance_km} km ({moon_distance_percentage:.3f}%)"
moon_declination = float(extract_info(r'Declin\.\s*=\s*([\d.]+)° S', data))
moon_declination_percentage = 100 * (moon_declination + 28.6) / (28.6 * 2)
moon_declination_str = f"{moon_declination} (deg) ({moon_declination_percentage:.3f}%)"
moon_altitude = float(extract_info(r'MOON:.*?Alt\.\s*=\s*([-\d.]+)°', data, re.DOTALL))
moon_azimuth = float(extract_info(r'MOON:.*?Az\.\s*=\s*([\d.]+)°', data, re.DOTALL))
moon_set_time_str = extract_info(r'Set\s*([\d:]+)', data)
geocentric_elongation = extract_info(r'Geocentric Elong\.\s*=\s*([\d.]+)°', data)

# Convert time strings to datetime objects
date_str = extract_info(r'Date/Time:\s*([A-Za-z]+\s[A-Za-z]+\s\d+\s\d+:\d+:\d+\sGMT[+-]\d+:\d+\s\d+)', data)
date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S GMT%z %Y')
moon_set_time = datetime.strptime(moon_set_time_str, '%H:%M').replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)
sunset_time_str = extract_info(r'Sunset\s*([\d:]+)', data)
sunset_time = datetime.strptime(sunset_time_str, '%H:%M').replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)

# Calculate differentials and lag time
differential_azimuth = sun_azimuth - moon_azimuth
differential_altitude = sun_altitude - moon_altitude
lag_time = (moon_set_time - sunset_time).total_seconds() / 60

# Output the extracted information and calculations
print("Latitude:", f"{latitude:.3f} (deg)")
print("Longitude:", f"{longitude:.3f} (deg)")
print("Date/Time:", datetime_obj)
print("Time Zone:", time_zone)
print("Sun's Altitude:", f"{sun_altitude:.3f} (deg)")
print("Sun's Azimuth:", f"{sun_azimuth:.3f} (deg)")
print("Moon Age:", moon_age)
print("Illumination Fraction:", illumination_fraction)
print("Distance of Moon from Earth:", moon_distance)
print("Moon's Declination:", moon_declination_str)
print("Moon's Altitude:", f"{moon_altitude:.3f} (deg)")
print("Moon's Azimuth:", f"{moon_azimuth:.3f} (deg)")
print("Moon's Set Time:", moon_set_time)
print("Geocentric Elongation:", f"{geocentric_elongation} (deg)")
print("Differential Azimuth (Sun - Moon):", f"{differential_azimuth:.3f} (deg)")
print("Differential Altitude (Sun - Moon):", f"{differential_altitude:.3f} (deg)")
print("Lag Time (Moonset - Sunset):", f"{lag_time:.0f} minutes")
