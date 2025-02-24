from flask import Flask, render_template, request
from weatherreport import WeatherReportGenerator
from weatheranalysis import loadweather_data, yearly_summary, draw_temperature_bars  # Fixed imports

app = Flask(__name__)

# Load data once when the app starts
weather_data = loadweather_data("weatherfiles/")
if not weather_data:
    print(" Warning: No weather data loaded!")

report_generator = WeatherReportGenerator(weather_data)

@app.route('/')
def index():
    return render_template("weatherreport.html")

@app.route('/report')
def report():
    year = request.args.get('year')

    if not year or not year.strip().isdigit():
        return " Error: Please provide a valid numeric year!", 400

    year = str(year).strip()

    # Debugging outputs
    print(f" Requested Year: {year}")
    print(" Available Years in yearly_extremes:", report_generator.calculations.get('yearly_extremes', {}).keys())
    print(" Available Keys in monthly_averages:", report_generator.calculations.get('monthly_averages', {}).keys())

    yearly_report = report_generator.generate_yearly_report(year)
    monthly_report = report_generator.generate_monthly_report(year)

    if not yearly_report and not monthly_report:
        return f" No data found for {year}!", 404

    yearly_summary_report = yearly_summary(year)

    return render_template(
        "weatherreport.html",
        yearly_report=yearly_report,
        monthly_report=monthly_report,
        yearly_summary=yearly_summary_report
    )

@app.route('/temperature-bars')
def temperature_bars():
    """Endpoint to draw horizontal bar charts for a given month."""
    year = request.args.get('year')
    month = request.args.get('month')

    if not year or not month or not year.isdigit() or not month.isdigit():
        return " Error: Please provide valid numeric year and month!", 400

    year, month = int(year), int(month)
    draw_temperature_bars(year, month)  # Calls the console-based bar chart function

    return f" Temperature bars for {year}-{month:02d} displayed in the console."

if __name__ == "__main__":
    app.run(debug=True)
