# Environment Setup Guide

## Google Cloud Configuration

Since you're using Gemini models (configured in `llm/models.yaml`), you need to set up Google Cloud authentication.

### Option 1: Set Project ID via Environment Variable

Create a `.env` file in your project root with:

```env
GOOGLE_CLOUD_PROJECT=your-project-id-here
```

Replace `your-project-id-here` with your actual Google Cloud project ID.

### Option 2: Set Project ID via gcloud CLI

```bash
gcloud config set project your-project-id-here
```

### Option 3: Set Project ID in Code (Not Recommended)

You can also set it programmatically, but environment variables are preferred.

## Authentication Methods

### Method 1: Service Account Key (Recommended for Production)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "IAM & Admin" > "Service Accounts"
3. Create a new service account or select existing one
4. Create a new key (JSON format)
5. Download the JSON file
6. Set the environment variable:

```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
```

### Method 2: Application Default Credentials (Recommended for Development)

```bash
gcloud auth application-default login
```

This will authenticate you locally and create credentials automatically.

### Method 3: Workload Identity (For Cloud Environments)

If running on Google Cloud, use Workload Identity for automatic authentication.

## Complete .env File Example

```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=my-ufc-project-123456
GOOGLE_APPLICATION_CREDENTIALS=/Users/username/Downloads/my-project-key.json

# Optional: Other AI Providers
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
XAI_API_KEY=your-xai-key
```

## Verification Steps

1. **Check your project ID:**
   ```bash
   gcloud config get-value project
   ```

2. **Verify authentication:**
   ```bash
   gcloud auth list
   ```

3. **Test Vertex AI access:**
   ```bash
   gcloud ai models list
   ```

## Troubleshooting

### "Unable to find your project" Error
- Make sure `GOOGLE_CLOUD_PROJECT` is set correctly
- Verify the project ID exists and you have access
- Check that authentication is working

### "Permission denied" Error
- Ensure your service account has the necessary roles:
  - `roles/aiplatform.user`
  - `roles/aiplatform.developer`
- Or use a service account with broader access for testing

### "Invalid credentials" Error
- Regenerate your service account key
- Make sure the JSON file path is correct
- Verify the file has proper permissions

## Quick Setup Commands

```bash
# Set project ID
export GOOGLE_CLOUD_PROJECT=your-project-id

# Authenticate (choose one)
gcloud auth application-default login
# OR
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Test the setup
python ufc_fight_sheet.py
``` 