# Telegram Cleaner Bot

A Python script that automatically deletes recent messages from a Telegram group using the Telethon library.

## Features

- 🔥 **Complete Group Cleaner** - Deletes ALL messages from first to last
- 🔗 Connects to Telegram using your API credentials  
- 📥 Fetches up to 10,000 messages (configurable)
- 🎯 No time restrictions - cleans entire group history
- ⚡ Handles supergroups, channels, and regular groups
- 🔄 Batch deletion with rate limiting protection
- ✅ Safe confirmation prompts before deletion
- 🛡️ Admin permission checking and error handling

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Telegram API credentials:**
   - Go to https://my.telegram.org/auth
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application to get your `api_id` and `api_hash`

3. **Configure the script:**
   Open `delete_bot.py` and fill in these values:
   ```python
   api_id = 12345678                    # Your API ID (integer, remove quotes)
   api_hash = 'your_api_hash_here'      # Your API hash (string)
   phone_number = '+1234567890'         # Your phone number with country code
   target_chat = -1001234567890         # Chat ID (integer) or '@username'
   ```

   **⚠️ Important Notes:**
   - `api_id` should be an **integer** (no quotes)
   - `target_chat` can be either:
     - Chat ID: `-1001234567890` (integer, no quotes)
     - Username: `'@groupname'` (string, with quotes)
   - Use [@userinfobot](https://t.me/userinfobot) to get your Chat ID

## Usage

1. **Run the script:**
   ```bash
   python delete_bot.py
   ```

2. **First-time authentication:**
   - The script will ask for your phone number (if not configured)
   - Enter the verification code sent to your Telegram app
   - A session file will be created for future runs

3. **Message deletion:**
   - The script will show how many messages will be deleted
   - Confirm the deletion when prompted
   - Monitor the progress as messages are deleted in batches

## Important Notes

⚠️ **Safety Considerations:**
- Only messages you sent OR messages in groups where you're an admin can be deleted
- Messages are permanently deleted and cannot be recovered
- The script includes confirmation prompts to prevent accidental deletion
- Rate limiting is handled to avoid Telegram API restrictions

🔧 **Configuration Options:**
- `MESSAGE_LIMIT`: Number of messages to fetch (default: 10,000)
- `BATCH_SIZE`: Number of messages to delete per API request (max 100)
- No time restrictions - deletes ALL messages found

## Troubleshooting

- **"Admin rights required"**: You need admin rights to delete others' messages
- **Rate limiting**: The script automatically handles rate limits with delays
- **Chat not found**: Make sure the chat username/ID is correct and you're a member
- **Authentication errors**: Delete the session file and re-authenticate

## Files

- `delete_bot.py` - Main script
- `requirements.txt` - Python dependencies
- `telegram_cleaner_session.session` - Session file (created automatically)

## Disclaimer

Use this script responsibly. Make sure you have permission to delete messages in the target group. The authors are not responsible for any misuse of this tool. 
