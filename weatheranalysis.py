import os
import csv

class WeatherReading:
    """Class to store individual weather readings."""
    def __init__(self, PKT, max_temp, min_temp, humidity):
        self.PKT = PKT
        self.max_temp = self._convert_to_float(max_temp)
        self.min_temp = self._convert_to_float(min_temp)
        self.humidity = self._convert_to_int(humidity)

    def _convert_to_float(self, value):
        try:
            return float(value) if value.strip() else None
        except (ValueError, AttributeError):
            return None

    def _convert_to_int(self, value):
        try:
            return int(value) if value.strip() else None
        except (ValueError, AttributeError):
            return None

    def __repr__(self):
        return f"WeatherReading(date={self.PKT}, max_temp={self.max_temp}, min_temp={self.min_temp}, humidity={self.humidity})"


class WeatherResult:
    """Class to calculate weather statistics."""
    def __init__(self, year):
        self.year = int(year)
        self.highest_temp = None
        self.lowest_temp = None
        self.highest_humidity = None
        self.monthly_temp_data = {}
        self.monthly_min_temp_data = {}
        self.monthly_humidity_data = {}

    def update_extremes(self, max_temp, min_temp, humidity):
        """Updates yearly extreme temperature and humidity values."""
        if max_temp is not None:
            self.highest_temp = max(self.highest_temp, max_temp) if self.highest_temp is not None else max_temp
        if min_temp is not None:
            self.lowest_temp = min(self.lowest_temp, min_temp) if self.lowest_temp is not None else min_temp
        if humidity is not None:
            self.highest_humidity = max(self.highest_humidity, humidity) if self.highest_humidity is not None else humidity

    def add_monthly_temp(self, month, max_temp, min_temp, humidity):
        """Stores temperature and humidity data for a specific month."""
        if max_temp is not None:
            self.monthly_temp_data.setdefault(month, []).append(max_temp)
        if min_temp is not None:
            self.monthly_min_temp_data.setdefault(month, []).append(min_temp)
        if humidity is not None:
            self.monthly_humidity_data.setdefault(month, []).append(humidity)

    def calculate_monthly_averages(self):
     """Calculates average temperature and humidity for each month."""
    
    # Ensure dictionary attributes exist before usage
     if not hasattr(self, 'monthly_avg_temp'):
        self.monthly_avg_temp = {}
     if not hasattr(self, 'monthly_avg_min_temp'):
        self.monthly_avg_min_temp = {}
     if not hasattr(self, 'monthly_avg_humidity'):
        self.monthly_avg_humidity = {}

     for month, temps in self.monthly_temp_data.items():
        valid_temps = [t for t in temps if t is not None]
        self.monthly_avg_temp[month] = sum(valid_temps) / len(valid_temps) if valid_temps else None

     for month, temps in self.monthly_min_temp_data.items():
        valid_temps = [t for t in temps if t is not None]
        self.monthly_avg_min_temp[month] = sum(valid_temps) / len(valid_temps) if valid_temps else None

     for month, humidities in self.monthly_humidity_data.items():
        valid_humidities = [h for h in humidities if h is not None]
        self.monthly_avg_humidity[month] = sum(valid_humidities) / len(valid_humidities) if valid_humidities else None


def yearly_extremes(weather_data):
    """Finds the highest temperature, lowest temperature, and highest humidity for a given year."""
    yearly_results = {}
    
    for reading in weather_data:
        try:
            year = int(reading.PKT.split('-')[0])  # Extract year from date
        except ValueError:
            continue

        yearly_results.setdefault(year, WeatherResult(year)).update_extremes(reading.max_temp, reading.min_temp, reading.humidity)

    return {year: {"max_temp": result.highest_temp, "min_temp": result.lowest_temp, "max_humidity": result.highest_humidity} for year, result in yearly_results.items()}


def monthly_averages(weather_data):
    """Calculates average monthly temperatures and humidity for each year."""
    yearly_results = {}

    for reading in weather_data:
        try:
            year, month = reading.PKT.split('-')[:2]  # Extract year and month
            year = int(year)
        except ValueError:
            continue

        yearly_results.setdefault(year, WeatherResult(year)).add_monthly_temp(month, reading.max_temp, reading.min_temp, reading.humidity)

    for result in yearly_results.values():
        result.calculate_monthly_averages()

    return {(year, month): {"avg_max_temp": result.monthly_avg_temp.get(month), "avg_min_temp": result.monthly_avg_min_temp.get(month), "avg_humidity": result.monthly_avg_humidity.get(month)} for year, result in yearly_results.items() for month in result.monthly_avg_temp}


class WeatherParser:
    """Class to parse weather files and store data."""
    def __init__(self, directory="weatherfiles"):
        self.directory = directory
        self.weather_data = []

    def parse_files(self):
        """Reads all files in the directory and extracts weather data."""
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.directory, filename), "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip the header

                    for row in reader:
                        if len(row) >= 4:
                            self.weather_data.append(WeatherReading(row[0], row[1], row[2], row[3]))

    def get_data(self):
        """Returns parsed weather data as a list of WeatherReading objects."""
        return self.weather_data


def loadweather_data(directory="weatherfiles"):
    """Loads weather data from files and returns structured results."""
    parser = WeatherParser(directory)
    parser.parse_files()
    weather_data = parser.get_data()
    
    return {"yearly_extremes": yearly_extremes(weather_data), "monthly_averages": monthly_averages(weather_data)}
