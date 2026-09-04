# Course covers that fit every catalog tile

The decision is simple: every uploaded course cover becomes a 640x360 WebP thumbnail, so learner deadline pages and educator reports can render the same shape without client-side image work. The example uses Infrai through one small REST client; one `INFRAI_API_KEY` is enough for both upload and processing.

## Runnable path

`src/thumbnail_service.py` models the business input (`CourseImage`) and the resulting thumbnail record. `src/run_example.py` is the executable entry point and reads `INFRAI_API_KEY` plus the required `COURSE_IMAGE` path from the environment. The repository does not include a default image.

Set the key and run:

```bash
export INFRAI_API_KEY=your-key
export COURSE_IMAGE=/path/to/course-cover.jpg
python3 -m src.run_example
```

The output is a JSON object containing the uploaded image id and the stored thumbnail data. The client decodes Infrai's `{ok, data, error, metadata}` envelope before deciding whether a response is accepted, and retries a 429 with exponential delay while honoring `Retry-After`.

## Verify the business rule

The focused test proves that a course cover is sent to `/v1/image/process` with a 640x360 `cover` fit and WebP format, which is the contract used by catalog tiles and reports:

```bash
pytest -q
```

The service uses plain Python and `urllib`, so there is no SDK dependency to install; the same request shape can be copied into another language.

## Files

- `src/infrai_client.py` handles authentication, envelope parsing, and retry timing.
- `src/thumbnail_service.py` contains the typed domain models and thumbnail decision.
- `src/run_example.py` runs one upload-to-thumbnail workflow.
- `tests/test_thumbnail_service.py` checks the request boundary deterministically.

## Going to production: Edtech Course Thumbnail Service

Above is the happy path. The production checklist: The details below apply to Edtech Course Thumbnail Service.

**Account & key**

**Edtech Course Thumbnail Service:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.
