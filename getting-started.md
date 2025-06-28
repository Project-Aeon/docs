---
layout: default
title: Getting Started
nav_order: 2
description: "Authentication, user keys, and quick start guide for Aeon APIs"
---

# Getting Started
{: .no_toc }

Everything you need to know to start using Aeon APIs
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Authentication & Security

All Aeon APIs use a two-part authentication system:

| Header | Example value | Notes |
|--------|---------------|-------|
| `Authorization` | `Bearer YOUR_API_TOKEN` | Obtain from your Aeon dashboard *(never commit real tokens to Git)* |
| `Content-Type` | `application/json` | All requests and responses use JSON |

You'll **also** pass a **`user_key`** in most request bodies.  
The user key identifies your account and determines which presets and videos you can access.

> **Security Tip:** Store both the API token and user key in your CI/CD secret manager—*never* in source control.
{: .text-grey-dk-000 .bg-grey-lt-000}

---

## Generate a User Key

User keys don't expire, but they become invalid if you change your email or password.

| Step | Description |
|------|-------------|
| 1 | Log in to your Aeon dashboard |
| 2 | Click **Profile → API** |
| 3 | Click **Generate user key** and copy the value |

---

## Quick Start

### Video from Web Article

```bash
# 1. List available presets
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_key": "YOUR_USER_KEY", "built_in": true}'

# 2. Create video from web article
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preset_video_id": "1745530741190x383445637",
    "video_name": "My First Video",
    "source_url": "https://example.com/article",
    "user_key": "YOUR_USER_KEY",
    "callback_url": "https://yourserver.com/webhook"
  }'

# 3. Check video status
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_video" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "VIDEO_ID", "user_key": "YOUR_USER_KEY"}'
```

### Video from Images

```bash
# 1. Process images through AIGC API
curl -X POST "https://aigc-preview-889529529975.us-central1.run.app/create-slideshow-urls" \
  -H "Content-Type: application/json" \
  -d '{
    "image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "location_prompt": "in a modern office setting"
  }'

# 2. Create video using saved state
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_new_video_from_preset" \
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

## Base URLs

### Main Video API
```
https://app.project-aeon.com/api/1.1/wf/
```

### AIGC Preview API
```
https://aigc-preview-889529529975.us-central1.run.app
```

---

## Next Steps

<div class="code-example" markdown="1">

**Explore the APIs:**
- [Main Video API →](/main-api/) - Convert articles to videos
- [AIGC Preview API →](/aigc-api/) - Process images with AI
- [Error Reference →](/errors/) - Handle errors and webhooks

**Need Help?**
- Check our [complete examples](/main-api/#examples)
- Review [common errors](/errors/)
- Understand [webhook integration](/errors/#webhooks)

</div> 