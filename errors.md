---
layout: default
title: Errors & Webhooks
nav_order: 5
description: "Error handling and webhook integration for Aeon APIs"
---

# Errors & Webhooks
{: .no_toc }

Error handling and webhook integration reference
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## HTTP Error Codes

Both Aeon APIs use standard HTTP status codes to indicate success or failure.

| HTTP Code | Status | Most Common Causes |
|-----------|--------|--------------------|
| **200** | OK | Request successful |
| **400** | Bad Request | Missing or malformed JSON, invalid parameters |
| **401** | Unauthorized | Invalid API token (Main API only) |
| **403** | Forbidden | Wrong `user_key` for resource |
| **404** | Not Found | Invalid preset ID, video ID, or endpoint |
| **500** | Internal Server Error | Server-side processing failure |

---

## Error Response Format

### Main Video API Errors

```json
{
  "status": "error",
  "message": "Detailed error description",
  "error_code": "SPECIFIC_ERROR_CODE"
}
```

### AIGC Preview API Errors

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Common Error Scenarios

### Authentication Errors (Main API)

#### Missing API Token
```bash
# Request without Authorization header
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets" \
  -H "Content-Type: application/json" \
  -d '{"user_key": "YOUR_USER_KEY"}'
```

**Response (401):**
```json
{
  "status": "error",
  "message": "Missing or invalid authorization token"
}
```

#### Invalid User Key
```bash
# Request with wrong user_key
curl -X POST "https://app.project-aeon.com/api/1.1/wf/ae_get_presets" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_key": "INVALID_KEY"}'
```

**Response (403):**
```json
{
  "status": "error",
  "message": "Invalid user key or insufficient permissions"
}
```

### Request Validation Errors

#### Missing Required Fields
```json
{
  "status": "error",
  "message": "Missing required field: preset_video_id"
}
```

#### Invalid Parameter Types
```json
{
  "status": "error",
  "message": "Field 'captions' must be a boolean value"
}
```

### Resource Not Found Errors

#### Invalid Preset ID
```json
{
  "status": "error",
  "message": "Preset not found or access denied",
  "error_code": "PRESET_NOT_FOUND"
}
```

#### Invalid Video ID
```json
{
  "status": "error",
  "message": "Video not found or access denied",
  "error_code": "VIDEO_NOT_FOUND"
}
```

### AIGC API Specific Errors

#### No Images Provided
```json
{
  "detail": "No image URLs or base64 images provided"
}
```

#### Too Many Images
```json
{
  "detail": "Too many images. Maximum 50 images allowed (URLs + base64 combined)"
}
```

#### Invalid Base64 Data
```json
{
  "detail": "Invalid base64 image data at index 2"
}
```

#### Processing Timeout
```json
{
  "detail": "Image processing timeout after 180 seconds"
}
```

---

## Error Handling Best Practices

### 1. Implement Exponential Backoff

For 5xx errors, implement retry logic with exponential backoff:

```python
import time
import requests

def api_request_with_retry(url, headers, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code >= 500:
                # Server error - retry with backoff
                wait_time = (2 ** attempt) + 1
                print(f"Server error, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                # Client error - don't retry
                return response.json()
                
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            
    return {"error": "Max retries exceeded"}
```

### 2. Validate Input Before Sending

```python
def validate_video_request(data):
    required_fields = ['preset_video_id', 'video_name', 'user_key']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate either source_url or save_state is provided
    if not data.get('source_url') and not data.get('save_state'):
        raise ValueError("Either source_url or save_state must be provided")
    
    return True
```

### 3. Handle Rate Limits

```python
def handle_rate_limit(response):
    if response.status_code == 429:
        retry_after = response.headers.get('Retry-After', 60)
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(int(retry_after))
        return True
    return False
```

---

## Webhooks

Webhooks allow you to receive notifications when long-running operations complete, eliminating the need for polling.

### Webhook Requirements

- **HTTPS endpoints only** (HTTP not supported)
- **Respond with 2xx status code** to acknowledge receipt
- **Timeout:** 30 seconds maximum response time
- **Retry policy:** 3 attempts with exponential backoff

### Video Creation Webhook

When you provide a `callback_url` to video creation endpoints, Aeon will POST the following JSON upon completion:

```json
{
  "video_id": "1234567890",
  "status": "Completed",
  "video_url": "https://storage.googleapis.com/aeon-ptv-bucket/your-video.mp4",
  "preset_video_id": "1745530741190x383445637",
  "video_name": "Your Video Title",
  "created_at": "2025-04-28T10:30:00Z"
}
```

### Preset Cloning Webhook

When cloning presets, the webhook payload includes:

```json
{
  "preset_video_id": "NEW_PRESET_ID",
  "status": "Completed",
  "clone_from_preset_id": "ORIGINAL_PRESET_ID",
  "created_at": "2025-04-28T10:30:00Z"
}
```

### Webhook Implementation Example

```python
from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

@app.route('/aeon-webhook', methods=['POST'])
def handle_aeon_webhook():
    try:
        # Get the webhook payload
        payload = request.get_json()
        
        # Validate the webhook (optional - add signature verification)
        if not validate_webhook_signature(request):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Handle different webhook types
        if 'video_id' in payload:
            handle_video_completion(payload)
        elif 'preset_video_id' in payload:
            handle_preset_completion(payload)
        
        # Always return 200 to acknowledge receipt
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'error': 'Processing failed'}), 500

def handle_video_completion(payload):
    video_id = payload['video_id']
    status = payload['status']
    video_url = payload.get('video_url')
    
    if status == 'Completed' and video_url:
        print(f"Video {video_id} completed: {video_url}")
        # Update your database, notify users, etc.
    else:
        print(f"Video {video_id} failed or still processing")

def handle_preset_completion(payload):
    preset_id = payload['preset_video_id']
    print(f"Preset cloned successfully: {preset_id}")
    # Update your database with new preset ID

def validate_webhook_signature(request):
    # Implement signature validation if needed
    # signature = request.headers.get('X-Aeon-Signature')
    # return verify_signature(request.data, signature)
    return True
```

### Testing Webhooks

For development, you can use tools like ngrok to expose your local server:

```bash
# Install ngrok
npm install -g ngrok

# Expose your local webhook endpoint
ngrok http 3000

# Use the HTTPS URL in your API requests
# https://abc123.ngrok.io/aeon-webhook
```

### Webhook Security

1. **Validate the source**: Only accept webhooks from known Aeon IPs
2. **Use HTTPS**: Never accept webhooks over HTTP
3. **Verify signatures**: Implement signature verification if provided
4. **Idempotency**: Handle duplicate webhooks gracefully

---

## Troubleshooting Guide

### Common Issues

#### 1. Video Creation Fails

**Symptoms:**
- 400 error with "Invalid source URL"
- Video stuck in processing state

**Solutions:**
- Verify the source URL is publicly accessible
- Check that the webpage has sufficient text content
- Try a different preset ID

#### 2. AIGC Processing Timeouts

**Symptoms:**
- 500 error after 180 seconds
- "Processing timeout" error

**Solutions:**
- Reduce the number of images per request
- Use smaller image files
- Try processing images in batches

#### 3. Webhook Not Received

**Symptoms:**
- Long-running operations complete but no webhook received

**Solutions:**
- Verify webhook URL is HTTPS and publicly accessible
- Check webhook endpoint responds with 2xx status code
- Review server logs for webhook delivery attempts

#### 4. Authentication Issues

**Symptoms:**
- 401/403 errors despite correct credentials

**Solutions:**
- Regenerate API token from dashboard
- Verify user key hasn't expired (change password/email)
- Check token isn't being committed to source control

---

## Getting Help

If you encounter persistent issues:

1. **Check Status**: Verify API status at [status.project-aeon.com](https://status.project-aeon.com)
2. **Review Logs**: Enable detailed logging in your application
3. **Test Endpoints**: Use curl to isolate the issue
4. **Contact Support**: Provide error logs and request details

---

## Next Steps

<div class="code-example" markdown="1">

**Explore More:**
- [Getting Started →](/getting-started/) - Basic setup guide
- [Main Video API →](/main-api/) - Create videos from content
- [AIGC Preview API →](/aigc-api/) - Process images with AI
- [Changelog →](/changelog/) - API updates and changes

</div> 