from src.thumbnail_service import CourseImage, make_thumbnail


class FakeClient:
    def __init__(self):
        self.calls = []

    def post(self, path, payload):
        self.calls.append((path, payload))
        if path.endswith("upload"):
            return {"ok": True, "data": {"id": "img_course_1"}}
        return {"ok": True, "data": {"url": "https://cdn.example/thumb.webp", "width": 640, "height": 360}}


def test_course_cover_is_cropped_to_16_9_webp():
    client = FakeClient()
    result = make_thumbnail(CourseImage("bytes", "cover.png"), client)
    assert result.thumbnail["width"] == 640
    assert client.calls[1] == ("/v1/image/process", {"image": "img_course_1", "ops": [{"op": "resize", "width": 640, "height": 360, "fit": "cover", "enlarge": False}], "format": "webp", "store": True})
