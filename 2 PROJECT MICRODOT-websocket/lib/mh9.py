from machine import ADC, Pin

# Inisialisasi ADC pada pin GP26
adc = ADC(Pin(26))

# Konstanta kalibrasi (misalnya, berdasarkan percobaan atau datasheet sensor)
ZERO_POINT_VOLTAGE = 0.4  # Tegangan nol (dalam volt) untuk lingkungan bebas CO
SENSITIVITY = 0.05  # Sensitivitas dalam volt per ppm (misalnya, 0.05 V/ppm)

def read_adc():
    """
    Membaca nilai ADC dan mengonversi ke tegangan.
    
    Returns:
        float: Tegangan yang diukur (dalam volt).
    """
    raw_value = adc.read_u16()  # Baca nilai 16-bit dari ADC
    voltage = raw_value * 3.3 / 65535  # Konversi nilai ADC ke tegangan (dalam volt)
    return voltage

def calculate_co_concentration(voltage):
    """
    Menghitung konsentrasi CO berdasarkan tegangan yang diukur.
    
    Args:
        voltage (float): Tegangan yang diukur (dalam volt).
        
    Returns:
        float: Konsentrasi CO (dalam ppm).
    """
    if voltage < ZERO_POINT_VOLTAGE:
        return 0  # Jika tegangan lebih rendah dari titik nol, asumsikan 0 ppm
    else:
        concentration = (voltage - ZERO_POINT_VOLTAGE) / SENSITIVITY
        return concentration

def get_co_concentration():
    """
    Mengambil konsentrasi CO langsung dari pembacaan sensor.
    
    Returns:
        float: Konsentrasi CO (dalam ppm).
    """
    voltage = read_adc()
    return calculate_co_concentration(voltage)