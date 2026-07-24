
import requests


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text} . "
    
    return "Something went wrong"

if __name__ == "__main__":
    city = input("Enter a city: ")
    print(get_weather(city))