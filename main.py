from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
from utils import scroll_down
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

options = Options()
options.binary_location = r'chrome-win64/chrome.exe'
driver = webdriver.Chrome(options=options)

driver.maximize_window()
driver.get('https://www.redbus.in/online-booking/rtc-directory')

i = 1


def get_all_rtc_operators_with_routes():  # all 25 or 10 of them
    # logic for fetching only operators who have routes in page or else skip that operator
    region_wise_rtc = driver.find_elements(By.XPATH, "//ul[@class='D113_ul_region_rtc']/li/a")
    rtc_list = []
    for j in region_wise_rtc:
        rtc_list.append((j.get_attribute('text'), j.get_attribute('href')))

    # check for validity
    _valid_rtc_list = []
    for rtc in rtc_list:
        driver.get(rtc[1])
        routes = driver.find_elements(By.XPATH, "//div[@class='route_link']")
        if len(routes) > 0:
            _valid_rtc_list.append(rtc)

    return _valid_rtc_list


def get_all_routes_for_operator(_valid_rtc_list):
    # loop through all pages [1,2,3,4,5] of routes and get all routes
    All_routes = {}
    for rtc in _valid_rtc_list:
        driver.get(rtc[1])
        pages = driver.find_elements(By.XPATH, "//div[@class='DC_117_paginationTable']//div")

        temp_routes = []

        # for single pages : they dont have pagination
        if len(pages) == 0:
            routes = driver.find_elements(By.CLASS_NAME, "route_details")
            for route in routes:
                route = route.find_element(By.CSS_SELECTOR, "a.route")
                route_name = route.get_attribute('text')
                route_link = route.get_attribute('href')
                temp_routes.append((route_name, route_link))
            All_routes[rtc[0]] = temp_routes
            continue

        for page in pages:
            # element = WebDriverWait(page, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[3]")))
            driver.execute_script("arguments[0].click()", page)

            # get routes
            routes = driver.find_elements(By.CLASS_NAME, "route_details")
            for route in routes:
                route = route.find_element(By.CSS_SELECTOR, "a.route")
                route_name = route.get_attribute('text')
                route_link = route.get_attribute('href')
                temp_routes.append((route_name, route_link))

        All_routes[rtc[0]] = temp_routes

    return All_routes


def get_buses_route_wise(_route, bus_operator_id):
    global i
    # logic for fetching private and govt buses which are in same page
    driver.get(_route[1])

    # expand all govt bus cards and go till end of page until all content loads
    # state_bus_groups = driver.find_elements(By.CSS_SELECTOR, "div.button")
    time.sleep(2)
    state_bus_groups = driver.find_elements(By.XPATH, "//div[text() = 'View Buses']")

    for group in state_bus_groups:
        driver.execute_script("arguments[0].click()", group)

    scroll_down(driver)
    time.sleep(3)
    all_buses = driver.find_elements(By.XPATH,
                                     "//ul[@class='bus-items']/div/li/div[@class='clearfix bus-item']/div[@class='clearfix bus-item-details']")

    final_data = {
        "bus_route_name": _route[0],
        "bus_route_link": _route[1],
        "bus_operator_id": bus_operator_id
    }

    df_og = pd.DataFrame()

    for bus in all_buses:

        try:
            final_data["bus_name"] = bus.find_element(By.XPATH,
                                                      ".//div[@class='clearfix row-one']//div[1]//div[1]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["bus_name"] = "None"
        try:
            final_data["bus_type"] = bus.find_element(By.XPATH,
                                                      ".//div[@class='clearfix row-one']//div[1]//div[2]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["bus_type"] = "None"
        try:
            final_data["departing_time"] = bus.find_element(By.XPATH,
                                                            ".//div[@class='clearfix row-one']//div[2]//div[1]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["departing_time"] = "None"
        try:
            final_data["duration"] = bus.find_element(By.XPATH,
                                                      ".//div[@class='clearfix row-one']//div[3]//div[1]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["duration"] = "None"
        try:
            final_data["arrival_time"] = bus.find_element(By.XPATH,
                                                          ".//div[@class='clearfix row-one']//div[4]//div[1]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["arrival_time"] = "None"
        try:
            final_data["star_rating"] = bus.find_element(By.XPATH,
                                                         ".//div[@class='clearfix row-one']//div[5]//div[1]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["star_rating"] = "None"
        try:
            final_data["price"] = bus.find_element(By.XPATH,
                                                   ".//div[@class='clearfix row-one']//div[6]//div[1]//div[@class='fare d-block']//span").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["price"] = "None"
        try:
            final_data["seats_available"] = bus.find_element(By.XPATH,
                                                             ".//div[@class='clearfix row-one']//div[7]").get_attribute(
                "innerText")
        except NoSuchElementException:
            final_data["seats_available"] = "None"

        if final_data["seats_available"] != "None" and final_data["seats_available"] != "":
            final_data["seats_available"] = final_data["seats_available"].split()[0]
        else:
            print(f"error: {final_data['bus_route_name']} {final_data['bus_name']}")

        df = pd.DataFrame(final_data, index=[i])
        i += 1
        df_og = pd.concat([df_og, df])

    return df_og


# get valid  operators List (pickled)

try:
    valid_rtc_list = pickle.load(open("valid_rtc_list.pickle", "rb"))
except (OSError, IOError) as e:
    valid_rtc_list = get_all_rtc_operators_with_routes()
    pickle.dump(valid_rtc_list, open("valid_rtc_list.pickle", "wb"))

# get All routes per valid operator Dict (pickled)

try:
    All_routes_for_all_operators = pickle.load(open("All_routes_for_all_operators.pickle", "rb"))
except (OSError, IOError) as e:
    All_routes_for_all_operators = get_all_routes_for_operator(valid_rtc_list)
    pickle.dump(All_routes_for_all_operators, open("All_routes_for_all_operators.pickle", "wb"))

Final_df = pd.DataFrame()

final_routes = set()

for _operator, _routes in All_routes_for_all_operators.items():
    for route in _routes:
        final_routes.add((route, _operator))

count = len(final_routes)

operator_id = 1
operator_list = {}
c = 0
for rout, operator in final_routes:

    if operator in operator_list:
        pass
    else:
        operator_list[operator] = operator_id
        operator_id += 1

    try:
        temp_df_route = get_buses_route_wise(rout, operator_list[operator])  # yet to be implemented
        Final_df = pd.concat([Final_df, temp_df_route])
    except Exception as e:
        print(rout[1] + "  " + f"error: {str(e)}")
        continue
    c += 1
    print(f"{c}/{count} - done")

# Final_df.to_csv('all_buses_data3.csv')
print("done")

Base = declarative_base()
engine = db.create_engine("sqlite:///red-bus-data.db")


class bus_operator_table(Base):
    __tablename__ = 'red-bus-operators'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    operator_name = db.Column(db.String(100))


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

for op_name, op_id in operator_list.items():
    try:
        temp_op = bus_operator_table(id=op_id, operator_name=op_name.strip())
        session.add(temp_op)
        session.commit()
    except Exception as e:
        session.rollback()
        print(str(e))

session.close()

while True:
    pass
