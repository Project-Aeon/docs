---
layout: default
title: Main Video API
nav_order: 3
description: "Complete reference for Aeon's video creation API"
---

# Main Video API
{: .no_toc }

Convert web content into engaging videos using configurable presets
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Base URL

```
https://app.project-aeon.com/api/1.1/wf/
```

## Authentication

All endpoints require:
- **Header:** `Authorization: Bearer YOUR_API_TOKEN`
- **Header:** `Content-Type: application/json`
- **Body:** `user_key` parameter

---

## List Presets

Returns preset IDs you can use with **Create Video**.

| Method | Path |
|--------|------|
| `POST` | `/ae_get_presets` |

**Required body fields:**

| Field | Type | Description |
|-------|------|-------------|
| `user_key` | string | Your user key |
| `built_in` | boolean | Return built-in presets (typically `true`) |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_key": "YOUR_USER_KEY",
    "built_in": true
  }'
```

<details><summary>Sample response</summary>

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

## List Supported Languages

Returns valid language codes for the optional `language` parameter in **Create Video**.

| Method | Path |
|--------|------|
| `POST` | `/ae_list_languages` |

**Required body fields:**

| Field | Type | Description |
|-------|------|-------------|
| `user_key` | string | Your user key |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_list_languages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_key": "YOUR_USER_KEY"
  }'
```

<details><summary>Sample response</summary>

```json
{
  "status": "success",
  "response": {
    "languages": [
      { "code": "en-US", "name": "English (US)" },
      { "code": "es-ES", "name": "Spanish (Spain)" }
    ]
  }
}
```
</details>

---

## Clone a Preset

Creates a new, editable preset based on an existing built-in or custom preset. This allows you to customize styling, transitions, and other video elements derived from a base template.

{: .text-red-200 }
> **Note:** Cloning takes ~1 minute, so please setup a callback URL to receive the response.  
> This is only needed to adapt a preset to a new brand—not required for every video.

| Method | Path |
|--------|------|
| `POST` | `/ae_clone_new_preset` |

**Required body fields:**

| Field | Type | Description |
|-------|------|-------------|
| `user_key` | string | Your user key |
| `clone_from_preset_id` | string | ID of the preset to clone (from **List Presets**) |
| `source_url` | string | Web page URL used to initialize the clone |
| `callback_url` | string *(optional)* | POSTed when cloning finishes (takes ~1 minute) |
| `team_id` | string *(optional)* | ID of the team to associate the cloned preset with |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_clone_new_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_key": "YOUR_USER_KEY",
    "clone_from_preset_id": "1745530741190x383445637",
    "source_url": "https://example.com/article-for-cloning",
    "callback_url": "https://yourserver.com/aeon-webhook",
    "team_id": "YOUR_TEAM_ID"
  }'
```

<details><summary>Sample response</summary>

```json
{
  "status": "success",
  "response": {
    "preset_video_id": "NEW_PRESET_ID"
  }
}
```
</details>

---

## Create a Video from a Preset

Create a video from either a web article or pre-processed images.

| Method | Path |
|--------|------|
| `POST` | `/ae_new_video_from_preset` |

**Required body fields:**

| Field | Type | Description |
|-------|------|-------------|
| `preset_video_id` | string | ID from **List Presets** or **Clone Preset** |
| `video_name` | string | Any human‑readable title |
| `user_key` | string | Your user key |
| `source_url` | string *(optional)* | Web page to convert (not required if using `save_state`) |
| `save_state` | string *(optional)* | Saved state blob from AIGC Preview API (looks like `aigc_saved_state_xxx.json`) |

**Optional parameters:**

| Field | Type | Description |
|-------|------|-------------|
| `callback_url` | string | POSTed when rendering finishes |
| `captions` | boolean | Generate captions (default: `true`) |
| `voice` | boolean | Include voiceover (default: `false`) |
| `language` | string | Language code (e.g., `en-US`). See [List Supported Languages](#list-supported-languages) |
| `soundtrack` | boolean | Include background music (default: `true`) |

### Example: Video from Web Article

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637",
    "video_name": "Aeon Demo — April 2025",
    "source_url": "https://example.com/article",
    "user_key": "YOUR_USER_KEY",
    "callback_url": "https://yourserver.com/aeon-webhook",
    "captions": true,
    "voice": true,
    "language": "en-US",
    "soundtrack": true
  }'
```

### Example: Video from Processed Images

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637",
    "video_name": "My Image Video",
    "user_key": "YOUR_USER_KEY",
    "callback_url": "https://yourserver.com/aeon-webhook",
    "save_state": "aigc_saved_state_xxxx.json",
    "voice": false,
    "captions": false
  }'
```

**Successful response:**

```json
{
  "status": "success",
  "response": {
    "video_id": "VIDEO_ID",
    "expires": 31536000
  }
}
```

> **Best practice:** Always provide a `callback_url`. Rendering can take several minutes; polling every few seconds is unnecessary.
{: .text-grey-dk-000 .bg-grey-lt-000}

---

## Poll Video Status

Check rendering progress or fetch the final video URL.

| Method | Path |
|--------|------|
| `POST` | `/ae_get_video` |

**Required body fields:**

| Field | Type | Description |
|-------|------|-------------|
| `video_id` | string | ID returned from **Create Video** |
| `user_key` | string | Your user key |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_video" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "VIDEO_ID",
    "user_key": "YOUR_USER_KEY"
  }'
```

**Completed response:**

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

## Complete Workflow Examples

### Article → Video

```bash
# 1. Get available presets
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_key": "YOUR_USER_KEY", "built_in": true}'

# 2. Create video from article
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637",
    "video_name": "Article Video",
    "source_url": "https://example.com/article",
    "user_key": "YOUR_USER_KEY",
    "callback_url": "https://yourserver.com/webhook"
  }'

# 3. Poll for completion (if no webhook)
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_video" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "RETURNED_VIDEO_ID", "user_key": "YOUR_USER_KEY"}'
```

### Images → Video (with AIGC)

```bash
# 1. Process images via AIGC API
curl -X POST "https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls" \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/image1.jpg"],
    "location_prompt": "in a modern office"
  }'

# 2. Use saved_state_blob from AIGC response
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637", 
    "video_name": "Image Slideshow",
    "user_key": "YOUR_USER_KEY",
    "save_state": "aigc_saved_state_xyz.json"
  }'
```

---

## Next Steps

<div class="code-example" markdown="1">

**Explore More:**
- [AIGC Preview API →](/aigc-api/) - Process images with AI
- [Error Handling →](/errors/) - Handle errors and webhooks
- [Getting Started →](/getting-started/) - Basic setup guide

</div> 