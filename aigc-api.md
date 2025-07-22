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

The AIGC Preview API processes images through an AI pipeline that can handle both URL-based and base64-encoded image inputs. The API generates AI descriptions and performs various image processing tasks. It now supports model images as reference images to enhance AI generation quality, particularly useful for full-body generation when original images don't contain full bodies.

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
| `model_urls` | array | optional | Array of model reference image URLs (only first image used) |
| `model_b64` | array | optional | Array of base64 model image objects (only first image used) |
| `pipeline_config_file` | string | optional | Config file name |
| `location_prompt` | string | optional | Location context for AI |
| `person_prompt` | string | optional | Description of a person to render in the image |
| `animation_prompt` | string | optional | Description of animation style for final video render |
| `do_not_alter` | boolean | optional | If true, runs description only and skips AI generation (default: false) |


### Base64 Image Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | string | **required** | Base64 encoded image data |
| `mime_type` | string | optional | MIME type (default: "image/jpeg") |

### Model Image Object

Model images serve as reference images for AI generation, particularly useful for full-body generation when the original images don't contain full bodies. When provided, model images are used as reference points for multi-image flux generation. **Only one model image is supported per request** - if multiple model images are provided, only the first one will be used.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | string | **required** | Base64 encoded model image data |
| `mime_type` | string | optional | MIME type (default: "image/jpeg") |

### Requirements

- At least one of `image_urls` or `base64_images` must be provided
- Maximum 50 images total (URLs + base64 combined)
- Only one model image is used per request (if multiple provided, only first is used)
- Base64 images must have valid `data` field
- Model images are optional but enhance AI generation quality
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

### 4. Using Model Images

Model images serve as reference images for AI generation, particularly useful when your original images don't contain full bodies:

#### Model Images via URLs
```json
{
  "image_urls": ["https://example.com/clothing_item.jpg"],
  "model_urls": ["https://example.com/model_reference.jpg"],
  "person_prompt": "a professional model in their 20s with confident posture",
  "location_prompt": "in a modern studio with clean lighting",
  "animation_prompt": "smooth professional transitions with model poses"
}
```

#### Model Images via Base64
```json
{
  "image_urls": ["https://example.com/product.jpg"],
  "model_b64": [
    {
      "data": "iVBORw0KGgoAAAANSUhEUgAA...",
      "mime_type": "image/png"
    }
  ],
  "person_prompt": "an elegant fashion model with striking features",
  "animation_prompt": "cinematic fashion photography style transitions"
}
```

#### Mixed Model Images
```json
{
  "image_urls": ["https://example.com/garment.jpg"],
  "model_urls": ["https://example.com/reference_model1.jpg"],
  "location_prompt": "in a high-end fashion studio",
  "person_prompt": "a professional fashion model",
  "animation_prompt": "dynamic fashion show style movements"
}
```

{: .note }
> **Note**: If both `model_urls` and `model_b64` are provided, only the first model image from `model_urls` will be used.

---

## Response Format

### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Images processed successfully from URLs and base64 images!",
  "images_requested": 3,
  "models_requested": 1,
  "result": {
    "processed_images": [
      "https://storage.googleapis.com/bucket/processed_image1.jpg",
      "https://storage.googleapis.com/bucket/processed_image2.jpg"
    ],
    "saved_state_blob": "aigc_saved_state_uuid.json",
    "model_images": [
      "https://storage.googleapis.com/bucket/model_reference1.jpg"
    ],
    "total_model_images": 1
  }
}
```

The `saved_state_blob` can be used with the [Main Video API](/main-api/#create-a-video-from-a-preset) to create videos from processed images.

### Description-Only Response (do_not_alter: true)

When using `do_not_alter: true`, the response includes detailed AI-generated descriptions:

```json
{
  "status": "success",
  "message": "Images described successfully (description-only mode)!",
  "images_requested": 2,
  "result": {
    "images": [
      {
        "original_url": "https://example.com/product1.jpg",
        "final_url": "https://storage.googleapis.com/bucket/temp_image1.jpg",
        "description": "A front view of a blue cotton t-shirt displayed on a white background",
        "person_present": false,
        "person_full_body": false,
        "person_description": "A young adult male model with athletic build, wearing casual clothing",
        "garment_description": "A navy blue cotton crew neck t-shirt with short sleeves",
        "view": "front",
        "location_description": "Professional photography studio with clean white background"
      },
      {
        "original_url": "https://example.com/product2.jpg", 
        "final_url": "https://storage.googleapis.com/bucket/temp_image2.jpg",
        "description": "A back view of the same blue t-shirt showing the garment details",
        "person_present": false,
        "person_full_body": false,
        "person_description": "A young adult male model with athletic build, wearing casual clothing",
        "garment_description": "Back view of navy blue cotton t-shirt with standard fit",
        "view": "back",
        "location_description": "Professional photography studio with clean white background"
      }
    ],
    "processing_mode": "description_only",
    "do_not_alter": true
  }
}
```

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
    "animation_prompt": "cinematic fade transitions with slow panning movements"
  }'
```

### Advanced Configuration

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/image.jpg"],
    "pipeline_config_file": "in-studio_selected-assets_360.json",
    "location_prompt": "in a high-tech laboratory setting",
    "person_prompt": "a skilled scientist in a white lab coat conducting experiments",
    "animation_prompt": "360-degree rotating views with scientific precision movements"
  }'
```

### Using Model Images

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/garment.jpg"],
    "model_urls": ["https://example.com/model_reference.jpg"],
    "person_prompt": "a professional fashion model with elegant posture",
    "location_prompt": "in a modern photography studio with professional lighting",
    "animation_prompt": "smooth fashion photography transitions with model poses"
  }'
```

### Mixed Input with Model Images

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/clothing1.jpg"],
    "base64_images": [
      {
        "data": "iVBORw0KGgoAAAANSUhEUgAA...",
        "mime_type": "image/png"
      }
    ],
    "model_urls": ["https://example.com/reference_model.jpg"],
    "person_prompt": "a professional fashion model showcasing contemporary fashion",
    "location_prompt": "in a high-end fashion studio with dramatic lighting",
    "animation_prompt": "dynamic fashion show style movements with professional transitions"
  }'
```

{: .note }
> **Note**: Only one model image is used per request. If both `model_urls` and `model_b64` are provided, only the first image from `model_urls` will be used.

### Description-Only Processing

```bash
curl -X POST https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": [
      "https://example.com/product1.jpg",
      "https://example.com/product2.jpg"
    ],
    "do_not_alter": true,
    "location_prompt": "in a professional photography studio"
  }'
```

This returns detailed AI descriptions of your images without running expensive image generation steps, making it perfect for:
- Content analysis and cataloging
- Quick metadata extraction
- Testing image quality before full processing

---

## Image Processing Limits

| Limit | Value |
|-------|-------|
| **Maximum images per request** | 50 images |
| **Model images per request** | 1 image (only first used if multiple provided) |
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
   - Applies to both regular images and model images

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