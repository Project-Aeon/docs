# Aeon API Documentation (v0.1 BETA)

> **Status:** Public beta – endpoints and payloads may change.

The Aeon API lets you convert written web content into engaging video using configurable *presets*.  
Use these endpoints to list available presets, create a video, and poll for its completion.

---

## Base URL

```
https://app.project-aeon.com/api/1.1/wf/
```

All examples assume production.  
For testing, replace the domain with `app.project-aeon.com/version-test`.

---

## Authentication & Security

| Header | Example value | Notes |
|--------|---------------|-------|
| `Authorization` | `Bearer YOUR_API_TOKEN` | Obtain from your Aeon dashboard *(never commit real tokens to Git)* |
| `Content-Type` | `application/json` | All requests and responses use JSON |

You’ll **also** pass a **`user_key`** in most request bodies.  
The user key identifies your account and determines which presets and videos you can access.

> **Tip:** Store both the API token and user key in your CI/CD secret manager—*never* in source control.

---

## Quick Start

1. [Generate a user key](#generate-a-user-key)  
2. [List built‑in presets](#list-presets)  
3. [Create a video](#create-a-video-from-a-preset)  
4. [Poll for completion](#poll-video-status)  

---

## Generate a User Key

User keys don’t expire, but they become invalid if you change your email or password.

| Step | Description |
|------|-------------|
| 1 | Log in to your Aeon dashboard |
| 2 | Click **Profile → API** |
| 3 | Click **Generate user key** and copy the value |

---

## Endpoints

### List Presets

Returns preset IDs you can use with **Create Video**.

| Method | Path |
|--------|------|
| `POST` | `/ae_get_presets` |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets"   -H "Authorization: Bearer YOUR_API_TOKEN"   -H "Content-Type: application/json"   -d '{
        "user_key": "YOUR_USER_KEY",
        "built_in": true
      }'
```

<details><summary>Sample response</summary>

```json
{
  "status": "success",
  "response": {
    "ids": [
      {
        "_id": "1745530741190x383445637",
        "Preset Name": "Make a video from a webpage",
        "Name": "Convert an article to a video",
        "Created Date": 1745530741190,
        "Modified Date": 1745531504088
      }
    ]
  }
}
```
</details>

---

### Create a Video from a Preset

| Method | Path |
|--------|------|
| `POST` | `/ae_new_video_from_preset` |

Required body fields:

| Field | Type | Description |
|-------|------|-------------|
| `preset_video_id` | string | ID from **List Presets** |
| `video_name` | string | Any human‑readable title |
| `source_url` | string | Web page to convert |
| `user_key` | string | Your user key |
| `callback_url` | string *(optional)* | POSTed when rendering finishes |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset"   -H "Authorization: Bearer YOUR_API_TOKEN"   -H "Content-Type: application/json"   -d '{
        "preset_video_id": "PRESET_ID",
        "video_name": "Aeon Demo — April 2025",
        "source_url": "https://example.com/article",
        "user_key": "YOUR_USER_KEY",
        "callback_url": "https://yourserver.com/aeon-webhook"
      }'
```

Successful response (truncated):

```json
{
  "status": "success",
  "response": {
    "video_id": "VIDEO_ID",
    "expires": 31536000  // seconds
  }
}
```

> **Best practice:** Provide a `callback_url`. Rendering can take several minutes; polling every few seconds is unnecessary.

---

### Poll Video Status

Check rendering progress or fetch the final video URL.

| Method | Path |
|--------|------|
| `POST` | `/ae_get_video` |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_video"   -H "Authorization: Bearer YOUR_API_TOKEN"   -H "Content-Type: application/json"   -d '{
        "video_id": "VIDEO_ID",
        "user_key": "YOUR_USER_KEY"
      }'
```

**Completed response**

```json
{
  "status": "success",
  "response": {
    "video_id": "VIDEO_ID",
    "status": "Completed",
    "video_url": "https://storage.googleapis.com/aeon-ptv-bucket/your-video.mp4"
  }
}
```

---

## Errors

| HTTP Code | Meaning | Most common causes |
|-----------|---------|--------------------|
| **400** | Bad Request | Missing or malformed JSON |
| **401** | Unauthorized | Invalid API token |
| **403** | Forbidden | Wrong `user_key` for resource |
| **404** | Not Found | Invalid preset or video ID |
| **500** | Server error | Retry with exponential back‑off |

---

## Webhooks

If you supply a `callback_url`, Aeon will `POST` the following JSON upon completion:

```json
{
  "video_id": "VIDEO_ID",
  "status": "Completed",
  "video_url": "https://storage.googleapis.com/aeon-ptv-bucket/your-video.mp4"
}
```

Respond with **2XX** to acknowledge delivery.

---

## Changelog

| Date (UTC) | Version | Notes |
|------------|---------|-------|
| 2025‑04‑28 | 0.1 BETA | Initial public release |

---

## License

Documentation © 2025 Aeon. Released under the MIT License.
