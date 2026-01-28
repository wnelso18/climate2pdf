import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, timedelta
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tkintermapview
from ttkthemes import ThemedTk
import random

# Replace with your API key
VISUAL_CROSSING_API_KEY = "YOUR_API_KEY_HERE"  # From visualcrossing.com

# List of 50 obscure weather facts
WEATHER_FACTS = [
    "The smell of rain is caused by a bacteria called actinomycetes, which releases a scent when it gets wet.",
    "A single lightning bolt can heat the air around it to 54,000°F, five times hotter than the surface of the sun.",
    "The windiest place on Earth is Commonwealth Bay in Antarctica, with gusts reaching over 150 mph.",
    "A 'derecho' is a widespread, long-lived wind storm associated with a band of rapidly moving showers or thunderstorms.",
    "In 1922, a single day in Libya saw a temperature swing of 100°F, from 32°F to 132°F.",
    "The largest hailstone ever recorded fell in Vivian, South Dakota, in 2010, weighing 1.94 pounds and measuring 8 inches in diameter.",
    "A 'snow roller' is a rare natural phenomenon where wind rolls snow into a cylindrical shape, resembling a snowman’s body.",
    "The term 'blizzard' originally referred to a volley of gunfire before it was used to describe a severe snowstorm in the 1870s.",
    "In 1986, a rain of fish fell in Sri Lanka, likely caused by a waterspout lifting them from the ocean.",
    "The highest recorded wind speed from a tornado was 318 mph, measured in Oklahoma City on May 3, 1999.",
    "A 'haboob' is a massive dust storm that can reduce visibility to near zero, often seen in arid regions like the Sahara.",
    "The coldest temperature ever recorded on Earth was -128.6°F at Vostok Station, Antarctica, on July 21, 1983.",
    "A 'thundersnow' is a rare thunderstorm where snow falls instead of rain, often accompanied by muffled thunder.",
    "The wettest place on Earth, Mawsynram, India, receives an average of 467 inches of rain annually.",
    "A 'fire whirl' is a tornado-like vortex of flames that can form during intense wildfires, reaching heights of 1,000 feet.",
    "In 1816, known as the 'Year Without a Summer,' volcanic ash from Mount Tambora caused global cooling and snow in June.",
    "The longest-lasting rainbow ever recorded was observed for nearly 9 hours in Taipei, Taiwan, on November 30, 2017.",
    "A 'moonbow' is a rainbow caused by moonlight instead of sunlight, often appearing white to the human eye.",
    "The driest place on Earth, the Atacama Desert in Chile, has areas that haven’t seen rain in over 400 years.",
    "A 'snownado' is a rare vortex of snow and wind, resembling a small tornado, often seen in open snowy fields.",
    "In 1972, Iran experienced a blizzard that buried villages under 26 feet of snow, the deadliest snowstorm on record.",
    "A 'heat burst' is a sudden spike in temperature at night caused by a dying thunderstorm, sometimes raising temps by 20°F in minutes.",
    "The highest rainfall in a single minute was 1.23 inches, recorded in Unionville, Maryland, on July 4, 1956.",
    "A 'frost quake' occurs when frozen ground suddenly cracks due to rapid temperature drops, creating loud booms.",
    "The largest snowflake ever recorded was 15 inches wide, observed in Montana in 1887.",
    "A 'petrichor' is the earthy scent produced when rain falls on dry soil, derived from plant oils and bacteria.",
    "The most lightning strikes in a single place occur in Tororo, Uganda, with more strikes per square kilometer than anywhere else.",
    "A 'ball lightning' is a rare phenomenon where a glowing orb of electricity floats through the air during a storm.",
    "The highest temperature ever recorded was 134°F in Death Valley, California, on July 10, 1913.",
    "A 'cloudburst' is an extreme rain event where several inches can fall in minutes, often causing flash floods.",
    "In 2001, a red rain fell in Kerala, India, later found to be caused by airborne spores from local algae.",
    "A 'polar vortex' is a large area of low pressure and cold air surrounding the Earth’s poles, which can cause severe cold snaps.",
    "The longest recorded drought lasted 400 years in the Atacama Desert, from the 1500s to the 1900s.",
    "A 'green flash' is a rare optical phenomenon where a green spot is visible above the sun at sunrise or sunset.",
    "The most powerful hurricane on record, Hurricane Patricia in 2015, had sustained winds of 215 mph.",
    "A 'diamond dust' is a cloud of tiny ice crystals that sparkle in the sunlight, often seen in polar regions.",
    "The term 'hurricane' comes from the Taino word 'huracan,' meaning 'god of the storm.'",
    "A 'microburst' is a sudden, powerful downdraft of air that can cause wind speeds exceeding 100 mph.",
    "In 1994, a storm in Bolivia produced hailstones the size of grapefruits, causing widespread damage.",
    "A 'weather bomb' is a rapidly intensifying storm where the pressure drops at least 24 millibars in 24 hours.",
    "The most tornadoes in a single day—148—occurred on April 3, 1974, during the 'Super Outbreak' in the U.S.",
    "A 'fogbow' is a faint, white rainbow-like arc formed by tiny water droplets in fog.",
    "The highest recorded wave caused by a storm was 112 feet, observed in the Pacific Ocean in 1933.",
    "A 'sandstorm' can carry sand particles over 3,000 miles, as seen when Sahara dust reaches the Americas.",
    "The term 'El Niño' was originally used by Peruvian fishermen to describe a warm ocean current around Christmas.",
    "A 'blue jet' is a type of lightning that shoots upward from thunderstorm clouds into the stratosphere.",
    "The most expensive weather disaster in history was Hurricane Katrina in 2005, causing $125 billion in damages.",
    "A 'snow squall' is a sudden, intense burst of snow and wind that can cause whiteout conditions in minutes.",
    "The longest recorded thunderstorm lasted 192 hours in southern India in 2014.",
    "A 'glory' is a set of concentric, pastel-colored rings surrounding the shadow of an observer, often seen from planes.",
    "The term 'monsoon' comes from the Arabic word 'mausim,' meaning 'season,' referring to seasonal wind shifts."
]

def fetch_weather_data(lat, lon, start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = start_date
    start_date = start_date - timedelta(days=6)
    
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?unitGroup=us&key={VISUAL_CROSSING_API_KEY}&include=days&elements=datetime,precip"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        precip_data = {}
        for day in data["days"]:
            date_str = day["datetime"]
            precip = day["precip"] if day["precip"] is not None else 0.0
            precip_data[date_str] = precip
            print(f"Fetched {date_str}: WTR = {precip}")
        
        return precip_data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {}

def capitalize_town(town):
    """Capitalize the first letter of each word in the town name."""
    if not town:
        return "Unknown Location"
    return ", ".join(word.capitalize() for word in town.split(","))

def generate_report(lat, lon, start_date, output_filename, town_name):
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    precip_data = fetch_weather_data(lat, lon, start_date)
    
    if not precip_data:
        return None
    
    forty_eight_hr_total = sum(precip_data[date_str] for date_str in precip_data 
                               if datetime.strptime(date_str, "%Y-%m-%d") >= start_date_dt - timedelta(days=1) 
                               and datetime.strptime(date_str, "%Y-%m-%d") <= start_date_dt)
    seven_day_total = sum(precip_data.values())
    
    if not output_filename.endswith('.pdf'):
        output_filename += '.pdf'
    
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Use the user-provided town name in the title
    town_name = capitalize_town(town_name)
    elements.append(Paragraph(f"Weather Report for {town_name} - 7 Days Ending {start_date}", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Daily Precipitation (in inches):", styles['Heading2']))
    table_data = [["Date", "Precipitation (in)"]]
    for date, precip in sorted(precip_data.items()):
        table_data.append([date, f"{precip:.2f}"])
    table = Table(table_data, colWidths=[100, 100])
    table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    elements.append(table)
    
    # Add coordinates below the table, centered, same font size as table data
    elements.append(Spacer(1, 12))
    coord_style = styles['BodyText']  # Matches table data font size (default 10pt)
    coord_style.alignment = 1  # Center alignment
    elements.append(Paragraph(f"Coordinates: {lat:.4f}, {lon:.4f}", coord_style))
    
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Precipitation Totals:", styles['Heading2']))
    elements.append(Paragraph(f"48 Hours Before {start_date}: {forty_eight_hr_total:.2f} in", styles['BodyText']))
    elements.append(Paragraph(f"7 Days Before {start_date}: {seven_day_total:.2f} in", styles['BodyText']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Sources: Visual Crossing Weather API", styles['Normal']))
    elements.append(Paragraph('<a href="https://www.visualcrossing.com/resources/documentation/weather-data/how-we-process-integrated-surface-database-historical-weather-data/" color="blue">How We Process Integrated Surface Database Historical Weather Data</a>', styles['Normal']))
    
    doc.build(elements)
    return output_filename

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Report Generator")
        self.root.geometry("900x900")
        
        # Apply modern theme
        self.root.configure(bg="#666666")
        style = ttk.Style()
        style.theme_use('equilux')
        style.configure('TLabel', background="#666666", foreground="#ff9900", font=('Calibri', 10))
        style.configure('TButton', font=('Calibri', 10, 'bold'), padding=5)
        style.map('TButton', background=[('active', "#ff9900")], foreground=[('active', '#ff9900')])

        # Random weather fact display
        random_fact = random.choice(WEATHER_FACTS)
        self.fact_label = ttk.Label(root, text=f"Weather Fact: {random_fact}", font=('Calibri', 12, 'italic'), wraplength=750)
        self.fact_label.pack(pady=10)

        # Date entry
        ttk.Label(root, text="Starting Date (YYYY-MM-DD):").pack(pady=10)
        self.date_entry = ttk.Entry(root)
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, "2025-03-18")

        # Town/City entry
        ttk.Label(root, text="Town/City Name:").pack(pady=10)
        self.town_entry = ttk.Entry(root)
        self.town_entry.pack(pady=5)
        self.town_entry.insert(0, "Knoxville")

        # Output file selection
        ttk.Label(root, text="Output File:").pack(pady=10)
        self.filename_label = ttk.Label(root, text="No file selected")
        self.filename_label.pack(pady=5)
        self.browse_btn = ttk.Button(root, text="Browse Files", command=self.browse_file)
        self.browse_btn.pack(pady=5)

        # Map widget
        ttk.Label(root, text="Click on the map to select a location or type project coordinates:").pack(pady=10)
        self.coords_entry = ttk.Entry(root)
        self.coords_entry.pack(pady=5)
        self.coords_entry.insert(0, "35.9642, -83.9226")
        self.mapcoords_btn = ttk.Button(root, text="Set Coordinates", command=lambda: self.set_coordinates(tuple(map(float, self.coords_entry.get().split(',')))))
        self.mapcoords_btn.pack(pady=5)

        self.map_widget = tkintermapview.TkinterMapView(root, width=500, height=300, corner_radius=5)
        self.map_widget.pack(pady=10)
        self.map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}")
        self.map_widget.set_position(35.9642, -83.9226)
        self.map_widget.set_zoom(8)
        self.marker = None

        # Bind left-click to set coordinates
        self.map_widget.add_left_click_map_command(self.set_coordinates)

        # Coordinates display
        self.coords_label = ttk.Label(root, text="Coordinates: Not set")
        self.coords_label.pack(pady=5)

        # Generate button
        self.generate_btn = ttk.Button(root, text="Generate Report", command=self.generate_report)
        self.generate_btn.pack(pady=15)

        # Status label
        self.status = ttk.Label(root, text="")
        self.status.pack(pady=5)

        # Store selected coordinates and filename
        self.lat = None
        self.lon = None
        self.output_filename = None

    def set_coordinates(self, coords):
        self.lat, self.lon = coords
        self.coords_label.config(text=f"Coordinates: {self.lat:.4f}, {self.lon:.4f}")
        if self.marker:
            self.map_widget.delete(self.marker)
        self.marker = self.map_widget.set_marker(self.lat, self.lon, text="Selected Location")

    def browse_file(self):
        start_date = self.date_entry.get()
        try:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            default_filename = f"weather_report_{start_date_dt.strftime('%Y%m%d')}"
        except ValueError:
            default_filename = "weather_report"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_filename,
            title="Save Weather Report As"
        )
        if filename:
            self.output_filename = filename
            self.filename_label.config(text=f"Selected: {filename}")
        else:
            self.output_filename = None
            self.filename_label.config(text="No file selected")

    def generate_report(self):
        start_date = self.date_entry.get()
        town_name = self.town_entry.get().strip()
        if not self.lat or not self.lon:
            self.status.config(text="Please select a location on the map.", foreground="red")
            return
        if not self.output_filename:
            self.status.config(text="Please select an output file.", foreground="red")
            return
        
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            self.status.config(text="Generating report...", foreground="blue")
            self.root.update()
            filename = generate_report(self.lat, self.lon, start_date, self.output_filename, town_name)
            if filename:
                self.status.config(text=f"Report generated: {filename}", foreground="green")
            else:
                self.status.config(text="Failed to fetch data.", foreground="red")
        except ValueError:
            self.status.config(text="Invalid date format. Use YYYY-MM-DD.", foreground="red")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}", foreground="red")

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = WeatherApp(root)
    root.mainloop()