from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .infrai_client import InfraiClient


@dataclass(frozen=True)
class CourseImage:
    file: str
    filename: str
    width: int = 640
    height: int = 360


@dataclass(frozen=True)
class ThumbnailResult:
    image_id: str
    thumbnail: dict[str, Any]


def make_thumbnail(image: CourseImage, client: InfraiClient) -> ThumbnailResult:
    uploaded = client.post("/v1/image/upload", {"file": image.file, "filename": image.filename})
    source = uploaded["data"]
    image_id = source.get("id") or source.get("image")
    if not image_id:
        raise ValueError("upload response did not include an image id")
    processed = client.post(
        "/v1/image/process",
        {
            "image": image_id,
            "ops": [{"op": "resize", "width": image.width, "height": image.height, "fit": "cover", "enlarge": False}],
            "format": "webp",
            "store": True,
        },
    )
    return ThumbnailResult(image_id=image_id, thumbnail=processed["data"])
