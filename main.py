class Subject:
    def __init__(self):
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self.temperature, self.humidity, self.pressure)


class Observer:
    def update(self, temperature, humidity, pressure):
        raise NotImplementedError("Subclasses must implement update method")


class WeatherData(Subject):
    def __init__(self):
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self.temperature, self.humidity, self.pressure)

    def measurementsChanged(self):
        self.notifyObservers()

    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.measurementsChanged()


class CurrentConditionsDisplay(Observer):
    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.weatherData = weatherData
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()

    def display(self):
        print("Current conditions:", self.temperature,
              "F degrees and", self.humidity, "[%] humidity",
              "and pressure", self.pressure)


class StatisticsDisplay(Observer):
    def __init__(self, weatherData):
        self.temperature_list = []
        self.humidity_list = []
        self.pressure_list = []
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.temperature_list.append(temperature)
        self.humidity_list.append(humidity)
        self.pressure_list.append(pressure)
        self.display()

    def display(self):
        min_temp = min(self.temperature_list)
        max_temp = max(self.temperature_list)
        avg_temp = sum(self.temperature_list) / len(self.temperature_list)

        min_humidity = min(self.humidity_list)
        max_humidity = max(self.humidity_list)
        avg_humidity = sum(self.humidity_list) / len(self.humidity_list)

        min_pressure = min(self.pressure_list)
        max_pressure = max(self.pressure_list)
        avg_pressure = sum(self.pressure_list) / len(self.pressure_list)

        print("Statistics:")
        print("Temperature - Min:", min_temp, "Max:", max_temp, "Average:", avg_temp)
        print("Humidity - Min:", min_humidity, "Max:", max_humidity, "Average:", avg_humidity)
        print("Pressure - Min:", min_pressure, "Max:", max_pressure, "Average:", avg_pressure)


class ForecastDisplay(Observer):
    def __init__(self, weatherData):
        self.forecast_temperature = 0
        self.forecast_humidity = 0
        self.forecast_pressure = 0
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.forecast_temperature = temperature + 0.11 * humidity + 0.2 * pressure
        self.forecast_humidity = humidity - 0.9 * humidity
        self.forecast_pressure = pressure + 0.1 * temperature - 0.21 * pressure
        self.display()

    def display(self):
        print("Forecast:")
        print("Temperature:", self.forecast_temperature)
        print("Humidity:", self.forecast_humidity)
        print("Pressure:", self.forecast_pressure)


class WeatherStation:
    def main(self):
        weather_data = WeatherData()
        current_display = CurrentConditionsDisplay(weather_data)
        statistics_display = StatisticsDisplay(weather_data)
        forecast_display = ForecastDisplay(weather_data)

        weather_data.setMeasurements(80, 65, 30.4)
        weather_data.setMeasurements(82, 70, 29.2)
        weather_data.setMeasurements(78, 90, 29.2)

        weather_data.removeObserver(current_display)
        weather_data.setMeasurements(120, 100, 1000)


if __name__ == "__main__":
    w = WeatherStation()
    w.main()