# region generated meta
import typing

class Inputs(typing.TypedDict):
    file: str
    prompt: str
    output_file: str

class Outputs(typing.TypedDict):
    images: typing.List[str]
# endregion

import os
import requests
import json
import time
from typing import List, Dict, Any
from oocana import Context
import tempfile


def main(params: Inputs, context: Context) -> Outputs:
    """
    Main function to process image using FAL API with three-step process:
    1. Initiate task with POST request
    2. Poll status until completed
    3. Fetch result and download image
    """
    
    # Get API configuration from environment
    console_api_url = context.oomol_llm_env.get("base_url")
    api_key: Any = context.oomol_llm_env.get("api_key")
    
    file_path = params["file"]
    prompt = params["prompt"]
    
    # Validate input file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    headers = {
        'Authorization': f"Bearer {api_key}",
    }
    
    try:
        # Step 1: Initiate the task with POST request
        
        initiate_url = console_api_url + "/api/tasks/fal/images/process"
        
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f)
            }
            data = {
                'prompt': prompt
            }
            
            response = requests.post(
                initiate_url, 
                files=files, 
                data=data, 
                headers=headers, 
                timeout=120
            )
            response.raise_for_status()
        
        # Parse response to get request_id
        result_data = response.json()
        if 'request_id' not in result_data:
            raise ValueError("Invalid API response format: missing request_id")
        
        request_id = result_data['request_id']
        print(f"Task initiated successfully. Request ID: {request_id}")
        
        # Step 2: Poll status until completed
        
        status_url = console_api_url + f"/api/tasks/fal/status/{request_id}"
        max_retries = 60  # Maximum 5 minutes (60 * 5 seconds)
        retry_count = 0
        
        while retry_count < max_retries:
            status_response = requests.get(status_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            if 'data' not in status_data or 'status' not in status_data['data']:
                raise ValueError("Invalid status response format")
            
            status = status_data['data']['status']
            
            if status == "COMPLETED":
                print("Task completed successfully!")
                break
            elif status == "FAILED":
                raise Exception("Task failed during processing")
            elif status in ["PENDING", "IN_PROGRESS"]:
                # Still processing, wait and retry
                retry_count += 1
                print(f"Task status: {status}, waiting... ({retry_count}/{max_retries})")
                time.sleep(5)  # Wait 5 seconds before next poll
            else:
                raise Exception(f"Unknown task status: {status}")
        
        if retry_count >= max_retries:
            raise Exception("Task timeout: maximum polling time exceeded")
        
        # Step 3: Fetch the result
        result_url = console_api_url + f"/api/tasks/fal/result/{request_id}"
        result_response = requests.get(result_url, headers=headers, timeout=30)
        result_response.raise_for_status()
        
        result_data = result_response.json()
        if 'data' not in result_data or 'images' not in result_data['data']:
            raise ValueError("Invalid result response format")
        
        images = result_data['data']['images']
        if not isinstance(images, list) or len(images) == 0:
            raise ValueError("No images found in result")
        
        # Get the first image URL
        first_image = images[0]
        if isinstance(first_image, dict) and 'url' in first_image:
            image_url = first_image['url']
        elif isinstance(first_image, str):
            image_url = first_image
        else:
            raise ValueError(f"Invalid image format: {first_image}")
        
        # Download the image
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()
        
        # Determine output file path
        output_file_path = params.get("output_file")
        if output_file_path:
            # Use provided output file path
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'wb') as f:
                f.write(image_response.content)
            saved_file_path = output_file_path
        else:
            # Save to temporary file
            file_extension = os.path.splitext(image_url)[1] or '.jpg'
            temp_file = tempfile.NamedTemporaryFile(
                suffix=file_extension, 
                delete=False,
                dir="/oomol-driver/oomol-storage"
            )
            temp_file.write(image_response.content)
            temp_file.close()
            saved_file_path = temp_file.name
        
        # Preview the downloaded image
        context.preview({
            "type": "image",
            "data": image_url
        })
        
        return {"image": saved_file_path}
        
    except requests.exceptions.Timeout:
        raise Exception("Request timeout, please check network connection")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON response from API")
    except Exception as e:
        raise Exception(f"Processing error: {str(e)}")