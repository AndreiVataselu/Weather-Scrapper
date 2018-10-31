from selenium import webdriver
import re
import matplotlib.pyplot as plt
import datetime
import mplcursors

def get_week_date():
    week = []
    for i in range(7):
        week.append(datetime.date.today() + datetime.timedelta(days=i+1))
    return week


def create_plot(temperatures, days=[1, 2, 3, 4, 5, 6, 7]):
    week_dates = get_week_date()
    fig = plt.figure()
    plot = fig.add_subplot(111)
    plot.plot(days, temperatures, marker='o', linestyle='dashed')
    plt.title("Temperatures", fontsize=24)
    plt.ylabel("Celsius Degrees", fontsize=14)
    plt.xlabel("Days", fontsize=14)
    cursor = mplcursors.cursor()
    cursor.connect(
        "add", lambda sel: sel.annotation.set_text("Temp: {0}°C\nDate: {1}".format(
            temperatures[int(sel.target.index)],
            week_dates[int(sel.target.index)].strftime("%d %b"))))

    plt.show()


def main():
    # Getting the user desired county
    county = input("County: ")
    county = county.title().lstrip().rstrip().replace(" ", "-")

    # Scrapping the temperatures
    SCRAP_LINK = "http://vremea.ido.ro/{0}.htm".format(county)

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(options=options)

    browser.get(SCRAP_LINK)

    weather_elements = browser.find_elements_by_class_name("miq")

    arrayOfEl = []
    for element in weather_elements:
        arrayOfEl.append(element.text)

    browser.quit()

    temps = []
    try:
        for i in range(0, 14, 2): # Only 7 days
            temps.append(int(re.search("-?\d{1,2}°C", arrayOfEl[i]).group(0)[:-2]))
        create_plot(temps)
    except IndexError:
        print("Invalid county!")


main()