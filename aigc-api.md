---
layout: default
title: AIGC Preview API
nav_order: 4
description: "Complete reference for Aeon's AI image processing API"
---

# AIGC Preview API
{: .no_toc }

Process images through an AI pipeline with advanced image processing capabilities
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

The AIGC Preview API processes images through an AI pipeline that can handle both URL-based and base64-encoded image inputs. The API generates AI descriptions and performs various image processing tasks.

## Base URL

```
https://aigc-preview-889529529975.us-central1.run.app
```

## Authentication

{: .text-green-200 }
> **No authentication required** for the preview API.

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

---

## Request Format

### Content-Type
```
Content-Type: application/json
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image_urls` | array | optional | Array of image URLs |
| `base64_images` | array | optional | Array of base64 image objects |
| `duration_per_image` | number | optional | Duration per image (default: 3.0) |
| `fps` | number | optional | FPS (default: 30) |
| `resolution_width` | number | optional | Width (default: 1920) |
| `resolution_height` | number | optional | Height (default: 1080) |
| `pipeline_config_file` | string | optional | Config file name |
| `location_prompt` | string | optional | Location context for AI |
| `person_prompt` | string | optional | Description of a person to render in the image |
| `animation_prompt` | string | optional | Description of animation style for final video render |


### Base64 Image Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | string | **required** | Base64 encoded image data |
| `mime_type` | string | optional | MIME type (default: "image/jpeg") |

### Requirements

- At least one of `image_urls` or `base64_images` must be provided
- Maximum 50 images total (URLs + base64 combined)
- Base64 images must have valid `data` field
- Supported image formats: JPEG, PNG, GIF, WebP, AVIF

---

## Input Methods

### 1. URL-Based Images

Process images directly from URLs:

```json
{
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png"
  ],
  "location_prompt": "in a modern office setting",
  "person_prompt": "a professional businesswoman in her 30s wearing a navy blue suit",
  "animation_prompt": "smooth camera movements with professional transitions"
}
```

### 2. Base64-Encoded Images

Process base64 encoded images:

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

Combine both input methods:

```json
{
  "image_urls": ["https://example.com/image1.jpg"],
  "base64_images": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAA...",
      "mime_type": "image/png"
    }
  ],
  "location_prompt": "in a professional photography studio",
  "person_prompt": "a confident photographer in casual clothing with camera equipment",
  "animation_prompt": "dynamic camera angles with creative artistic movements"
}
```

---

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

The `saved_state_blob` can be used with the [Main Video API](/main-api/#create-a-video-from-a-preset) to create videos from processed images.

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Pipeline Configuration Options

### Available Config Files

| Config File | Description |
|-------------|-------------|
| `in-studio_selected-assets_classic.json` | **Default** - Standard image processing |
| `in-studio_selected-assets_360.json` | 360-degree image processing |
| `in-studio_selected-assets_no-face.json` | Processing without face detection |

### Usage

```json
{
  "pipeline_config_file": "in-studio_selected-assets_360.json"
}
```

---

## cURL Examples

### Using Base64 Images

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": [],
    "base64_images": [
      {
        "data": "iVBORw0KGgoAAAANSUhEUgAA...",
        "mime_type": "image/png"
      }
    ],
    "location_prompt": "in a modern office",
    "person_prompt": "a young professional software developer wearing casual attire",
    "animation_prompt": "gentle zoom effects with modern tech-style transitions"
  }'
```

### Using Image URLs

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.png"
    ],
    "duration_per_image": 3.0,
    "fps": 30,
    "animation_prompt": "cinematic fade transitions with slow panning movements"
  }'
```

### Advanced Configuration

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/image.jpg"],
    "duration_per_image": 5.0,
    "fps": 60,
    "resolution_width": 3840,
    "resolution_height": 2160,
    "pipeline_config_file": "in-studio_selected-assets_360.json",
    "location_prompt": "in a high-tech laboratory setting",
    "person_prompt": "a skilled scientist in a white lab coat conducting experiments",
    "animation_prompt": "360-degree rotating views with scientific precision movements"
  }'
```

---

## Image Processing Limits

| Limit | Value |
|-------|-------|
| **Maximum images per request** | 50 images |
| **Processing timeout** | 180 seconds |
| **Supported formats** | JPEG, PNG, GIF, WebP, AVIF |
| **File cleanup** | Base64 images automatically cleaned up |

---

## Error Handling

### Common Error Codes

| HTTP Code | Description |
|-----------|-------------|
| `400 Bad Request` | Invalid input (no images, too many images, invalid base64) |
| `500 Internal Server Error` | Pipeline processing failure |

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

## Integration with Video API

The AIGC API works seamlessly with the [Main Video API](/main-api/). Here's the complete workflow:

```bash
# 1. Process images through AIGC API
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "location_prompt": "in a modern workspace",
    "person_prompt": "a creative designer working on innovative projects",
    "animation_prompt": "smooth creative transitions with inspiring movements"
  }'

# Response will include saved_state_blob: "aigc_saved_state_xyz.json"

# 2. Create video using the saved state
curl -X POST https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637",
    "video_name": "My Image Video",
    "user_key": "YOUR_USER_KEY",
    "save_state": "aigc_saved_state_xyz.json"
  }'
```

---

## Next Steps

<div class="code-example" markdown="1">

**Explore More:**
- [Main Video API →](/main-api/) - Create videos from processed images
- [Getting Started →](/getting-started/) - Basic setup guide
- [Error Reference →](/errors/) - Handle errors and troubleshooting

</div> 