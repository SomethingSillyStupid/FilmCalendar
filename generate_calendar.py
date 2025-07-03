# generate_calendar.py
import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta

BASE_URL = "https://vidiotsfoundation.org"
CALENDAR_FILE = "vidiots_calendar.ics"
THEATER_LOCATION = "Vidiots, 4884 Eagle Rock Blvd, Los Angeles, CA"

def scrape_showtimes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    cal = Calendar()

    film_links = soup.select('a[href*="/film/"]')
    for link in film_links:
        film_url = link["href"]
        if not film_url.startswith("http"):
            film_url = BASE_URL + film_url

        film_title = link.get_text(strip=True)
        try:
            film_page = requests.get(film_url)
            film_soup = BeautifulSoup(film_page.content, "html.parser")

            # Update selector based on actual site structure
            for st in film_soup.select('a[data-showtime]'):
                dt_str = st["data-showtime"]
                showtime = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

                event = Event()
                event.name = film_title
                event.begin = showtime
                event.duration = timedelta(hours=2)
                event.location = THEATER_LOCATION
                event.description = f"More info: {film_url}"
                cal.events.add(event)
        except Exception as e:
            print(f"Error processing {film_title}: {e}")

    with open(CALENDAR_FILE, "w") as f:
        f.writelines(cal)

if __name__ == "__main__":
    scrape_showtimes()
