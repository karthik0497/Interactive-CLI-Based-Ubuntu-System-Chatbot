*   **Infrastructure**: I run on Google's internal, enterprise-grade infrastructure.
*   **Access**: I do not use a public API key. I have direct access to the models via internal systems.
*   **Limits**: My usage is not subject to the public "Free Tier" rate limits you are seeing.

## 2. Your Chatbot (The Code We Wrote)
Your Python script connects to Google's public **Gemini API**.
*   **Authentication**: It uses the `GEMINI_API_KEY` you created.
*   **Plan**: You are likely on the **"Spark" (Free) tier**.
*   **Limits**: The Free tier has strict limits (Rate Limits).
    *   Example: You can only make ~15 requests per minute (RPM).
    *   **The Issue**: When you start the app, it runs multiple calls (checking models, sending system prompt). This bursts through your limit quickly, causing the `429 Quota Exceeded` error.

## The Fix
I have updated your code to be "gentler" on the API:
1.  **Skip Model Listing**: I removed the check that lists all models (this saves 1 expensive API call on startup).
2.  **Hardcode Best Model**: I saw in your logs that you have `gemini-2.5-flash`, so I will set that as the default directly.
3.  **Crash Protection**: If the AI is tired (Rate Limit), the app will simply start in "Quiet Mode" rather than crashing.

You can try running `python3 main.py` again. It should be much more stable now!
