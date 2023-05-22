# In your Django views.py file

from django.shortcuts import render
from django.http import HttpResponse

def gravity_correction(request):
    if request.method == 'POST':
        # Get the input values from the form
        latitude = float(request.POST['latitude'])
        elevation = float(request.POST['elevation'])
        observed_gravity = float(request.POST['observed_gravity'])
        correction_type = request.POST['correction_type']

        # Perform the gravity correction based on the selected correction type
        corrected_gravity = calculate_gravity_correction(latitude, elevation, observed_gravity, correction_type)

        # Return the corrected gravity value to the user
        return HttpResponse(f"Corrected Gravity: {corrected_gravity}")

    return render(request, 'gravity_correction.html')

def calculate_gravity_correction(latitude, elevation, observed_gravity, correction_type):
    # Constants for gravity corrections
    G = 6.67430e-11                                 # Gravitational constant in m^3 kg^−1 s^−2
    equatorial_radius = 6378137.0                   # Equatorial radius of the Earth in meters
    polar_radius = 6356752.0                        # Polar radius of the Earth in meters
    geocentric_gravity = 9.7803267714               # Geocentric gravitational acceleration in m/s^2
    density_of_earth = 5515                         # Average density of the Earth in kg/m^3

    if correction_type == 'free_air':
        # Free-Air Correction
        free_air_correction = 0.3086 * elevation
        corrected_gravity = observed_gravity + free_air_correction

    elif correction_type == 'bouguer':
        # Bouguer Correction
        bouguer_correction = 0.0419 * elevation
        corrected_gravity = observed_gravity + bouguer_correction

    elif correction_type == 'terrain':
        # Terrain Correction
        terrain_correction = 0.0419 * elevation - 0.1036 * elevation**2
        corrected_gravity = observed_gravity + terrain_correction

    elif correction_type == 'eotvos':
        # Eötvös Correction
        omega = 7.292115e-5  # Angular velocity of the Earth in rad/s
        eotvos_correction = 0.031 * latitude * (omega**2) * (equatorial_radius**2) * (polar_radius**2) / G
        corrected_gravity = observed_gravity + eotvos_correction

    elif correction_type == 'latitude':
        # Latitude Correction
        latitude_correction = 0.0053024 * (latitude**2) + 0.0000058 * (latitude**4)
        corrected_gravity = observed_gravity + latitude_correction

    elif correction_type == 'igf':
        # International Gravity Formula (IGF)
        latitude_radians = latitude * (3.14159265359 / 180.0)
        height_ratio = elevation / 1000.0
        igf_correction = geocentric_gravity * ((1 + 0.00193185138639 * (latitude_radians**2)) /
                                               (1 - 0.00264639562867 * (latitude_radians**2)) - 1) * height_ratio
        corrected_gravity = observed_gravity + igf_correction

    else:
        # Invalid correction type
        raise ValueError("Invalid gravity correction type.")

    return corrected_gravity

