# Send to single device.
from pyfcm import FCMNotification
import sys

push_service = FCMNotification(api_key="AAAARbB5Gyg:APA91bFXFAcqgEa7otXJ2q0yuNlz2VUV1vSd7CPMxcB5kTXq0zuT6i5jhSOxT5tBISGnzl9lB-M8GRWvyt8026rwBhJDYn3jxO4tGs-rNp1VwHeKQxCQdX0lrf4e9H5sw7IkNsUOmpaF")


if __name__ == "__main__":
    registration_id = sys.argv[3] or "dwG4YE4dPdA:APA91bHjBU9tCweL2OYhoH1lYcd1A9rP3mUEOrRmqBbCtssF18RlA54tZQGIuC3ZmDqaB6vnJfG2yb_vd6dHc4KqhmF9Lx9En9TePediaLeOBj4URJb22Z9y-U12_w4-FbxvzvX7IgF0"
    message_title = sys.argv[1] or "Uber update"
    message_body = sys.argv[2] or "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, sound='Default')
    print(result)