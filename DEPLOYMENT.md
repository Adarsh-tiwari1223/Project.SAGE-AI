# SAGE AI Deployment Guide

## 🚀 Deploying on Render

### Prerequisites
- GitHub repository with your SAGE AI project
- Render account

### Steps

1. **Fork/Clone the Repository**
   - Make sure your repository is on GitHub

2. **On Render Dashboard**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the Service**
   - **Name**: `sage-ai` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements-deploy.txt`
   - **Start Command**: `python app.py`

4. **Environment Variables**
   Add these in Render dashboard:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   NEWS_API_KEY=your_news_api_key_here
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app

### Important Notes

- **Voice Features**: Not available on cloud deployment (no microphone access)
- **Web Interface**: Fully functional with text-based chat
- **Dependencies**: Uses `requirements-deploy.txt` (excludes PyAudio and pyttsx3)

### Local Development vs Deployment

| Feature | Local | Cloud Deployment |
|---------|-------|------------------|
| Voice Commands | ✅ Yes | ❌ No |
| Text-to-Speech | ✅ Yes | ❌ No |
| Web Interface | ✅ Yes | ✅ Yes |
| AI Chat | ✅ Yes | ✅ Yes |
| Weather | ✅ Yes | ✅ Yes |
| News | ✅ Yes | ✅ Yes |

### Troubleshooting

If deployment fails:
1. Check that `requirements-deploy.txt` is used (not `requirements.txt`)
2. Verify environment variables are set
3. Ensure `app.py` imports from `main-deploy.py` 