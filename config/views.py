import redis
from django.http import StreamingHttpResponse
from django.shortcuts import render


def event_stream():
    redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
    pubsub = redis_client.pubsub()
    pubsub.subscribe("new_orders")

    for message in pubsub.listen():
        if message["type"] == "message":
            yield f"data: {message['data'].decode('utf-8')}\n\n"


def stream_view(request):
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response


def home_view(request):
    return render(request, "index.html")
