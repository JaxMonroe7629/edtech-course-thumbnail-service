from __future__ import annotations

import json
import os

from .infrai_client import InfraiClient
from .thumbnail_service import CourseImage, make_thumbnail


def main() -> None:
    image_path = os.environ.get("COURSE_IMAGE")
    if not image_path:
        raise SystemExit("COURSE_IMAGE must point to an input image")
    image = CourseImage(file=image_path, filename=os.path.basename(image_path))
    result = make_thumbnail(image, InfraiClient())
    print(json.dumps({"image_id": result.image_id, "thumbnail": result.thumbnail}, indent=2))


if __name__ == "__main__":
    main()
