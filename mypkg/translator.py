import rclpy
from rclpy.node import Node
from person_msgs.srv import Trigger

class Translator(Node):
    def __init__(self):
        super().__init__("translator")
        self.srv = self.create_service(Trigger, 'trigger', self.translate_callback)
        self.get_logger().info("Translator service is ready.")

    def translate_callback(self, request, response):
        dictionary = {
            "こんにちは": "Hello",
            "ありがとう": "thank you",
            "さようなら": "Goodbye",
            "いぬ": "Dog",
            "ねこ": "Cat",
        }
        word = request.input
        translation = dictionary.get(word, "Unknown")
        response.output = translation
        return response

def main():
    rclpy.init()
    translator_node = Translator()
    
    try:
        rclpy.spin(translator_node)
    except KeyboardInterrupt:
        pass
    finally:
        translator_node.destroy_node()
        rclpy.shutdown()
