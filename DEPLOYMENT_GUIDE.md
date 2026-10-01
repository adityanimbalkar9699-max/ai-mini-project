# AuraMed Clinical AI // Cloud Deployment Manual

This platform is 100% cloud-ready. You can deploy it live on the internet (not just localhost) completely free within 3 minutes using any of the following modern cloud options:

---

## Option 1: Render.com (Recommended — 100% Free & Automatic)

Render is the simplest cloud platform for Python Flask apps.

### Step-by-Step Instructions:
1. **Initialize Git & Push to GitHub**:
   Open PowerShell in your project folder `S:\ai mini project`:
   ```powershell
   git init
   git add .
   git commit -m "Deploy AuraMed Clinical AI to Cloud"
   ```
   Create a new repository on [GitHub](https://github.com/new) (e.g. `auramed-clinical-ai`), then push your code:
   ```powershell
   git remote add origin https://github.com/<your-username>/auramed-clinical-ai.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com/) and sign in with GitHub.
   - Click **"New +"** -> **"Web Service"**.
   - Select your GitHub repository (`auramed-clinical-ai`).
   - Render will automatically detect `render.yaml` or you can enter:
     - **Name**: `auramed-clinical-ai`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4`
     - **Instance Type**: `Free`
   - Click **"Create Web Service"**.

3. **Done!**
   In about 2 minutes, Render will build and deploy your app. You will receive a permanent live HTTPS URL like:
   `https://auramed-clinical-ai.onrender.com`

---

## Option 2: Railway.app (Free / Instant)

Railway deploys straight from GitHub or directly from your terminal:

1. Sign in to [Railway.app](https://railway.app/).
2. Click **"New Project"** -> **"Deploy from GitHub repo"**.
3. Select your repository.
4. Railway automatically detects the `Procfile` and `requirements.txt`, provisions a container, and provides an active public domain under Settings -> Domains.

---

## Option 3: Google Cloud Run (Serverless Docker Container)

If you have a Google Cloud account:

1. Build and submit your container image:
   ```powershell
   gcloud builds submit --tag gcr.io/<YOUR-PROJECT-ID>/auramed-ai
   ```
2. Deploy to Cloud Run with public unauthenticated access:
   ```powershell
   gcloud run deploy auramed-ai \
     --image gcr.io/<YOUR-PROJECT-ID>/auramed-ai \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```
3. Cloud Run will output your live URL (e.g. `https://auramed-ai-xyz-uc.a.run.app`).

---

## Option 4: Local Docker Run (Verify Container Locally)

You can also run the exact cloud container on your local machine using Docker Desktop:

1. Build the Docker image:
   ```powershell
   docker build -t auramed-clinical-ai .
   ```
2. Run the container:
   ```powershell
   docker run -p 5000:5000 -e PORT=5000 auramed-clinical-ai
   ```
3. Open `http://localhost:5000` in your browser.

---

## Healthcheck & Monitoring
Once deployed, verify your service is operational by opening:
- `https://<YOUR-APP-URL>/health`

It should return:
```json
{
  "status": "healthy",
  "service": "AI Clinical Decision Support Expert System",
  "version": "2.4.0-cloud",
  "rules_loaded": 12,
  "engine": "Symbolic Logic (Forward & Backward Chaining)"
}
```
