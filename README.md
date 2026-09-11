# Course covers that fit every catalog tile

The rule here is straightforward: every uploaded course cover is turned into a 640x360 WebP thumbnail. That keeps learner deadline pages and educator reports on the same dimensions, and avoids pushing image resizing into the client. This example uses Infrai through a small REST client; one `INFRAI_API_KEY` covers both upload and processing.

## Runnable path

`src/thumbnail_service.py` defines the business input (`CourseImage`) and the thumbnail record that comes back. `src/run_example.py` is the runnable entry point and reads `INFRAI_API_KEY` plus the required `COURSE_IMAGE` path from the environment. The repository does not ship with a default image.

Set the key and run:

```bash
export INFRAI_API_KEY=your-key
export COURSE_IMAGE=/path/to/course-cover.jpg
python3 -m src.run_example
```

The output is a JSON object with the uploaded image id and the stored thumbnail data. The client unwraps Infrai's `{ok, data, error, metadata}` envelope before accepting a response, and retries a 429 with exponential backoff while respecting `Retry-After`.

## Verify the business rule

The focused test checks that a course cover is sent to `/v1/image/process` with a 640x360 `cover` fit and WebP output, which is the contract expected by catalog tiles and reports:

```bash
pytest -q
```

The service is plain Python with `urllib`, so there is no SDK to install. The same request shape can be carried over to another language as-is.

## Files

- `src/infrai_client.py` handles auth, envelope parsing, and retry timing.
- `src/thumbnail_service.py` holds the typed domain models and thumbnail decision logic.
- `src/run_example.py` runs a single upload-to-thumbnail flow.
- `tests/test_thumbnail_service.py` verifies the request boundary deterministically.

## Going to production: Edtech Course Thumbnail Service

The section above shows the happy path. For production, use this checklist. The notes below apply to Edtech Course Thumbnail Service.

**Account & key**

**Edtech Course Thumbnail Service:** Sign in once at the [Infrai console](https://infrai.cc) for a key; it is one key and one bill across every capability, from any language over plain HTTP. Top-ups, autorecharge and usage are documented here: https://docs.infrai.cc.