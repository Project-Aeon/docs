# Aeon API Documentation (v0.1 BETA)

> **Status:** Public beta – endpoints and payloads may change.

The Aeon API lets you convert written web content into engaging video using configurable *presets*.  
Use these endpoints to list available presets, create a video, and poll for its completion.

---

## Base URL

```
https://app.project-aeon.com/api/1.1/wf/
```

---

## Authentication & Security

| Header | Example value | Notes |
|--------|---------------|-------|
| `Authorization` | `Bearer YOUR_API_TOKEN` | Obtain from your Aeon dashboard *(never commit real tokens to Git)* |
| `Content-Type` | `application/json` | All requests and responses use JSON |

You'll **also** pass a **`user_key`** in most request bodies.  
The user key identifies your account and determines which presets and videos you can access.

> **Tip:** Store both the API token and user key in your CI/CD secret manager—*never* in source control.

---

## Quick  Start

1. [Generate a user key](#generate-a-user-key)  
2. [List built‑in presets](#list-presets)  
3. [Make a preset cloning from a built-in preset](#clone-a-preset)
4. [Create a video from the preset](#create-a-video-from-a-preset)  
5. [Poll for completion](#poll-video-status)  

---

## Generate a User Key

User keys don't expire, but they become invalid if you change your email or password.

| Step | Description |
|------|-------------|
| 1 | Log in to your Aeon dashboard |
| 2 | Click **Profile → API** |
| 3 | Click **Generate user key** and copy the value |

---

## Endpoints

### List Presets

Returns preset IDs you can use with **Create Video**.

| Method | Path |
|--------|------|
| `POST` | `/ae_get_presets` |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets"   -H "Authorization: Bearer YOUR_API_TOKEN"   -H "Content-Type: application/json"   -d '{
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

### List Supported Languages

Returns valid language codes for the optional `language` parameter in **Create Video**.

| Method | Path |
|--------|------|
| `POST` | `/ae_list_languages` |

Required body fields:

| Field | Type | Description |
|-------|------|-------------|
| `user_key` | string | Your user key |

```bash
cURL -X POST "https://app.project-aeon.com/api/1.1/wf/ae_list_languages" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "user_key": "YOUR_USER_KEY"
      }'
```

<details><summary>Sample response (Placeholder)</summary>

```json
{
  "status": "success",
  "response": {
    "languages": [
      { "code": "en-US", "name": "English (US)" },
      { "code": "es-ES", "name": "Spanish (Spain)" }
      // ... other languages
    ]
  }
}
```
</details>

---

### Clone a Preset

Creates a new, editable preset based on an existing built-in or custom preset. This allows you to customize styling, transitions, and other video elements derived from a base template.

Note that cloning takes ~1 minute, so please setup a callback URL to receive the response.
Note that this is only needed to adapt a preset to a new brand, this isn't needed for every video.

| Method | Path |
|--------|------|
| `POST` | `/ae_clone_new_preset` |

Required body fields:

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
        "clone_from_preset_id": "EXISTING_PRESET_ID",
        "source_url": "https://example.com/article-for-cloning",
        "callback_url": "https://yourserver.com/aeon-webhook",
        "team_id": "YOUR_TEAM_ID"
      }'
```

<details><summary>Sample response (Placeholder)</summary>

```json
{
  "status": "success",
  "response": {
    "preset_video_id": "NEW_PRESET_ID",
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
| `source_url` | string *(optional)* | Web page to convert (not required if using `save_state`) |
| `user_key` | string | Your user key |
| `callback_url` | string *(optional)* | POSTed when rendering finishes |
| `captions` | boolean *(optional)* | Generate captions (default: `true`) |
| `voice` | boolean *(optional)* | Include voiceover (default: `false`) |
| `language` | string *(optional)* | Language code (e.g., `en-US`). See [List Supported Languages](#list-supported-languages). Default depends on preset. |
| `soundtrack` | boolean *(optional)* | Include background music (default: `true`) |
| `save_state` | string *(optional)* | Saved state blob from AIGC Preview API (looks like `aigc_saved_state_xxx.json`) |

```bash
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset"   -H "Authorization: Bearer YOUR_API_TOKEN"   -H "Content-Type: application/json"   -d '{
        "preset_video_id": "PRESET_ID",
        "video_name": "Aeon Demo — April 2025",
    "preset_video_id": "1751000561548x719904119265165300",
    "callback_url": "https://yourserver.com/aeon-webhook",
        
        // Optional parameters
        "captions": true,
        "voice": true,
        "language": "en-US", // Get valid codes from /ae_list_languages
        "soundtrack": true ,
        "save_state": "aigc_saved_state_xxxx.json"
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

# AIGC Preview API - Image Processing

> **Status:** Preview API for local development and testing

The AIGC Preview API processes images through an AI pipeline that can handle both URL-based and base64-encoded image inputs. The API generates AI descriptions and performs various image processing tasks.

## Base URL

```
https://aigc-preview-889529529975.us-central1.run.app
```

## Authentication

No authentication required for local development API.

---

## Endpoints

### Health Check
```http
GET /health
```

Returns service health status.

### Root Information
```http
GET /
```

Returns API information and available endpoints.

### Process Images (Main Endpoint)
```http
POST /create-slideshow-urls
```

Process images from URLs and/or base64 encoded data through the AI pipeline.

## Request Format

### Content-Type
```
Content-Type: application/json
```

### Request Body

```json
{
  "image_urls": ["string"],           // Optional: Array of image URLs
  "base64_images": [                  // Optional: Array of base64 image objects
    {
      "data": "string",               // Required: Base64 encoded image data
      "mime_type": "string"           // Optional: MIME type (default: "image/jpeg")
    }
  ],
  "duration_per_image": 3.0,          // Optional: Duration per image (default: 3.0)
  "fps": 30,                          // Optional: FPS (default: 30)
  "resolution_width": 1920,           // Optional: Width (default: 1920)
  "resolution_height": 1080,          // Optional: Height (default: 1080)
  "pipeline_config_file": "string",   // Optional: Config file name
  "location_prompt": "string"         // Optional: Location context for AI
}
```

### Requirements

- At least one of `image_urls` or `base64_images` must be provided
- Maximum 50 images total (URLs + base64 combined)
- Base64 images must have valid `data` field
- Supported image formats: JPEG, PNG, GIF, WebP, AVIF

## Input Methods

### 1. URL-Based Images

```json
{
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png"
  ],
  "location_prompt": "in a modern office setting"
}
```

### 2. Base64-Encoded Images

```json
{
  "base64_images": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAA...",
      "mime_type": "image/png"
    },
    {
      "data": "/9j/4AAQSkZJRgABAQAAAQAB...",
      "mime_type": "image/jpeg"
    }
  ]
}
```

### 3. Mixed Input (URLs + Base64)

```json
{
  "image_urls": ["https://example.com/image1.jpg"],
  "base64_images": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAA...",
      "mime_type": "image/png"
    }
  ],
  "location_prompt": "in a professional photography studio"
}
```

## Response Format

### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Images processed successfully from URLs and base64 images!",
  "images_requested": 3,
  "result": {
    "processed_images": [
      "https://storage.googleapis.com/bucket/processed_image1.jpg",
      "https://storage.googleapis.com/bucket/processed_image2.jpg"
    ],
    "saved_state_blob": "aigc_saved_state_uuid.json"
  }
}
```

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Pipeline Configuration Options

### Available Config Files

- `in-studio_selected-assets_classic.json` (default)
- `in-studio_selected-assets_360.json`
- `in-studio_selected-assets_no-face.json`

### Usage

```json
{
  "pipeline_config_file": "in-studio_selected-assets_360.json"
}
```

## cURL Examples

### Using Base64 Images

```bash
curl -X POST http://localhost:8080/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": [],
    "base64_images": [
      {
        "data": "iVBORw0KGgoAAAANSUhEUgAA...",
        "mime_type": "image/png"
      }
    ],
    "location_prompt": "in a modern office"
  }'
```

### Using Image URLs

```bash
curl -X POST http://localhost:8080/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.png"
    ],
    "duration_per_image": 3.0,
    "fps": 30
  }'
```

## Image Processing Limits

- Maximum 50 images per request
- 180-second timeout for processing
- Base64 images are temporarily stored and cleaned up automatically
- Supported formats: JPEG, PNG, GIF, WebP, AVIF

## Common Error Codes

- `400 Bad Request` - Invalid input (no images, too many images, invalid base64)
- `500 Internal Server Error` - Pipeline processing failure

### Common Issues

1. **No images provided**
   ```json
   {"detail": "No image URLs or base64 images provided"}
   ```

2. **Too many images**
   ```json
   {"detail": "Too many images. Maximum 50 images allowed (URLs + base64 combined)"}
   ```

3. **Invalid base64 data**
   - Check that base64 string is valid
   - Ensure proper MIME type is specified

---

## Errors

| HTTP Code | Meaning | Most common causes |
|-----------|---------|--------------------|
| **400** | Bad Request | Missing or malformed JSON |
| **401** | Unauthorized | Invalid API token |
| **403** | Forbidden | Wrong `user_key` for resource |
| **404** | Not Found | Invalid preset or video ID |
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
| 2025‑04‑28 | 0.1 BETA | Initial public release |

---

## License

Documentation © 2025 Aeon. Released under the MIT License.
