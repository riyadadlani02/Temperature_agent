
from uagents import Agent, Context
import requests
from notification import push_notification
temperature_agent = Agent(
    name="current_Temp", seed="current_Temp recovery phrase")

API_KEY = "cada7a48cf6323e1235c4237baa81743"

config = {
    "min": 0,
    "max": 0,
    "location": "jaipur",
    "mobileNumber": "8169069127",
    "emailId": "sarfarajansaridev@gmail.com",
    "name": ""
}


def setData():
    config["location"] = input("Location : ")
    config["min"] = float(input("Min temperature in celcius : "))
    config["max"] = float(input("Max temperature in celcius : "))
    config["name"] = input("Name : ")
    config["mobileNumber"] = input("Mobile Number : ")
    config["emailId"] = input("Email Id : ")


@temperature_agent.on_interval(period=1800)
async def fetch_temperature(ctx: Context):
    location = config["location"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"] - 273.15

        ctx.storage.set("temperature", temperature)

        ctx.logger.info(
            f'Current temperature in {location} is {temperature}')
    else:
        ctx.logger.error(f'Error fetching temperature for {location}')


@temperature_agent.on_interval(period=1800)
async def send_notification(ctx: Context):

    current = ctx.storage.get("temperature")
    min = config["min"]
    max = config["max"]

    if current > min and current < max:
        ctx.logger.info("Temperature is in range")
        return

    name = config["name"]
    email = config["emailId"]
    mobile_number = config["mobileNumber"]
    location = config["location"]
    if current > max:
        body = f"""Hi {name}
        , The current temperature of {location} has gone above the maximum threshold.
        Current temperature : {current}
        Threshold : {max}"""
        push_notification(body, mobile_number, email)

    if current < min:
        body = f"""Hi {name}
, The current temperature of {location} has gone below the minimum threshold.
Current temperature : {current}
Threshold : {min}"""
        push_notification(body, mobile_number, email)

    # send notification
    ctx.logger.info(
        f'Temperature out of range, send notification . current temperature : {current}')


if __name__ == "__main__":
    setData()
    temperature_agent.run()
