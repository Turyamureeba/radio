from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
import csv
import math

class RadioApp(App):
    def build(self):
        self.title = 'Offline Radio App'
        layout = BoxLayout(orientation='vertical')
        
        # Load radio station data from CSV
        self.radio_stations = []
        with open('radio_stations.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                self.radio_stations.append(row)

        # Display radio stations in a ScrollView
        scroll_view = ScrollView()
        station_list = BoxLayout(orientation='vertical', size_hint_y=None)
        for station in self.radio_stations:
            station_button = Button(text=station[0], size_hint_y=None, height=44)
            station_button.bind(on_press=self.play_station)
            station_list.add_widget(station_button)
        scroll_view.add_widget(station_list)

        layout.add_widget(Label(text="Available FM Stations"))
        layout.add_widget(scroll_view)
        self.audio_player = None
        return layout

    def play_station(self, instance):
        station_name = instance.text
        for station in self.radio_stations:
            if station[0] == station_name:
                if self.audio_player:
                    self.audio_player.stop()
                self.audio_player = SoundLoader.load('audio/' + station[0] + '.mp3')
                if self.audio_player:
                    self.audio_player.play()

    def get_user_location(self):
        # Implement logic to use Android's Location API or Geolocation API here
        # This will involve requesting user's permission for location access
        # and then retrieving the user's latitude and longitude
        
        # For example, using Google's Geolocation API (requires API key):
        api_key = 'YOUR_GOOGLE_API_KEY'
        url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}'
        response = requests.post(url)
        location_data = response.json()
        user_latitude = location_data['location']['lat']
        user_longitude = location_data['location']['lng']
        
        return user_latitude, user_longitude

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Calculate distance between two coordinates using Haversine formula
        radius = 6371  # Earth's radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c
        return distance

    def search_radio_stations(self):
        user_latitude, user_longitude = self.get_user_location()
        max_distance_km = 10  # Maximum distance to consider stations available

        available_stations = []

        for station in self.radio_stations:
            station_name, company, frequency, station_latitude, station_longitude = station
            station_latitude = float(station_latitude)
            station_longitude = float(station_longitude)

            distance = self.calculate_distance(user_latitude, user_longitude, station_latitude, station_longitude)

            if distance <= max_distance_km:
                available_stations.append(station_name)

        print("Available FM Stations in Vicinity:")
        print(available_stations)

if __name__ == '__main__':
    RadioApp().run()
