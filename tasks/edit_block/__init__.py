#region generated meta
import typing
class Inputs(typing.TypedDict):
    main_image: str
    reference_image: str | None
    prompt: str
    model: typing.Literal["flux-pro/kontext", "nano-banana/edit"]
    output_file: str | None
class Outputs(typing.TypedDict):
    image: typing.NotRequired[str]
#endregion

import os
import requests
import json
import time
from typing import Any
from oocana import Context
import tempfile


async def main(params: Inputs, context: Context) -> Outputs:
    console_api_url = "https://llm.oomol.com"
    api_key: Any = await context.oomol_token()
    main_image = params["main_image"]
    reference_image = params.get("reference_image")
    prompt = params["prompt"]
    model = params.get("model", "nano-banana/edit")

    # 合并所有图像文件
    file_paths = [main_image]
    if reference_image:
        file_paths.append(reference_image)

    # 构建包含图像角色信息的增强prompt
    enhanced_prompt = prompt
    if len(file_paths) > 1:
        image_descriptions = []
        image_descriptions.append("Image 1: main image")
        image_descriptions.append("Image 2: reference image")

        enhanced_prompt = f"{prompt}\n\nImage descriptions:\n" + "\n".join(image_descriptions)
    
    # Validate input files exist
    if not file_paths or len(file_paths) == 0:
        raise ValueError("At least one input file is required")
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    # Validate model selection
    supported_models = ["nano-banana/edit", "flux-pro/kontext"]
    if model not in supported_models:
        raise ValueError(f"Unsupported model: {model}. Supported models: {supported_models}")
    
    headers = {
        'Authorization': f"Bearer {api_key}",
    }
    
    try:
        # Step 1: Initiate the task with POST request
        
        initiate_url = console_api_url + "/api/tasks/fal/images/process"
        
        files_array = []
        fileKey = "file"
        if model == "nano-banana/edit":
            fileKey = "files"

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_format = os.path.splitext(file_name)[1]
            files_array.append((fileKey, (file_name, open(file_path, 'rb'), f'image/{file_format[1:]}')))

        data = {
            'prompt': enhanced_prompt,
            'model': model
        }
        
        response = requests.post(
            initiate_url, 
            files=files_array, 
            data=data, 
            headers=headers, 
            timeout=120
        )
        response.raise_for_status()
        
        # nano-banana/edit 模型是直接返回结果，不需要查询进度
        if model =="nano-banana/edit":
            result_data = response.json()
        else :
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