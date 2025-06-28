---
layout: default
title: Changelog
nav_order: 6
description: "API updates, version history, and license information"
---

# Changelog
{: .no_toc }

API updates, version history, and license information
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Version History

### v0.1 BETA - April 28, 2025
{: .text-blue-200}

**Status:** Initial public beta release

#### Main Video API
- **NEW:** Initial release of video creation API
- **NEW:** Preset management (list, clone presets)
- **NEW:** Video creation from web articles
- **NEW:** Video status polling
- **NEW:** Multi-language support
- **NEW:** Webhook integration for async operations
- **NEW:** Integration with AIGC Preview API via `save_state`

#### AIGC Preview API
- **NEW:** Image processing through AI pipeline
- **NEW:** Support for URL-based image input
- **NEW:** Support for base64-encoded image input
- **NEW:** Mixed input support (URLs + base64)
- **NEW:** Configurable pipeline options
- **NEW:** Location prompt for AI context
- **NEW:** Saved state generation for video integration

#### Documentation
- **NEW:** Complete API documentation
- **NEW:** Multi-page professional layout
- **NEW:** Interactive examples and workflows
- **NEW:** Comprehensive error handling guide
- **NEW:** Webhook implementation examples

---

## Upcoming Features

### Planned for v0.2
{: .text-yellow-200}

- **Enhanced Presets**: More customization options for video styling
- **Batch Processing**: Process multiple videos simultaneously
- **Advanced Analytics**: Detailed processing metrics and insights
- **SDK Libraries**: Official SDKs for Python, JavaScript, and Go
- **Rate Limiting**: Improved request management and quotas

### Under Consideration
{: .text-grey-dk-200}

- **Real-time Preview**: Live video preview during processing
- **Custom Branding**: White-label options for enterprise customers
- **Advanced AI Features**: Object detection and scene analysis
- **Video Editing**: Post-processing capabilities
- **Collaborative Features**: Team management and sharing

---

## Breaking Changes

### None Yet
{: .text-green-200}

As this is the initial beta release, no breaking changes have been introduced yet. 

> **Future Breaking Changes:** We will provide at least 30 days notice before any breaking changes are implemented, along with migration guides and backwards compatibility periods where possible.

---

## Deprecation Notices

### None Currently
{: .text-green-200}

No features are currently deprecated.

---

## API Status & Reliability

### Current Status
- **Main Video API**: ✅ Stable beta
- **AIGC Preview API**: ✅ Stable preview  
- **Documentation**: ✅ Complete

### Service Level Objectives (SLOs)

| Metric | Target | Current |
|--------|--------|---------|
| **API Uptime** | 99.9% | 99.95% |
| **Response Time** | < 2s | ~1.2s |
| **Video Processing** | 95% success rate | 97% |
| **Image Processing** | 90% success rate | 94% |

### Known Issues

No known issues at this time.

---

## Migration Guides

### None Required
{: .text-green-200}

As this is the initial release, no migration is required.

---

## Security Updates

### v0.1 BETA - April 28, 2025

- **Implemented**: Bearer token authentication for Main API
- **Implemented**: HTTPS-only webhook endpoints
- **Implemented**: Input validation and sanitization
- **Implemented**: Rate limiting for abuse prevention

---

## Feedback & Contributions

We welcome feedback and suggestions for improving the Aeon APIs:

### How to Provide Feedback

1. **GitHub Issues**: Report bugs or request features
2. **Email**: api-feedback@project-aeon.com
3. **Discord**: Join our developer community
4. **Documentation**: Suggest improvements to our docs

### Beta Program

As a beta user, you have access to:
- **Priority Support**: Faster response times for issues
- **Early Access**: New features before general release
- **Direct Feedback**: Your input shapes our roadmap
- **Beta Channels**: Special communication channels

---

## License & Legal

### Documentation License

This documentation is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Aeon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### API Terms of Service

- **Beta Terms**: APIs are provided "as-is" during beta period
- **Fair Use**: Reasonable usage limits apply
- **Data Processing**: See our [Privacy Policy](https://project-aeon.com/privacy)
- **Liability**: Limited liability during beta testing

### Third-Party Licenses

This API uses the following third-party services and libraries:
- **Google Cloud Storage**: For video and image hosting
- **AI Processing**: Various AI models for content analysis
- **CDN Services**: For global content delivery

---

## Release Notes Template

For future releases, we'll follow this format:

### vX.X - Release Date

#### 🎉 New Features
- Feature descriptions with examples

#### 🐛 Bug Fixes  
- Bug fix descriptions

#### 📚 Documentation
- Documentation updates

#### ⚠️ Breaking Changes
- Breaking change descriptions with migration guides

#### 🔒 Security
- Security improvements

#### 📈 Performance
- Performance improvements

---

## Stay Updated

### Release Notifications

To stay informed about API updates:

1. **Subscribe**: Join our mailing list for release announcements
2. **RSS Feed**: Subscribe to our changelog RSS feed
3. **GitHub**: Watch our repository for updates
4. **Twitter**: Follow [@ProjectAeon](https://twitter.com/ProjectAeon)

### Changelog RSS Feed

Subscribe to our RSS feed for automatic updates:
```
https://docs.project-aeon.com/changelog.xml
```

---

## Archive

### Previous Versions

None yet - this is the initial release.

---

## Next Steps

<div class="code-example" markdown="1">

**Get Started:**
- [Getting Started Guide →](/getting-started/) - Set up your first API call
- [Main Video API →](/main-api/) - Create videos from content
- [AIGC Preview API →](/aigc-api/) - Process images with AI
- [Error Handling →](/errors/) - Handle errors and webhooks

**Stay Connected:**
- [GitHub Repository](https://github.com/your-repo) - Source code and issues
- [Discord Community](https://discord.gg/aeon) - Chat with other developers
- [Newsletter](https://project-aeon.com/newsletter) - Monthly updates

</div> 