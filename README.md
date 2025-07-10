# Strava to Google Calendar Automation

🏃‍♂️ **Automatically sync your Strava activities to Google Calendar and remove overlapping planned events.**

This project runs daily via GitHub Actions to:
- Fetch your recent Strava activities (last 3 days)
- Create calendar events for completed workouts
- Remove any overlapping planned events to avoid duplicates

## ✨ **Features**

- **🔄 Automated sync**: Runs daily at 2:05 PM Melbourne time
- **📅 Smart scheduling**: Creates events with proper duration and timing
- **🗑️ Duplicate cleanup**: Removes overlapping planned events
- **⚡ Zero maintenance**: Set it once, runs forever
- **🌏 Timezone aware**: Handles timezones correctly

## 🚀 **Setup Instructions**

### 1. **Fork This Repository**
Click the "Fork" button at the top of this page to create your own copy.

### 2. **Get Strava API Credentials**
1. Go to [Strava Developer Console](https://developers.strava.com/)
2. Create a new application
3. Note down your **Client ID** and **Client Secret**
4. Get your **Refresh Token**:
   - Use the authorization URL: `https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all`
   - Replace `YOUR_CLIENT_ID` with your actual client ID
   - Authorize and copy the `code` from the redirect URL
   - Run this command to get your refresh token:
   ```bash
   curl -X POST https://www.strava.com/oauth/token \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET \
     -d code=YOUR_CODE \
     -d grant_type=authorization_code
   ```

### 3. **Get Google Calendar API Credentials**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Run the authorization process:
   ```bash
   # Clone your forked repository locally
   git clone https://github.com/YOUR_USERNAME/strava_google_calendar_automation.git
   cd strava_google_calendar_automation
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Place your credentials.json in the credentials/ folder
   # Run authorization (this will open a browser)
   python authorize_google.py
   ```
7. Copy the complete JSON output from the authorization script

### 4. **Get Your Google Calendar ID**
1. Go to [Google Calendar](https://calendar.google.com/)
2. Find the calendar you want to use
3. Click the three dots → Settings and sharing
4. Copy the **Calendar ID** (usually ends with `@group.calendar.google.com`)

### 5. **Configure GitHub Secrets**
In your forked repository, go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `STRAVA_CLIENT_ID` | Your Strava app client ID | `12345` |
| `STRAVA_CLIENT_SECRET` | Your Strava app client secret | `abc123def456...` |
| `STRAVA_REFRESH_TOKEN` | Your Strava refresh token | `xyz789uvw012...` |
| `GOOGLE_CALENDAR_ID` | Your Google Calendar ID | `user@gmail.com` or `xyz@group.calendar.google.com` |
| `GOOGLE_CREDENTIALS` | Complete JSON from step 3 | `{"token": "ya29...", "refresh_token": "1//...", ...}` |

### 6. **Test the Automation**
1. Go to **Actions** tab in your repository
2. Click on **"Sync Strava to Calendar"**
3. Click **"Run workflow"** to test immediately
4. Check the logs to ensure everything works

## 📅 **How It Works**

1. **Daily Schedule**: GitHub Actions runs the sync at 11 AM Melbourne time (1 AM UTC)
2. **Activity Fetch**: Gets your Strava activities from the last 3 days
3. **Event Creation**: Creates calendar events with format: `"Activity Type – Activity Name"`
4. **Duplicate Removal**: Finds and removes any overlapping planned events
5. **Smart Timing**: Events are created with proper start time and duration

## 🔧 **Customization**

### Change Schedule
Edit `.github/workflows/sync-calendar.yml` and modify the cron expression:
```yaml
schedule:
  - cron: '0 1 * * *'  # Daily at 1 AM UTC (11 AM Melbourne)
```

### Modify Lookback Period
In `strava.py`, change the days to look back:
```python
since = int((datetime.utcnow() - timedelta(days=3)).timestamp())  # Change 3 to your preference
```

### Event Title Format
In `gcal.py`, modify the event summary format:
```python
'summary': f"{activity['type']} – {activity['name']}"  # Customize this line
```

## 🐛 **Troubleshooting**

**"No activities found"**
- Check your Strava API permissions include `activity:read_all`
- Verify your refresh token is valid

**"Calendar not found"**
- Double-check your Google Calendar ID
- Ensure the calendar exists and is accessible

**"Authentication failed"**
- Verify all GitHub secrets are set correctly
- Check if tokens have expired (Google tokens auto-refresh)

## 📊 **Manual Run**

To run the sync manually:
1. Go to your repository's **Actions** tab
2. Select **"Sync Strava to Calendar"**
3. Click **"Run workflow"**

## 🎯 **What Gets Synced**

- **Activities**: All Strava activities from the last 3 days
- **Event Duration**: Based on your actual activity duration
- **Timezone**: Automatically handled and converted to UTC
- **Overlap Detection**: Removes planned events that overlap with actual activities

That's it! Your Strava activities will now automatically appear in your Google Calendar. 🎉 
