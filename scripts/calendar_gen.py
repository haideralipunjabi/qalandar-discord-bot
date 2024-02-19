from constants import BASE_FOLDER, TEMP_FOLDER
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
from datetime import datetime as dt
import pdfkit
import os

options = {
    "page-size": "A4",
    "margin-top": "5mm",
    "margin-right": "5mm",
    "margin-bottom": "5mm",
    "margin-left": "5mm",
    "encoding": "UTF-8",
}


def generate_pdf(month, year):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    env = Environment(
        loader=FileSystemLoader(os.path.join(BASE_FOLDER, "jinja_templates")),
        autoescape=select_autoescape,
    )
    template = env.get_template("calendar.html")
    dates = []
    i = 1
    while True:
        try:
            d = date.fromisoformat(f"{year}-{str(month).zfill(2)}-{str(i).zfill(2)}")
        except ValueError:
            break
        dates.append(
            [
                f"{str(d.day).zfill(2)}/{str(d.month).zfill(2)}/{d.year}",
                days[d.weekday()],
            ]
        )
        i += 1

    div_2_dates = [dates[: len(dates) // 2], dates[len(dates) // 2 :]]
    filepath = os.path.join(TEMP_FOLDER, f"cal_{month}_{year}.pdf")
    pdfkit.from_string(template.render(maincols=div_2_dates), filepath, options=options)
    return filepath
