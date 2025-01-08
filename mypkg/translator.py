import rclpy
from rclpy.node import Node
from person_msgs.srv import Trigger

rclpy.init()
node = Node("translator")

def translate_callback( request, response):
    dictionary = {
        "こんにちわ": "Hello",
        "ありがとう": "thank you",
        "さようなら": "Goodbye",
        "いぬ": "Dog",
        "ねこ": "cat",
    }
    word = request.japanese
    translation = dictionary.get(word, "Unknown")
    response.english = translation
    return response

def main():
    srv = node.create_service(Trigger, 'trigger', translate_callback)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
