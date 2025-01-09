import rclpy
from rclpy.node import Node
from person_msgs.srv import Trigger 


rclpy.init()
node = Node("questioner")

def send_translation_request(client, japanese_word):
    request = Trigger.Request()
    request.japanese = japanese_word

    future = client.call_async(request)



    def translation_response_callback(future):
        try:
                response = future.result()
                node.get_logger().info(f'日本語: "{request.japanese}", 英語: "{response.english}"')
        except Exception as e:
                node.get_logger().error(f'サービス呼び出しに失敗しました: {e}')
        finally:
                rclpy.shutdown()

    future.add_done_callback(translation_response_callback)

def main():
    client = node.create_client(Trigger, 'trigger')
    node.get_logger().info('サービスクライアントが作成されました')

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('待機中...')

    send_translation_request(client, "こんにちわ")

    rclpy.spin(node)
