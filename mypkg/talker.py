import rclpy
from rclpy.node import Node
from person_msgs.srv import Query

rclpy.init()
node = Node("talker")


def cb(request, response):
    if request.name == "上田隆一":
        response.age = 46
    else:
        response.age = 255

    return response


def main():
    node.create_service(Query, "query", cb)
    rclpy.spin(node)
