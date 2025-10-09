# AI Image Edit

AI Image Edit is a powerful workflow tool that uses artificial intelligence to edit and transform images according to your text instructions. Whether you want to change objects, modify scenes, or apply creative transformations, this tool makes complex image editing accessible to everyone.

## Features

### 🖼️ Intelligent Image Processing
- **Main Image Processing**: Upload your primary image that needs editing
- **Reference Image Support**: Add reference images to guide the AI transformation
- **Multiple Image Input**: Process multiple images at once for batch operations
- **Smart Text Translation**: Automatically translates Chinese descriptions to English for better AI understanding
- **Image Upscaling**: Enhance image resolution and quality with AI-powered upscaling technology

### 🤖 Multiple AI Models
Choose from different AI models based on your needs:

- **nano-banana/edit**: Fast and efficient for general image editing tasks
- **flux-pro/kontext**: Advanced model for complex transformations and higher quality results

### 💾 Flexible Output Options
- **Custom Save Location**: Choose where to save your edited images
- **Automatic Storage**: Images are automatically saved to the workspace storage
- **Format Support**: Works with JPG, PNG, WebP, and JPEG formats

## How It Works

### The AI Image Edit Block

The core functionality is provided by the **Edit Block**, which processes your images through these steps:

1. **Image Input**: Upload one or more images (main image required, additional images optional)
2. **Description**: Provide a text description of how you want the image modified
3. **Model Selection**: Choose the appropriate AI model for your task
4. **Processing**: The AI analyzes your images and text to create the desired transformation
5. **Output**: Receive your edited image with a preview

### The Image Upscale Block

The **Image Upscale Block** enhances image quality through AI-powered upscaling:

1. **Image Input**: Provide the URL of the image you want to upscale
2. **AI Processing**: Advanced algorithms analyze and enhance the image resolution
3. **Output**: Receive a higher quality, upscaled version of your image

### Input Parameters

#### Edit Block Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **Main Image** | File | Yes | The primary image you want to edit (JPG, PNG, WebP, JPEG) |
| **Sub Image** | File | No | Reference image to guide the transformation |
| **Other Images** | File Array | No | Additional reference images |
| **Prompt** | Text | Yes | Description of the desired image transformation |
| **Model** | Selection | Yes | Choose between `nano-banana/edit` or `flux-pro/kontext` |
| **Output File** | Save Path | No | Custom location to save the result (optional) |

#### Image Upscale Block Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **Image URL** | String | Yes | URL of the image to upscale |

### Output

- **Edit Block**: Returns an array of processed image file paths that you can use in subsequent steps or download
- **Image Upscale Block**: Returns the URL of the upscaled image

## Usage Examples

### Basic Image Transformation
```
Main Image: photo-of-person.jpg
Prompt: "Change the person's shirt to a red color"
Model: nano-banana/edit
```

### Style Transfer with Reference
```
Main Image: landscape.jpg
Sub Image: artistic-style-reference.jpg
Prompt: "Apply the artistic style from the reference image to the landscape"
Model: flux-pro/kontext
```

### Object Replacement
```
Main Image: room-interior.jpg
Prompt: "Replace the sofa with a modern leather couch"
Model: nano-banana/edit
```

### Image Quality Enhancement
```
Image URL: https://example.com/low-res-photo.jpg
Block: Image Upscale
Output: High-resolution upscaled version
```

## Workflow Integration

### AI Image Edit Subflow

The project includes a pre-built subflow that combines:

1. **Text Translation**: Automatically translates Chinese prompts to English using an LLM
2. **Image Processing**: Applies the Edit Block with optimized settings
3. **Result Preview**: Displays the processed image for immediate review

### Input Parameters for Subflow:
- **Main Image**: Primary image file
- **Sub Image**: Optional reference image
- **Other Images**: Optional additional images
- **Description**: Text description (supports Chinese with automatic translation)
- **Model**: AI model selection
- **Output File**: Optional custom save location

## Getting Started

### Prerequisites
- Node.js and npm installed
- Python with Poetry for dependency management
- OOMOL platform environment

### Installation
```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
poetry install --no-root
```

### Basic Usage

1. **Upload Your Image**: Select the main image you want to edit
2. **Describe the Change**: Write a clear description of what you want to modify
3. **Choose a Model**: Select the AI model that best fits your needs
4. **Run the Workflow**: Execute the process and wait for results
5. **Download Result**: Save the edited image to your desired location

## Model Recommendations

### When to Use nano-banana/edit:
- Quick edits and modifications
- Simple object replacements
- Color adjustments
- Basic transformations
- Faster processing time needed

### When to Use flux-pro/kontext:
- Complex scene modifications
- High-quality artistic transformations
- Detailed style transfers
- Professional-grade results
- When processing time is less critical

## Tips for Best Results

### Writing Effective Prompts:
- Be specific and clear about what you want to change
- Mention colors, styles, or specific objects
- Use descriptive language
- Include context about the desired outcome

### Image Preparation:
- Use high-quality source images
- Ensure good lighting and clarity
- Consider the complexity of your requested changes
- Provide reference images when helpful

### Model Selection:
- Start with nano-banana/edit for simple tasks
- Use flux-pro/kontext for complex or artistic transformations
- Test both models to see which works better for your specific use case

## Technical Details

- **Supported Formats**: JPG, PNG, WebP, JPEG
- **Processing**: Asynchronous with status polling
- **Storage**: Uses OOMOL storage system (`/oomol-driver/oomol-storage/`)
- **Preview**: Automatic image preview after processing
- **Error Handling**: Comprehensive error handling and validation

## Troubleshooting

### Common Issues:
- **File not found**: Ensure image files exist at specified paths
- **Model errors**: Check if the selected model is available
- **Timeout issues**: Try reducing image size or complexity
- **Format errors**: Verify image formats are supported

### Getting Help:
- Check the workflow logs for detailed error messages
- Ensure all input parameters are correctly configured
- Verify network connectivity for AI model access
- Review the prompt clarity and specificity

## License

This project is available under the repository license. See the [GitHub repository](https://github.com/oomol-flows/ai-image-edit.git) for more details.

## Contributing

Contributions are welcome! Please visit the [GitHub repository](https://github.com/oomol-flows/ai-image-edit.git) to submit issues or pull requests.