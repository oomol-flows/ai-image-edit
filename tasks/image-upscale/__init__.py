from oocana import Context
import requests
import time

#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_url: str
class Outputs(typing.TypedDict):
    upscaled_image_url: typing.NotRequired[str]
#endregion

def main(params: Inputs, context: Context) -> Outputs | None:
    image_url = params.get("image_url")
    if not image_url:
        raise ValueError("image_url is required")
    
    # Step 1: Start upscale task
    start_url = "https://console.oomol.com/api/tasks/fal/images/upscale/start"
    start_payload = {"image_url": image_url}

    api_key: Any = context.oomol_llm_env.get("api_key")
    headers = {
        'Authorization': f"Bearer {api_key}",
    }
    
    try:
        start_response = requests.post(start_url, json=start_payload,headers=headers)
        start_response.raise_for_status()
        request_id = start_response.json().get("request_id")
        
        if not request_id:
            raise ValueError("No request_id received from start task")
        
        # Step 2: Check task status
        status_url = f"https://console.oomol.com/api/tasks/fal/images/upscale/status/{request_id}"
        
        while True:
            status_response = requests.get(status_url,headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            task_status = status_data.get("data", {}).get("status")
            
            if task_status == "COMPLETED":
                break
            elif task_status == "FAILED":
                raise ValueError(f"Task failed for request_id: {request_id}")
            else:
                # Wait 5 seconds before next check
                time.sleep(5)
        
        # Step 3: Get result
        result_url = f"https://console.oomol.com/api/tasks/fal/images/upscale/result/{request_id}"
        result_response = requests.get(result_url,headers=headers)
        result_response.raise_for_status()
        result_data = result_response.json()
        
        output_image_url = result_data.get("data", {}).get("image", {}).get("url")
        
        if not output_image_url:
            raise ValueError("No output image URL received")
        
        return {
            "upscaled_image_url": output_image_url
        }
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Task failed: {str(e)}")
