import calendar
class WeatherReportGenerator:
    def __init__(self, calculations):
        """Initializes the report generator with the calculation results."""
        self.calculations = calculations
    # def generate_yearly_report(self, year):
    #     """Generates a report for a specific year's extreme temperatures and humidity."""
    #     year = str(year).strip()  # Ensure year is a string

    #     # Debugging: Print available years before checking
    #     print("Available Years in yearly_extremes:", self.calculations['yearly_extremes'].keys())

        # report = f"Weather Report for {year}:\n"
        # if year in self.calculations['yearly_extremes']:
        #     data = self.calculations['yearly_extremes'][year]
        #     report += (f"Highest Temperature: {data['max_temp']:.2f}°C\n"
        #                f"Lowest Temperature: {data['min_temp']:.2f}°C\n"
        #                f"Highest Humidity: {data['max_humidity']:.2f}%\n\n")
        # else:
        #     report += "No data available for this year.\n"

        # return report
    def generate_yearly_report(self, year):
        """Generates a report for a specific year's extreme temperatures and humidity."""
        year = str(year).strip()  # Ensure year is a string

        if year in self.calculations['yearly_extremes']:
            data = self.calculations['yearly_extremes'][year]
            report = (f"Weather Report for {year}:\n"
                      f"Highest Temperature: {data['max_temp']}°C on {data['max_temp_day']}\n"
                      f"Lowest Temperature: {data['min_temp']}°C on {data['min_temp_day']}\n"
                      f"Most Humid Day: {data['max_humidity']}% on {data['max_humidity_day']}\n")
        else:
            report = f"Weather Report for {year}:\nNo data available for this year."

        return report



    def generate_monthly_report(self, year):
        """Generates a report for a specific year's monthly average temperatures and humidity."""
        year = str(year).strip()

        report = f"Monthly Weather Averages for {year}:\n"
        has_data = False

        # Debugging: Print available keys in monthly_averages
        print("Available Keys in monthly_averages:", self.calculations['monthly_averages'].keys())

        for key, data in self.calculations['monthly_averages'].items():
            if isinstance(key, str) and "-" in key:
                y, month = key.split("-")  
                y = str(y).strip()
            elif isinstance(key, tuple) and len(key) == 2:
                y, month = key
                y = str(y).strip()
            else:
                print("Skipping key with unknown format:", key)
                continue  # Skip unrecognized formats

            if y == year:
                has_data = True
                month = int(month)
                report += (f"{calendar.month_name[month]}:\n"
                           f"Average Max Temperature: {data['avg_max_temp']:.2f}°C\n"
                           f"Average Min Temperature: {data['avg_min_temp']:.2f}°C\n"
                           f"Average Humidity: {data['avg_humidity']:.2f}%\n\n")

        if not has_data:
            report += "No data available for this year.\n"

        return report
