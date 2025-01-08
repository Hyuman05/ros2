import rclpy
from rclpy.node import Node
from person_msgs.srv import Query  # サービスメッセージをインポート

def translate_callback(request, response):
    dictionary = {
        "ねこ": "cat",
        "いぬ": "dog",
        "こんにちは": "hello",
        "ありがとう": "thank you",
        "さようなら": "goodbye"
    }
    
    word = request.japanese  # クライアントからの日本語入力
    translation = dictionary.get(word, "Unknown")  # 辞書にない場合"Unknown"を返す
    response.english = translation  # 翻訳結果をレスポンスのenglishフィールドに設定
    return response

def main(args=None):
    rclpy.init(args=args)
    node = Node("Translator")  # 直接Nodeをインスタンス化してノード名を"Translator"に設定
    
    # サービスの作成
    service = node.create_service(Query, 'query', translate_callback)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
