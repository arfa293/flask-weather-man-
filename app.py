from flask import Flask, render_template, request
from weatherreport import WeatherReportGenerator
from weatheranalysis import loadweather_data  

app = Flask(__name__)

# Load data once when the app starts
weather_data = loadweather_data("weatherfiles/")  
report_generator = WeatherReportGenerator(weather_data)  # ✅ Initialize the report generator

@app.route('/')
def index():
    return render_template("weatherreport.html")  # Ensure this template exists

@app.route('/report')
def report():
    year = request.args.get('year')

    if not year:
        return "Please provide a year!", 400

    year = str(year).strip()  # Ensure year is a string and remove extra spaces

    # ✅ Debugging: Print available years in data
    print("Available Years in yearly_extremes:", report_generator.calculations['yearly_extremes'].keys())
    print("Available Keys in monthly_averages:", report_generator.calculations['monthly_averages'].keys())

    yearly_report = report_generator.generate_yearly_report(year)
    monthly_report = report_generator.generate_monthly_report(year)

    return render_template("weatherreport.html", yearly_report=yearly_report, monthly_report=monthly_report)

if __name__ == "__main__":
    app.run(debug=True)
