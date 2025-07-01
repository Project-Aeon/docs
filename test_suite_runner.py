#!/usr/bin/env python3
"""
AIGC Preview API Test Suite Runner

This script reads test configurations and runs comprehensive tests
against the localhost API, generating CSV results with detailed metrics.
"""

import json
import csv
import requests
import time
import itertools
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import traceback
import html

class TestSuiteRunner:
    def __init__(self, config_file: str = "test_suite_config.json", pause_after_tests: bool = False, generate_html: bool = False, host_url: str = None):
        """Initialize the test suite runner with configuration."""
        self.config_file = config_file
        self.config = None
        self.results = []
        self.start_time = None
        self.total_combinations = 0
        self.completed_tests = 0
        self.successful_tests = 0
        self.failed_tests = 0
        self.pause_after_tests = pause_after_tests
        self.generate_html = generate_html
        self.host_url = host_url
        
    def load_config(self) -> bool:
        """Load test configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            
            # Override base_url if host_url is provided
            if self.host_url:
                # Ensure host_url has proper format
                if not self.host_url.startswith(('http://', 'https://')):
                    self.host_url = f"http://{self.host_url}"
                self.config["base_url"] = self.host_url
                print(f"✅ Loaded configuration from {self.config_file}")
                print(f"🌐 Using custom host: {self.host_url}")
            else:
                print(f"✅ Loaded configuration from {self.config_file}")
                print(f"🌐 Using default host: {self.config.get('base_url', 'http://localhost:8080')}")
            
            return True
        except FileNotFoundError:
            print(f"❌ Configuration file {self.config_file} not found!")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {self.config_file}: {e}")
            return False
            
    def generate_test_combinations(self) -> List[Dict]:
        """Generate all possible test combinations from configuration."""
        combinations = []
        
        # Get all parameter sets
        image_lists = self.config["image_lists"]
        location_prompts = self.config["location_prompts"] 
        person_prompts = self.config["person_prompts"]
        pipeline_configs = self.config["pipeline_configs"]
        
        # Generate all combinations
        for img_key, img_data in image_lists.items():
            for loc_key, loc_data in location_prompts.items():
                for person_key, person_data in person_prompts.items():
                    for pipe_key, pipe_data in pipeline_configs.items():
                        combination = {
                            "test_id": f"{img_key}_{loc_key}_{person_key}_{pipe_key}",
                            "image_list_key": img_key,
                            "image_list_name": img_data["name"],
                            "image_list_description": img_data["description"],
                            "image_urls": img_data["urls"],
                            "image_count": len(img_data["urls"]),
                            "location_prompt_key": loc_key,
                            "location_prompt_name": loc_data["name"],
                            "location_prompt_value": loc_data["value"],
                            "person_prompt_key": person_key,
                            "person_prompt_name": person_data["name"],
                            "person_prompt_value": person_data["value"],
                            "pipeline_config_key": pipe_key,
                            "pipeline_config_name": pipe_data["name"],
                            "pipeline_config_filename": pipe_data["filename"]
                        }
                        combinations.append(combination)
        
        self.total_combinations = len(combinations)
        print(f"📊 Generated {self.total_combinations} test combinations")
        return combinations
        
    def create_api_request_body(self, combination: Dict) -> Dict:
        """Create API request body from test combination."""
        request_body = {
            "image_urls": combination["image_urls"],
            "base64_images": [],
            "pipeline_config_file": combination["pipeline_config_filename"],
            "animation_prompt": self.config["test_settings"]["animation_prompt"]
        }
        
        # Add optional prompts if they have values
        if combination["location_prompt_value"]:
            request_body["location_prompt"] = combination["location_prompt_value"]
            
        if combination["person_prompt_value"]:
            request_body["person_prompt"] = combination["person_prompt_value"]
            
        return request_body
        
    def make_api_call(self, combination: Dict) -> Tuple[bool, Dict, float, Optional[str]]:
        """Make API call with retry logic. Returns (success, response_data, duration, error)."""
        url = f"{self.config['base_url']}{self.config['endpoint']}"
        headers = {"Content-Type": "application/json"}
        request_body = self.create_api_request_body(combination)
        
        max_retries = self.config["test_settings"]["max_retries"]
        retry_delay = self.config["test_settings"]["retry_delay_seconds"]
        timeout = self.config["timeout_seconds"]
        
        for attempt in range(max_retries + 1):
            try:
                start_time = time.time()
                response = requests.post(
                    url, 
                    json=request_body, 
                    headers=headers, 
                    timeout=timeout
                )
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    return True, response.json(), duration, None
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    if attempt < max_retries:
                        print(f"  ⚠️  Attempt {attempt + 1} failed: {error_msg}")
                        print(f"     Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        return False, {}, duration, error_msg
                        
            except requests.exceptions.Timeout:
                duration = timeout
                error_msg = f"Request timeout after {timeout} seconds"
                if attempt < max_retries:
                    print(f"  ⚠️  Attempt {attempt + 1} timed out, retrying...")
                    time.sleep(retry_delay)
                    continue
                else:
                    return False, {}, duration, error_msg
                    
            except requests.exceptions.ConnectionError:
                duration = time.time() - start_time if 'start_time' in locals() else 0
                error_msg = "Connection error - is the API server running?"
                if attempt < max_retries:
                    print(f"  ⚠️  Attempt {attempt + 1} connection failed, retrying...")
                    time.sleep(retry_delay)
                    continue
                else:
                    return False, {}, duration, error_msg
                    
            except Exception as e:
                duration = time.time() - start_time if 'start_time' in locals() else 0
                error_msg = f"Unexpected error: {str(e)}"
                if attempt < max_retries:
                    print(f"  ⚠️  Attempt {attempt + 1} failed: {error_msg}")
                    time.sleep(retry_delay)
                    continue
                else:
                    return False, {}, duration, error_msg
                    
        return False, {}, 0, "Max retries exceeded"
        
    def process_api_response(self, combination: Dict, success: bool, response_data: Dict, 
                           duration: float, error: Optional[str]) -> Dict:
        """Process API response and create result record."""
        timestamp = datetime.now().isoformat()
        
        result = {
            # Test identification
            "timestamp": timestamp,
            "test_id": combination["test_id"],
            "test_number": self.completed_tests + 1,
            
            # Input parameters
            "image_list_key": combination["image_list_key"],
            "image_list_name": combination["image_list_name"],
            "image_list_description": combination["image_list_description"],
            "image_urls": "; ".join(combination["image_urls"]),
            "image_count": combination["image_count"],
            "location_prompt_key": combination["location_prompt_key"],
            "location_prompt_name": combination["location_prompt_name"],
            "location_prompt_value": combination["location_prompt_value"] or "",
            "person_prompt_key": combination["person_prompt_key"],
            "person_prompt_name": combination["person_prompt_name"],
            "person_prompt_value": combination["person_prompt_value"] or "",
            "pipeline_config_key": combination["pipeline_config_key"],
            "pipeline_config_name": combination["pipeline_config_name"],
            "pipeline_config_filename": combination["pipeline_config_filename"],
            
            # Results
            "success": success,
            "duration_seconds": round(duration, 2),
            "error_message": error or "",
        }
        
        if success and response_data:
            # Extract response details
            result.update({
                "response_status": response_data.get("status", ""),
                "images_requested": response_data.get("images_requested", 0),
                "processed_images_count": len(response_data.get("processed_images", [])),
                "processed_image_urls": "; ".join(response_data.get("processed_images", [])),
                "saved_state_blob": response_data.get("saved_state_blob", ""),
            })
        else:
            # Fill in empty values for failed requests
            result.update({
                "response_status": "",
                "images_requested": 0,
                "processed_images_count": 0,
                "processed_image_urls": "",
                "saved_state_blob": "",
            })
            
        return result
        
    def run_single_test(self, combination: Dict, test_num: int) -> Dict:
        """Run a single test and return the result."""
        print(f"\n🧪 Test {test_num}/{self.total_combinations}: {combination['test_id']}")
        print(f"   📷 Images: {combination['image_list_name']} ({combination['image_count']} images)")
        print(f"   📍 Location: {combination['location_prompt_name']}")
        print(f"   👤 Person: {combination['person_prompt_name']}")
        print(f"   ⚙️  Pipeline: {combination['pipeline_config_name']}")
        
        success, response_data, duration, error = self.make_api_call(combination)
        result = self.process_api_response(combination, success, response_data, duration, error)
        
        if success:
            print(f"   ✅ SUCCESS in {duration:.1f}s - {result['processed_images_count']} images processed")
            self.successful_tests += 1
        else:
            print(f"   ❌ FAILED in {duration:.1f}s - {error}")
            self.failed_tests += 1
            
        self.completed_tests += 1
        return result
        
    def save_results_to_csv(self, filename: Optional[str] = None) -> str:
        """Save test results to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.csv"
            
        if not self.results:
            print("⚠️  No results to save - no tests were completed!")
            # Create an empty CSV file with headers for consistency
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    # Write just the headers based on expected structure
                    headers = [
                        "timestamp", "test_id", "test_number", "image_list_key", "image_list_name",
                        "image_list_description", "image_urls", "image_count", "location_prompt_key",
                        "location_prompt_name", "location_prompt_value", "person_prompt_key",
                        "person_prompt_name", "person_prompt_value", "pipeline_config_key",
                        "pipeline_config_name", "pipeline_config_filename", "success",
                        "duration_seconds", "error_message", "response_status", "images_requested",
                        "processed_images_count", "processed_image_urls", "saved_state_blob"
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                print(f"📄 Empty CSV file created: {filename}")
            except Exception as e:
                print(f"❌ Error creating empty CSV: {e}")
            return filename
            
        # Get all field names from the first result
        fieldnames = list(self.results[0].keys())
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
                
            print(f"📊 Results saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return filename
            
    def generate_html_report(self, csv_filename: str = None, results: List[Dict] = None) -> str:
        """Generate HTML report from results or CSV file."""
        if results is None:
            if csv_filename and os.path.exists(csv_filename):
                results = self.load_results_from_csv(csv_filename)
            else:
                results = self.results
                
        if not results:
            print("⚠️  No results available for HTML generation!")
            return ""
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"test_results_{timestamp}.html"
        
        # Generate HTML content
        html_content = self.create_html_content(results)
        
        try:
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"🌐 HTML report generated: {html_filename}")
            return html_filename
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            return ""
            
    def load_results_from_csv(self, csv_filename: str) -> List[Dict]:
        """Load test results from CSV file."""
        results = []
        try:
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                results = list(reader)
                
            # Convert string booleans and numbers back to proper types
            for result in results:
                result['success'] = result.get('success', '').lower() == 'true'
                try:
                    result['duration_seconds'] = float(result.get('duration_seconds', 0))
                    result['image_count'] = int(result.get('image_count', 0))
                    result['images_requested'] = int(result.get('images_requested', 0))
                    result['processed_images_count'] = int(result.get('processed_images_count', 0))
                    result['test_number'] = int(result.get('test_number', 0))
                except (ValueError, TypeError):
                    pass  # Keep as string if conversion fails
                    
            print(f"📊 Loaded {len(results)} results from {csv_filename}")
            return results
            
        except Exception as e:
            print(f"❌ Error loading CSV file {csv_filename}: {e}")
            return []
            
    def create_html_content(self, results: List[Dict]) -> str:
        """Create HTML content for the test results report."""
        
        # Calculate summary statistics
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get('success', False))
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Get timestamp range
        timestamps = [r.get('timestamp', '') for r in results if r.get('timestamp')]
        start_time = min(timestamps) if timestamps else 'Unknown'
        end_time = max(timestamps) if timestamps else 'Unknown'
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIGC Preview API Test Results</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        
        .header p {{
            margin: 5px 0;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        
        .summary-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .success {{ color: #28a745; }}
        .failure {{ color: #dc3545; }}
        
        .table-container {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: #f8f9fa;
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        
        td {{
            padding: 15px 10px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e9ecef;
        }}
        
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .status-success {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .status-failure {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .image-gallery {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .image-thumbnail {{
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 4px;
            border: 2px solid #dee2e6;
            cursor: pointer;
            transition: transform 0.2s, border-color 0.2s;
        }}
        
        .image-thumbnail:hover {{
            transform: scale(1.05);
            border-color: #667eea;
        }}
        
        .test-details {{
            font-size: 0.9em;
            color: #666;
        }}
        
        .test-id {{
            font-family: monospace;
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
        }}
        
        .error-message {{
            color: #dc3545;
            font-size: 0.85em;
            font-style: italic;
        }}
        
        .duration {{
            font-weight: 600;
            color: #28a745;
        }}
        
        .no-images {{
            color: #6c757d;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .summary {{ grid-template-columns: 1fr 1fr; }}
            table {{ font-size: 0.9em; }}
            th, td {{ padding: 10px 5px; }}
            .image-thumbnail {{ width: 60px; height: 60px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 AIGC Preview API Test Results</h1>
        <p>📊 <strong>{total_tests}</strong> total tests | ✅ <strong>{successful_tests}</strong> successful | ❌ <strong>{failed_tests}</strong> failed</p>
        <p>📈 Success Rate: <strong>{success_rate:.1f}%</strong></p>
        <p>⏰ Test Period: {start_time} to {end_time}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Total Tests</h3>
            <div class="number">{total_tests}</div>
        </div>
        <div class="summary-card">
            <h3>Successful</h3>
            <div class="number success">{successful_tests}</div>
        </div>
        <div class="summary-card">
            <h3>Failed</h3>
            <div class="number failure">{failed_tests}</div>
        </div>
        <div class="summary-card">
            <h3>Success Rate</h3>
            <div class="number">{success_rate:.1f}%</div>
        </div>
    </div>
    
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Test</th>
                    <th>Status</th>
                    <th>Configuration</th>
                    <th>Input Images</th>
                    <th>Processed Images</th>
                    <th>Duration</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add table rows
        for result in results:
            status_class = "status-success" if result.get('success', False) else "status-failure"
            status_text = "✅ SUCCESS" if result.get('success', False) else "❌ FAILED"
            
            # Process input images
            input_urls = result.get('image_urls', '').split('; ') if result.get('image_urls') else []
            input_images_html = self.create_image_gallery_html(input_urls, 'Input')
            
            # Process output images  
            output_urls = result.get('processed_image_urls', '').split('; ') if result.get('processed_image_urls') else []
            output_images_html = self.create_image_gallery_html(output_urls, 'Output')
            
            # Configuration details
            config_details = f"""
                <div class="test-details">
                    <strong>Pipeline:</strong> {html.escape(result.get('pipeline_config_name', 'N/A'))}<br>
                    <strong>Location:</strong> {html.escape(result.get('location_prompt_name', 'N/A'))}<br>
                    <strong>Person:</strong> {html.escape(result.get('person_prompt_name', 'N/A'))}
                </div>
            """
            
            # Error message if failed
            error_html = ""
            if not result.get('success', False) and result.get('error_message'):
                error_html = f'<div class="error-message">Error: {html.escape(result.get("error_message", ""))}</div>'
            
            duration_html = f'<span class="duration">{result.get("duration_seconds", 0):.1f}s</span>'
            
            html_content += f"""
                <tr>
                    <td>
                        <div class="test-id">{html.escape(result.get('test_id', 'N/A'))}</div>
                        <div class="test-details">#{result.get('test_number', 'N/A')}</div>
                    </td>
                    <td>
                        <span class="status-badge {status_class}">{status_text}</span>
                    </td>
                    <td>{config_details}</td>
                    <td>{input_images_html}</td>
                    <td>{output_images_html}</td>
                    <td>{duration_html}</td>
                    <td>
                        <div class="test-details">
                            <strong>Images:</strong> {result.get('image_count', 0)} → {result.get('processed_images_count', 0)}<br>
                            <strong>Timestamp:</strong> {result.get('timestamp', 'N/A')[:19].replace('T', ' ')}
                        </div>
                        {error_html}
                    </td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <script>
        // Add click handlers for image thumbnails
        document.addEventListener('DOMContentLoaded', function() {
            const thumbnails = document.querySelectorAll('.image-thumbnail');
            thumbnails.forEach(thumbnail => {
                thumbnail.addEventListener('click', function() {
                    window.open(this.src, '_blank');
                });
            });
        });
    </script>
</body>
</html>
"""
        
        return html_content
        
    def create_image_gallery_html(self, image_urls: List[str], gallery_type: str = "") -> str:
        """Create HTML for image gallery with thumbnails."""
        if not image_urls or not any(url.strip() for url in image_urls):
            return '<div class="no-images">No images</div>'
            
        gallery_html = '<div class="image-gallery">'
        for url in image_urls:
            url = url.strip()
            if url:
                gallery_html += f'''
                    <img src="{html.escape(url)}" 
                         alt="{gallery_type} Image" 
                         class="image-thumbnail"
                         title="Click to open full size in new tab"
                         loading="lazy">
                '''
        gallery_html += '</div>'
        return gallery_html
            
    def print_summary(self):
        """Print test execution summary."""
        if not self.start_time:
            print("⚠️  No test execution data available for summary.")
            return
            
        total_duration = time.time() - self.start_time
        success_rate = (self.successful_tests / self.completed_tests * 100) if self.completed_tests > 0 else 0
        
        print("\n" + "="*60)
        print("📈 TEST EXECUTION SUMMARY")
        print("="*60)
        print(f"⏱️  Total Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        print(f"🧪 Total Tests: {self.completed_tests}/{self.total_combinations}")
        print(f"✅ Successful: {self.successful_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if self.completed_tests > 0 and self.results:
            avg_duration = sum(r['duration_seconds'] for r in self.results) / len(self.results)
            print(f"⏱️  Average Test Duration: {avg_duration:.1f} seconds")
        elif self.completed_tests == 0:
            print("⚠️  No tests were completed successfully.")
            
        print("="*60)
        
    def run_all_tests(self) -> bool:
        """Run all test combinations."""
        if not self.load_config():
            return False
            
        combinations = self.generate_test_combinations()
        if not combinations:
            print("❌ No test combinations generated!")
            return False
            
        print(f"\n🚀 Starting test execution...")
        print(f"📋 Configuration: {self.config['test_suite_name']}")
        print(f"🎯 Target: {self.config['base_url']}{self.config['endpoint']}")
        
        self.start_time = time.time()
        
        csv_filename = None
        interrupted = False
        
        try:
            for i, combination in enumerate(combinations, 1):
                result = self.run_single_test(combination, i)
                self.results.append(result)
                
                # Print progress
                progress = (i / self.total_combinations) * 100
                print(f"📊 Progress: {progress:.1f}% ({i}/{self.total_combinations})")
                
                # Handle pause after adding result to ensure it's saved
                if self.pause_after_tests:
                    print(f"   ⏸️  Test completed. Press Enter to continue to next test, 'q' to quit and save results, or 's' to skip remaining pauses...")
                    try:
                        user_input = input("   ").strip().lower()
                        if user_input == 'q':
                            print(f"   🛑 User requested to quit. Will save {len(self.results)} completed test results...")
                            raise KeyboardInterrupt()
                        elif user_input == 's':
                            print("   ⏭️  Skipping remaining pauses, continuing with full speed...")
                            self.pause_after_tests = False
                    except KeyboardInterrupt:
                        print("   🛑 User interrupted. Results will be saved...")
                        raise
                
        except KeyboardInterrupt:
            interrupted = True
            print(f"\n⚠️  Test execution interrupted by user!")
            if self.results:
                print(f"💾 Saving partial results from {len(self.results)} completed tests...")
            else:
                print("💾 No completed tests to save.")
            
        except Exception as e:
            interrupted = True
            print(f"\n❌ Unexpected error during test execution: {e}")
            traceback.print_exc()
            if self.results:
                print(f"💾 Saving partial results from {len(self.results)} completed tests...")
            
        finally:
            # Always save results and print summary
            print(f"\n📋 Saving results...")
            csv_filename = self.save_results_to_csv()
            self.print_summary()
            
            if self.results:
                if interrupted:
                    print(f"\n📁 Partial results saved to: {csv_filename}")
                    print(f"✅ {len(self.results)} test results preserved despite interruption")
                else:
                    print(f"\n📁 Complete results saved to: {csv_filename}")
                    
                # Generate HTML report if requested
                if self.generate_html:
                    html_filename = self.generate_html_report()
                    if html_filename:
                        print(f"🌐 HTML report saved to: {html_filename}")
            else:
                print(f"\n📄 Results file created: {csv_filename} (no tests completed)")
                
        return not interrupted


def generate_html_from_csv(csv_filename: str) -> None:
    """Generate HTML report from existing CSV file."""
    if not os.path.exists(csv_filename):
        print(f"❌ CSV file '{csv_filename}' not found!")
        return
        
    print(f"🌐 Generating HTML report from {csv_filename}...")
    runner = TestSuiteRunner()
    html_filename = runner.generate_html_report(csv_filename=csv_filename)
    
    if html_filename:
        print(f"✅ HTML report generated successfully!")
        print(f"📁 Open in browser: {html_filename}")
    else:
        print("❌ Failed to generate HTML report")


def main():
    """Main execution function."""
    print("🧪 AIGC Preview API Test Suite Runner")
    print("="*50)
    
    # Parse command line arguments
    config_file = "test_suite_config.json"
    pause_after_tests = False
    generate_html = False
    html_from_csv = None
    host_url = None
    
    # Simple argument parsing
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--pause" or arg == "-p":
            pause_after_tests = True
        elif arg == "--html":
            generate_html = True
        elif arg == "--html-from-csv":
            if i + 1 < len(args):
                html_from_csv = args[i + 1]
                i += 1  # Skip the next argument as it's the CSV filename
            else:
                print("❌ --html-from-csv requires a CSV filename!")
                sys.exit(1)
        elif arg == "--host":
            if i + 1 < len(args):
                host_url = args[i + 1]
                i += 1  # Skip the next argument as it's the host URL
            else:
                print("❌ --host requires a URL!")
                sys.exit(1)
        elif arg == "--help":
            print("Usage: python test_suite_runner.py [config_file] [options]")
            print("\nOptions:")
            print("  -p, --pause              Pause after each test for manual review")
            print("  --html                   Generate HTML report after tests")
            print("  --html-from-csv <file>   Generate HTML report from existing CSV file")
            print("  --host <url>             Specify custom host URL (default: localhost:8080)")
            print("  --help                   Show this help message")
            print("\nExamples:")
            print("  python test_suite_runner.py                        # Run with default config")
            print("  python test_suite_runner.py --pause                # Run with pauses")
            print("  python test_suite_runner.py --html                 # Run tests and generate HTML")
            print("  python test_suite_runner.py --host my-server.com   # Test against custom host")
            print("  python test_suite_runner.py --host https://api.example.com:3000  # Full URL")
            print("  python test_suite_runner.py --pause --html --host staging.myapp.com  # All options")
            print("  python test_suite_runner.py custom_config.json     # Use custom config")
            print("  python test_suite_runner.py --html-from-csv results.csv  # Generate HTML from existing CSV")
            sys.exit(0)
        elif not arg.startswith("-"):
            config_file = arg
        i += 1
    
    # Handle HTML generation from CSV mode
    if html_from_csv:
        generate_html_from_csv(html_from_csv)
        return
        
    if not os.path.exists(config_file):
        print(f"❌ Configuration file '{config_file}' not found!")
        print(f"Usage: python {sys.argv[0]} [config_file] [options]")
        print("Use --help for more information.")
        sys.exit(1)
        
    # Determine the health check URL
    if host_url:
        # Ensure host_url has proper format for health check
        if not host_url.startswith(('http://', 'https://')):
            health_url = f"http://{host_url}/health"
        else:
            health_url = f"{host_url}/health"
    else:
        health_url = "http://localhost:8080/health"
    
    # Check if API server is reachable
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ API server is reachable at {health_url.replace('/health', '')}")
        else:
            print(f"⚠️  API server at {health_url.replace('/health', '')} responded but not healthy")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot reach API server at {health_url.replace('/health', '')}")
        if not host_url:
            print("💡 Make sure the API server is running with: python main.py")
        else:
            print("💡 Make sure the API server is running and accessible")
        answer = input("Continue anyway? (y/N): ").lower().strip()
        if answer != 'y':
            sys.exit(1)
    except Exception as e:
        print(f"⚠️  Could not check API server status: {e}")
        
    # Show mode status
    if pause_after_tests:
        print("⏸️  Pause mode enabled - will pause after each test")
        print("   Press Enter to continue, 'q' to quit, 's' to skip remaining pauses")
    if generate_html:
        print("🌐 HTML report generation enabled")
    if host_url:
        print(f"🌐 Custom host specified: {host_url}")
    
    # Run the test suite
    runner = TestSuiteRunner(config_file, pause_after_tests, generate_html, host_url)
    completed_fully = runner.run_all_tests()
    
    if completed_fully:
        print("\n🎉 Test suite execution completed successfully!")
    else:
        print("\n⚠️  Test suite was interrupted, but results have been saved.")
        print("💡 You can review the partial results in the generated CSV file.")


if __name__ == "__main__":
    main() 