import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
from bs4 import BeautifulSoup

class WeatherNode(Node):
    def __init__(self):
        super().__init__('weather_node')
        self.publisher = self.create_publisher(String, 'weather_topic', 10)
        self.timer = self.create_timer(60, self.get_weather)
        self.prefectures = {
            '北海道': 'Sapporo',
            '青森県': 'Aomori',
            '岩手県': 'Morioka',
            '宮城県': 'Sendai',
            '秋田県': 'Akita',
            '山形県': 'Yamagata',
            '福島県': 'Fukushima',
            '東京都': 'Tokyo',
            '神奈川県': 'Yokohama',
            '埼玉県': 'Saitama',
            '千葉県': 'Chiba',
            '茨城県': 'Mito',
            '栃木県': 'Utsunomiya',
            '群馬県': 'Maebashi',
            '山梨県': 'Kofu',
            '新潟県': 'Niigata',
            '富山県': 'Toyama',
            '石川県': 'Kanazawa',
            '福井県': 'Fukui',
            '長野県': 'Nagano',
            '岐阜県': 'Gifu',
            '静岡県': 'Shizuoka',
            '愛知県': 'Nagoya',
            '三重県': 'Tsu',
            '滋賀県': 'Otsu',
            '京都府': 'Kyoto',
            '大阪府': 'Osaka',
            '兵庫県': 'Kobe',
            '奈良県': 'Nara',
            '和歌山県': 'Wakayama',
            '鳥取県': 'Tottori',
            '島根県': 'Matsue',
            '岡山県': 'Okayama',
            '広島県': 'Hiroshima',
            '山口県': 'Yamaguchi',
            '徳島県': 'Tokushima',
            '香川県': 'Takamatsu',
            '愛媛県': 'Matsuyama',
            '高知県': 'Kochi',
            '福岡県': 'Fukuoka',
            '佐賀県': 'Saga',
            '長崎県': 'Nagasaki',
            '熊本県': 'Kumamoto',
            '大分県': 'Oita',
            '宮崎県': 'Miyazaki',
            '鹿児島県': 'Kagoshima',
            '沖縄県': 'Naha'
        }

    def get_weather(self):
        self.get_logger().info('天気情報の取得を開始')
        for prefecture, city in self.prefectures.items():
            self.get_logger().info(f'{prefecture} ({city})の天気を取得中')


            url = "https://www.data.jma.go.jp/stats/data/mdrr/synopday/data1s.html"
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, "html.parser")
            elems = soup.find_all("tr")


            weather_html = str(elems[58].contents[5])
            temp_html = str(elems[58].contents[7])
            pref_html = str(elems[58].contents[0])


            weather_data = weather_html[:weather_html.find("</td>")]
            weather_data = weather_data[weather_data.find(">") + 1:]
            temp_data = temp_html[:temp_html.find("</td>")]
            temp_data = temp_data[temp_data.find(">") + 1:]
            pref = pref_html[:pref_html.find("</td>")]
            pref = pref[pref_html.find(">") + 1:]


            weather_data = weather_data.replace(']', '').replace(')', '').replace('#', '').replace('*', '').replace('@', '')
            temp_data = temp_data.replace(']', '').replace(')', '').replace('#', '').replace('*','').replace('@', '')


            weather_message = f'{pref}の天気: {weather_data}, 気温: {temp_data}°C'


            self.publish_weather(weather_message)

    def publish_weather(self, message: str):
         msg = String()
         msg.data = message
         self.publisher.publish(msg)
         self.get_logger().info(f"Published weather massage: {message}")

def main():
    rclpy.init()
    weather_node = WeatherNode()
    rclpy.spin(weather_node)
    weather_node.destroy_node()
    rclpy.shutdown()
