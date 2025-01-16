import rclpy
from rclpy.node import Node
from person_msgs.srv import Trigger 

class Questioner(Node):
    def __init__(self):
        super().__init__("questioner")
        self.client = self.create_client(Trigger, "trigger")
        self.get_logger().info('サービスクライアントが作成されました')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("待機中")
        self.words = ["こんにちは", "ありがとう", "さようなら", "いぬ", "ねこ", "dog"]
        self.request_count = 0
        self.send_next_request()
    def send_next_request(self):
        if self.request_count < len(self.words):
            word = self.words[self.request_count]
            self.send_request(word)
            self.request_count += 1
        else:
            self.get_logger().info("全てのリクエストが完了。終了します。")

    def send_request(self, word):
        self.request = Trigger.Request()
        self.request.input = word
        self.future = self.client.call_async(self.request)
        self.future.add_done_callback(lambda future: self.callback(future, word))

    def callback(self, future, word):
        try:
            response = future.result()
            self.get_logger().info(f'intput: "{word}", output: "{response.output}"')
        except Exception as e:
            self.get_logger().error(f'サービス呼び出しに失敗しました: {e}')
        self.send_next_request()
def main():
    rclpy.init()
    questioner_node = Questioner()

    try:
        rclpy.spin(questioner_node)
    except KeyboardInterrupt:
        pass
    finally:
         questioner_node.destroy_node()
         rclpy.shutdown()
