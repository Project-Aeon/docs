# AIGC Preview API Test Suite

This test suite comprehensively tests the AIGC Preview API with various combinations of input parameters and generates detailed CSV reports.

## Files Overview

- `test_suite_config.json` - Configuration file defining all test parameters
- `test_suite_runner.py` - Main test execution script
- `test_results_YYYYMMDD_HHMMSS.csv` - Generated test results (created after running)
- `test_results_YYYYMMDD_HHMMSS.html` - Visual HTML report with image galleries (optional)

## Configuration Structure

The `test_suite_config.json` contains:

### Image Lists
- **shorts_single**: Single shorts clothing item
- **dress_multiple**: Full body dress with multiple views
- **bag_single**: Single bag product
- **temp_multiple**: Multiple temporary storage images  
- **front_back_pair**: Front and back view pair

### Location Prompts
- **none**: No location specified (null)
- **city_sidewalk**: "A bustling city sidewalk"

### Person Prompts  
- **none**: No person specified (null)
- **asian_girl**: "A cute asian girl, smiling and having fun"

### Pipeline Configurations
- **classic**: `in-studio_selected-assets_classic.json`
- **no_face**: `in-studio_selected-assets_no-face.json`
- **360**: `in-studio_selected-assets_360.json`

## Total Test Combinations

The test suite generates **30 total combinations**:
- 5 image lists × 2 location prompts × 2 person prompts × 3 pipeline configs = 30 tests

## Prerequisites

1. **API Server Running**: Make sure the AIGC Preview API is running on localhost:8080
   ```bash
   python main.py
   ```

2. **Python Dependencies**: Ensure you have the required packages:
   ```bash
   pip install requests
   ```

## Usage

### Basic Usage
```bash
python test_suite_runner.py
```

### With Custom Config File
```bash
python test_suite_runner.py my_custom_config.json
```

### With Pause After Each Test
```bash
python test_suite_runner.py --pause
```

### With HTML Report Generation
```bash
python test_suite_runner.py --html
```

### Custom Config with Pause and HTML
```bash
python test_suite_runner.py my_custom_config.json --pause --html
```

### Generate HTML from Existing CSV
```bash
python test_suite_runner.py --html-from-csv test_results_20250630_212048.csv
```

### Custom Host Testing
```bash
# Test against a remote server
python test_suite_runner.py --host api.example.com

# Test with full URL including protocol and port
python test_suite_runner.py --host https://staging.myapp.com:3000

# Combine with other options
python test_suite_runner.py --host my-server.com --pause --html
```

### Getting Help
```bash
python test_suite_runner.py --help
```

### Making the Script Executable (Optional)
```bash
chmod +x test_suite_runner.py
./test_suite_runner.py --pause
```

## Test Execution Flow

1. **Health Check**: Verifies API server is reachable at localhost:8080
2. **Load Configuration**: Reads test parameters from JSON config
3. **Generate Combinations**: Creates all possible test combinations
4. **Execute Tests**: Runs each combination with retry logic
5. **Save Results**: Outputs comprehensive CSV report
6. **Print Summary**: Shows execution statistics

## Pause Mode Feature

The `--pause` option allows you to manually review each test result before proceeding:

### When to Use Pause Mode
- **Debugging**: Step through tests to identify issues
- **Manual Review**: Inspect API responses and processing results
- **Resource Monitoring**: Check system performance between tests
- **Learning**: Understand what each test combination does

### Pause Mode Controls
When pause mode is enabled, after each test you can:
- **Press Enter**: Continue to the next test
- **Type 'q' + Enter**: Quit immediately and save all completed results to CSV  
- **Type 's' + Enter**: Skip remaining pauses and run at full speed

### Interruption Handling
The test suite **always saves partial results** when interrupted:
- **Ctrl+C**: Saves all completed tests before exiting
- **'q' in pause mode**: Saves all completed tests before exiting  
- **Unexpected errors**: Saves completed tests even if the suite crashes
- **Early termination**: You never lose your progress!

### Example with Pause Mode
```
🧪 Test 1/30: shorts_single_none_none_classic
   📷 Images: Single Shorts Image (1 images)
   📍 Location: No Location
   👤 Person: No Person Prompt
   ⚙️  Pipeline: Classic Configuration
   ✅ SUCCESS in 45.2s - 1 images processed
   ⏸️  Test completed. Press Enter to continue to next test, 'q' to quit and save results, or 's' to skip remaining pauses...
   [waiting for user input]
```

### Example with Early Exit
```
🧪 Test 5/30: dress_multiple_city_sidewalk_classic
   ✅ SUCCESS in 67.3s - 2 images processed
   ⏸️  Test completed. Press Enter to continue to next test, 'q' to quit and save results, or 's' to skip remaining pauses...
   q
   🛑 User requested to quit. Will save 5 completed test results...

⚠️  Test execution interrupted by user!
💾 Saving partial results from 5 completed tests...

📋 Saving results...
📊 Results saved to: test_results_20250101_143022.csv

📁 Partial results saved to: test_results_20250101_143022.csv
✅ 5 test results preserved despite interruption
```

## Sample Output

```
🧪 AIGC Preview API Test Suite Runner
==================================================
✅ API server is reachable at localhost:8080
✅ Loaded configuration from test_suite_config.json
📊 Generated 30 test combinations

🚀 Starting test execution...
📋 Configuration: AIGC Preview API Test Suite
🎯 Target: http://localhost:8080/create-slideshow-urls

🧪 Test 1/30: shorts_single_none_none_classic
   📷 Images: Single Shorts Image (1 images)
   📍 Location: No Location
   👤 Person: No Person Prompt
   ⚙️  Pipeline: Classic Configuration
   ✅ SUCCESS in 45.2s - 1 images processed
📊 Progress: 3.3% (1/30)

[... continues for all 30 tests ...]

============================================================
📈 TEST EXECUTION SUMMARY
============================================================
⏱️  Total Duration: 1247.3 seconds (20.8 minutes)
🧪 Total Tests: 30/30
✅ Successful: 28
❌ Failed: 2
📊 Success Rate: 93.3%
⏱️  Average Test Duration: 41.6 seconds
============================================================

📁 Results saved to: test_results_20250101_143022.csv
```

## CSV Output Format

The generated CSV contains the following columns:

### Test Identification
- `timestamp` - When the test was executed
- `test_id` - Unique test identifier
- `test_number` - Sequential test number

### Input Parameters
- `image_list_key` - Image list identifier
- `image_list_name` - Human-readable image list name
- `image_list_description` - Description of the image set
- `image_urls` - Semicolon-separated list of image URLs
- `image_count` - Number of images in the set
- `location_prompt_key` - Location prompt identifier
- `location_prompt_name` - Human-readable location name
- `location_prompt_value` - Actual location prompt text
- `person_prompt_key` - Person prompt identifier  
- `person_prompt_name` - Human-readable person prompt name
- `person_prompt_value` - Actual person prompt text
- `pipeline_config_key` - Pipeline configuration identifier
- `pipeline_config_name` - Human-readable pipeline name
- `pipeline_config_filename` - Configuration file name

### Results
- `success` - Whether the test passed (True/False)
- `duration_seconds` - Test execution time
- `error_message` - Error details if test failed
- `response_status` - API response status
- `images_requested` - Number of images requested
- `processed_images_count` - Number of images successfully processed
- `processed_image_urls` - Semicolon-separated processed image URLs
- `saved_state_blob` - Generated state blob identifier

## Error Handling & Retries

The test suite includes robust error handling:

- **Automatic Retries**: Up to 3 attempts per test
- **Timeout Handling**: 300-second timeout per request
- **Connection Errors**: Graceful handling of server unavailability  
- **HTTP Errors**: Detailed error message capture
- **Interrupted Execution**: Saves partial results if stopped

## Customizing Tests

### Adding New Image Lists
```json
"new_image_set": {
  "name": "My Custom Images",
  "description": "Description of the image set",
  "urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ]
}
```

### Adding New Prompts
```json
"new_location": {
  "name": "Beach Setting",
  "description": "Tropical beach environment",
  "value": "on a sunny tropical beach with palm trees"
}
```

### Modifying Test Settings
```json
"test_settings": {
  "animation_prompt": "your custom animation prompt",
  "max_retries": 5,
  "retry_delay_seconds": 10,
  "save_response_details": true,
  "include_processing_history": true
}
```

## Analysis Tips

### Using the CSV Data
1. **Filter by Success/Failure**: Identify which combinations work best
2. **Performance Analysis**: Sort by `duration_seconds` to find slow tests
3. **Error Patterns**: Group by `error_message` to identify common issues
4. **Configuration Comparison**: Compare success rates across pipeline configs
5. **Partial Results**: Interrupted test runs are still valuable for analysis

### Working with Partial Results
- **CSV format is identical**: Partial results use the same CSV structure as complete runs
- **Timestamps show progress**: Use `test_number` column to see how far tests progressed  
- **Still statistically valid**: Even partial results can reveal performance patterns
- **Combine multiple runs**: Merge CSV files from different test sessions if needed
- **HTML from partial results**: Generate visual reports even from interrupted test runs

### Excel/Sheets Analysis
- Import the CSV into Excel or Google Sheets
- Create pivot tables to analyze success rates by parameter
- Generate charts showing performance trends
- Filter data to focus on specific test scenarios

## HTML Visual Reports 🌐

The test suite can generate beautiful HTML reports with clickable image galleries that make it easy to visually review test results.

### HTML Report Features

- **📊 Dashboard Overview**: Summary statistics with success/failure rates
- **🖼️ Image Galleries**: Thumbnail views of both input and processed images
- **🔍 Clickable Images**: Click any thumbnail to open full-size image in new tab  
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **🎨 Modern UI**: Clean, professional styling with intuitive navigation
- **⚡ Fast Loading**: Lazy-loaded images for optimal performance

### When to Use HTML Reports

- **👀 Visual Review**: Quickly scan all test results at a glance
- **🔍 Quality Control**: Spot-check processed image quality across tests
- **📋 Client Presentations**: Professional reports for stakeholders
- **🐛 Debugging**: Visual identification of processing issues
- **📊 Analysis**: Compare results across different configurations

### HTML Generation Options

#### 1. Generate HTML After Tests
```bash
# Run tests and automatically generate HTML report
python test_suite_runner.py --html

# With pause mode and HTML generation
python test_suite_runner.py --pause --html
```

#### 2. Generate HTML from Existing CSV
```bash
# Generate HTML from previous test results (no re-running tests)
python test_suite_runner.py --html-from-csv test_results_20250630_212048.csv
```

### HTML Report Layout

The generated HTML includes:

1. **Header Dashboard**
   - Total tests run
   - Success/failure counts
   - Overall success rate
   - Test execution timeframe

2. **Summary Cards**
   - Visual statistics display
   - Color-coded success indicators

3. **Detailed Results Table**
   - Test identification and status
   - Configuration details (pipeline, location, person prompts)
   - Input image thumbnails
   - Processed image thumbnails
   - Execution duration
   - Error messages (if any)

### Example HTML Output Structure
```
🧪 AIGC Preview API Test Results
📊 30 total tests | ✅ 28 successful | ❌ 2 failed
📈 Success Rate: 93.3%

┌─────────────────────────────────────────────────────┐
│ Test │ Status │ Config │ Input Images │ Output Images │
├─────────────────────────────────────────────────────┤
│ #1   │   ✅    │ Classic│   [img] [img] │   [img] [img] │
│ #2   │   ✅    │ No-Face│      [img]    │      [img]    │
│ #3   │   ❌    │   360  │   [img] [img] │       -       │
└─────────────────────────────────────────────────────┘
```

## Command Line Options

### Available Options
- `-p, --pause`: Enable pause mode (pause after each test)
- `--html`: Generate HTML report after running tests
- `--html-from-csv <file>`: Generate HTML report from existing CSV file
- `--host <url>`: Specify custom host URL (default: localhost:8080)
- `--help`: Show help message and exit

### Option Examples
```bash
# Run with default settings
python test_suite_runner.py

# Run with pause mode enabled
python test_suite_runner.py --pause

# Run tests and generate HTML report
python test_suite_runner.py --html

# Use custom config with pause mode and HTML
python test_suite_runner.py my_config.json --pause --html

# Test against custom host
python test_suite_runner.py --host api.example.com

# Generate HTML from existing CSV (no new tests)
python test_suite_runner.py --html-from-csv results.csv

# Show help
python test_suite_runner.py --help
```

## Troubleshooting

### Common Issues

**API Server Not Running**
```
❌ Cannot reach API server at localhost:8080
💡 Make sure the API server is running with: python main.py
```
Solution: Start the API server before running tests

**Configuration File Missing**
```
❌ Configuration file 'test_suite_config.json' not found!
```
Solution: Ensure the config file exists in the same directory

**Tests Timing Out**
```
Request timeout after 300 seconds
```
Solution: Increase `timeout_seconds` in config or check server performance

**Memory Issues**
If processing many large images, monitor system resources and consider:
- Running tests in smaller batches
- Increasing system memory
- Reducing concurrent image processing

## Performance Expectations

Based on typical API response times:
- **Single image tests**: 30-60 seconds each
- **Multiple image tests**: 60-120 seconds each  
- **Full test suite (30 tests)**: 20-40 minutes total

Actual times depend on:
- Server performance and load
- Image sizes and complexity
- Network latency
- Pipeline configuration complexity

## Quick Start Examples

### Run Tests with Visual Results
```bash
# Run full test suite with HTML report
python test_suite_runner.py --html

# Run with manual control and HTML report  
python test_suite_runner.py --pause --html

# Test against staging with HTML report
python test_suite_runner.py --host staging.myapp.com --html
```

### Generate HTML from Previous Results
```bash
# Find your CSV files
ls test_results_*.csv

# Generate visual report from any CSV
python test_suite_runner.py --html-from-csv test_results_20250630_212048.csv
```

The HTML reports make it easy to:
- 🔍 **Visually inspect** both input and output images side-by-side
- 📊 **Quickly identify** which configurations work best
- 🎯 **Share results** with team members or clients
- 🐛 **Debug issues** by seeing exactly what each test produced

## Custom Host Testing 🌐

Test your API against different environments without changing configuration files.

### Host URL Flexibility

The `--host` option accepts various URL formats:
```bash
# Simple hostname (adds http:// automatically)
--host api.example.com

# Hostname with port
--host my-server.com:3000

# Full URL with protocol
--host https://staging.myapp.com

# Full URL with custom port
--host https://production.api.com:8443
```

### Environment Testing Use Cases

#### 🏠 **Local Development**
```bash
# Test different local ports
python test_suite_runner.py --host localhost:3000
python test_suite_runner.py --host 127.0.0.1:8000
```

#### 🧪 **Staging Environment**
```bash
# Test staging deployment
python test_suite_runner.py --host staging.myapp.com --html
```

#### 🚀 **Production Validation**
```bash
# Validate production environment (be careful!)
python test_suite_runner.py --host https://api.production.com --pause
```

#### 🔗 **Cloud Services**
```bash
# Test against Cloud Run, Heroku, AWS, etc.
python test_suite_runner.py --host https://myapp-12345.herokuapp.com
python test_suite_runner.py --host https://myservice.run.app
```

### Benefits of Custom Host Testing

- **🔄 Environment Parity**: Test the same scenarios across dev/staging/prod
- **🐛 Deployment Validation**: Verify new deployments work correctly
- **📊 Performance Comparison**: Compare response times across environments
- **🛡️ Load Testing**: Run comprehensive tests against staging before production
- **🌍 Regional Testing**: Test different geographic deployments

### Host Configuration Notes

- **Health Check**: Automatically tests `/health` endpoint on the specified host
- **Protocol Detection**: Adds `http://` if no protocol specified
- **Config Override**: Host URL overrides the `base_url` in your config file
- **Error Handling**: Provides clear feedback if host is unreachable 