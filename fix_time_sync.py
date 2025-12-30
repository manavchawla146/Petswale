"""
This script provides instructions to fix the Google OAuth time sync issue.
"""

print("""
=== GOOGLE OAUTH TIME SYNC FIX ===

The Google OAuth login is failing because your system clock is set to December 29, 2025,
which is in the future. Google OAuth tokens have strict timestamp validation.

SOLUTIONS:

1. MANUAL TIME SET (Recommended):
   - Right-click on the clock in your taskbar
   - Select "Adjust date/time"
   - Turn off "Set time automatically" if it's on
   - Set the correct date and time (should be around December 2024, not 2025)
   - Turn "Set time automatically" back on
   - Click "Sync now" to sync with time servers

2. COMMAND LINE (Admin PowerShell):
   Run PowerShell as Administrator and execute:
   ```
   net start w32time
   w32tm /resync
   ```

3. TEMPORARY WORKAROUND:
   If you can't fix the time immediately, you can:
   - Use email/password login instead of Google OAuth
   - Create a test user account with email: test@example.com, password: test123

4. GOOGLE CONSOLE CHECK:
   Ensure your Google OAuth app settings are correct:
   - Go to: https://console.cloud.google.com/
   - Navigate to APIs & Services > Credentials
   - Check that your OAuth 2.0 Client ID is configured for "Web application"
   - Verify the authorized redirect URIs include: http://127.0.0.1:5000/auth/google_login

After fixing the time, restart the Flask app and try Google login again.

Current system time shows: December 29, 2025 (FUTURE DATE)
Correct time should be: December 2024 (CURRENT DATE)
""")

# Check if we can import datetime to show the issue
import datetime
import time

current_system_time = datetime.datetime.now()
unix_timestamp = int(time.time())

print(f"\nCurrent system time: {current_system_time}")
print(f"Unix timestamp: {unix_timestamp}")
print(f"This timestamp is causing the OAuth validation to fail.")
