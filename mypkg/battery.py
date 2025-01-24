import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import psutil

class BatteryStatusNode(Node):
    def __init__(self):
        super().__init__('battery')
        self.publisher = self.create_publisher(String, 'battery_topic', 10)
        self.timer = self.create_timer(10, self.publish_battery_status)

    def get_battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            return f"Battery is at {percent}% {'(Plugged in)' if plugged else '(Not plugged in)'}"
        else:
            return "Battery information not available."

    def publish_battery_status(self):
        battery_status = self.get_battery_status()
        msg = String()
        msg.data = battery_status
        self.publisher.publish(msg)
        self.get_logger().info(f"Published battery status: {battery_status}")

def main():
    rclpy.init()
    battery_node = BatteryStatusNode()
    rclpy.spin(battery_node)
    battery_node.destroy_node()
    rclpy.shutdown()

