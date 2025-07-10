# Strava to Calendar Automation

🏃‍♂️ Automatically sync your Strava workout activities to Google Calendar and remove overlapping planned events.

## Security Notice

This project handles sensitive authentication tokens. **Never commit credentials to version control.** Follow the security guidelines below.

## Features

- 📅 **Auto-sync**: Creates calendar events for Strava activities
- 🗑️ **Smart cleanup**: Removes overlapping planned events
- 🔄 **Token refresh**: automatically handles expired credentials
- 🌏 **Timezone aware**: Proper timezone handling for events
- 🛡️ **Error handling**: Graceful handling of API failures

## Setup

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd calendar_automation_strava
pip install -r requirements.txt
```

### 2. Strava API Setup

1. Create a Strava app at [developers.strava.com](https://developers.strava.com)
2. Run the token setup script:
   ```bash
   python get_strava_token.py
   ```
3. Follow the prompts to get your tokens

### 3. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google Calendar API
3. Create OAuth 2.0 credentials
4. Download credentials as `credentials/credentials.json`
5. Run authorization:
   ```bash
   python authorize_google.py
   ```
   
   **Note:** This script will:
   - Create `credentials/token.json` for local development
   - Display the token content for setting up the `GOOGLE_CREDENTIALS` secret in GitHub Actions

### 4. Environment Variables

Create a `.env` file with:

```env
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
STRAVA_REFRESH_TOKEN=your_strava_refresh_token
GOOGLE_CALENDAR_ID=your_google_calendar_id
```

### 5. Test Run

```bash
python main.py
```

## GitHub Actions Setup

For automated daily sync:

### Repository Secrets

Add these secrets to your GitHub repository:

- `STRAVA_CLIENT_ID`: Your Strava app client ID
- `STRAVA_CLIENT_SECRET`: Your Strava app client secret  
- `STRAVA_REFRESH_TOKEN`: Your Strava refresh token
- `GOOGLE_CALENDAR_ID`: Your Google Calendar ID
- `GOOGLE_CREDENTIALS`: Contents of your `credentials/token.json` file

### Schedule

The workflow runs daily at 11 AM Melbourne time (1 AM UTC).

## Security Best Practices

### ✅ DO:
- Use environment variables for secrets
- Keep credentials in `.env` file locally
- Use GitHub Secrets for automation
- Regenerate tokens if compromised

### ❌ DON'T:
- Commit `.env` files
- Commit `credentials/` directory
- Share tokens in logs or messages
- Hard-code credentials in source code

## Files to Keep Private

These files contain sensitive data and are automatically ignored by git:

- `.env` - Environment variables
- `credentials/token.json` - Google OAuth tokens
- `credentials/credentials.json` - Google OAuth app credentials

## Troubleshooting

### Common Issues

1. **"Missing environment variables"**
   - Ensure all required variables are set in `.env`

2. **"Google credentials not found"**
   - For local development: Run `python authorize_google.py` first
   - For GitHub Actions: Ensure `GOOGLE_CREDENTIALS` secret is set correctly

3. **"Invalid credentials"**
   - Tokens may be expired; re-run authorization
   - For GitHub Actions: Update the `GOOGLE_CREDENTIALS` secret with fresh credentials

4. **"No activities found"**
   - Check Strava API permissions and date range

### Debug Mode

Use the debug script to check overlap detection:

```bash
python debug_overlap_check.py
```

## How It Works

1. **Fetch Activities**: Gets recent Strava activities (last 3 days)
2. **Fetch Events**: Gets calendar events from same time period
3. **Find Overlaps**: Identifies overlapping events using time ranges
4. **Delete Duplicates**: Removes matched planned events
5. **Create Events**: Adds new events for Strava activities

## API Rate Limits

- **Strava**: 100 requests per 15 minutes, 1000 per day
- **Google Calendar**: 1000 requests per 100 seconds per user

Running once daily is well within these limits.

## License

This project is for personal use. Ensure you comply with Strava and Google's terms of service. 