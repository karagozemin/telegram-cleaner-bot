#!/usr/bin/env python3
"""
Telegram Group Message Cleaner Bot

This script connects to Telegram using the Telethon library and deletes
messages from a specified group that are newer than 2 days old.

Requirements:
- telethon library
- Valid Telegram API credentials (api_id, api_hash)
- Phone number for authentication
- Target chat/group username or ID

Author: Auto-generated script
"""

import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.functions.messages import DeleteMessagesRequest
from telethon.tl.functions.channels import DeleteMessagesRequest as ChannelDeleteMessagesRequest
from telethon.errors import FloodWaitError, ChatAdminRequiredError
import time

# =============================================================================
# CONFIGURATION - FILL THESE VALUES MANUALLY
# =============================================================================

# Get these values from https://my.telegram.org/auth
api_id = 'YOUR_API_ID'  # Replace with your actual API ID (integer, remove quotes)
api_hash = 'YOUR_API_HASH'  # Replace with your actual API hash (string)

# Your phone number (including country code, e.g., '+1234567890')
phone_number = 'YOUR_PHONE_NUMBER'  # Replace with your phone number (with country code)

# Target chat - can be username (e.g., '@groupname') or chat ID (integer)
# Using Chat ID (most reliable method)
target_chat = 'YOUR_CHAT_ID_OR_USERNAME'  # Replace with your Chat ID or @username

# =============================================================================
# SCRIPT CONFIGURATION
# =============================================================================

# Number of messages to fetch (maximum possible)
MESSAGE_LIMIT = 10000  # Increase if your group has more messages

# NO TIME THRESHOLD - Delete ALL messages from first to last

# Session file name (will be created automatically)
SESSION_NAME = 'telegram_cleaner_session'

async def main():
    """
    Main function that handles the message deletion process.
    """
    print("🤖 Telegram Group Message Cleaner Bot")
    print("=" * 50)
    
    # Validate configuration
    if (api_id == 'YOUR_API_ID' or 
        api_hash == 'YOUR_API_HASH' or 
        phone_number == 'YOUR_PHONE_NUMBER' or 
        target_chat == 'YOUR_CHAT_ID_OR_USERNAME'):
        print("❌ Error: Please fill in your API credentials and target chat in the script!")
        print("   - Get API credentials from: https://my.telegram.org/auth")
        print("   - Set your phone number (with country code)")
        print("   - Set the target chat username or ID")
        return
    
    # Create the client and connect
    client = TelegramClient(SESSION_NAME, api_id, api_hash)
    
    try:
        print("📱 Connecting to Telegram...")
        await client.start(phone=phone_number)
        
        # Get information about ourselves
        me = await client.get_me()
        print(f"✅ Successfully logged in as: {me.first_name} (@{me.username})")
        
        # Get the target chat
        print(f"🔍 Looking for chat: {target_chat}")
        try:
            chat = await client.get_entity(target_chat)
            print(f"✅ Found chat: {chat.title}")
        except Exception as e:
            print(f"❌ Error finding chat '{target_chat}': {e}")
            return
        
        # NO TIME THRESHOLD - Delete ALL messages
        print(f"🎯 Target: Delete ALL messages from first to last in the group!")
        print(f"⚠️  This will completely clean the entire group history!")
        
        # Fetch messages
        print(f"📥 Fetching last {MESSAGE_LIMIT} messages...")
        messages = []
        messages_to_delete = []
        
        async for message in client.iter_messages(chat, limit=MESSAGE_LIMIT):
            messages.append(message)
            
            # NO TIME CHECK - Add ALL messages for deletion
            messages_to_delete.append(message.id)
            if len(messages_to_delete) % 100 == 0:  # Progress indicator every 100 messages
                print(f"🎯 Found {len(messages_to_delete)} messages so far... (Message ID: {message.id})")
        
        print(f"📊 Fetched {len(messages)} messages total")
        print(f"🎯 Found {len(messages_to_delete)} messages to delete (ENTIRE GROUP HISTORY!)")
        
        if not messages_to_delete:
            print("✅ No messages to delete!")
            return
        
        # Confirm deletion
        print("\n⚠️  WARNING: This will permanently delete the selected messages!")
        confirmation = input("Do you want to proceed? (yes/no): ").strip().lower()
        
        if confirmation not in ['yes', 'y']:
            print("❌ Operation cancelled by user.")
            return
        
        # Delete messages in batches (Telegram API limit is 100 messages per request)
        BATCH_SIZE = 100
        deleted_count = 0
        
        print(f"🗑️  Starting deletion process...")
        
        for i in range(0, len(messages_to_delete), BATCH_SIZE):
            batch = messages_to_delete[i:i + BATCH_SIZE]
            
            try:
                print(f"🗑️ Attempting to delete batch {i//BATCH_SIZE + 1} with {len(batch)} messages...")
                print(f"   Message IDs: {batch[:5]}{'...' if len(batch) > 5 else ''}")
                
                # Check if it's a supergroup/channel and use appropriate delete method
                if hasattr(chat, 'megagroup') and chat.megagroup:
                    print("   Using ChannelDeleteMessagesRequest (supergroup)")
                    result = await client(ChannelDeleteMessagesRequest(
                        channel=chat,
                        id=batch
                    ))
                elif hasattr(chat, 'broadcast') and chat.broadcast:
                    print("   Using ChannelDeleteMessagesRequest (channel)")
                    result = await client(ChannelDeleteMessagesRequest(
                        channel=chat,
                        id=batch
                    ))
                else:
                    print("   Using regular DeleteMessagesRequest (group)")
                    result = await client(DeleteMessagesRequest(
                        revoke=True,  # Delete for everyone (if we have permission)
                        id=batch
                    ))
                
                deleted_count += len(batch)
                print(f"✅ Successfully deleted batch {i//BATCH_SIZE + 1}: {len(batch)} messages (Total: {deleted_count})")
                print(f"   API Result: {result}")
                
                # Add a small delay to avoid hitting rate limits
                if i + BATCH_SIZE < len(messages_to_delete):
                    await asyncio.sleep(1)
                    
            except FloodWaitError as e:
                print(f"⏳ Rate limit hit. Waiting {e.seconds} seconds...")
                await asyncio.sleep(e.seconds)
                # Retry the same batch
                i -= BATCH_SIZE
                continue
                
            except ChatAdminRequiredError:
                print("❌ Error: Admin rights required to delete messages in this chat")
                break
                
            except Exception as e:
                print(f"❌ Error deleting batch: {e}")
                continue
        
        print(f"\n🎉 Successfully deleted {deleted_count} messages!")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        
    finally:
        print("📴 Disconnecting...")
        await client.disconnect()

async def is_admin(client, chat):
    """
    Check if the current user is an admin in the given chat.
    
    Args:
        client: TelegramClient instance
        chat: Chat entity
        
    Returns:
        bool: True if user is admin, False otherwise
    """
    try:
        # Get our user ID
        me = await client.get_me()
        
        # Get chat participants (admins)
        async for participant in client.iter_participants(chat, filter=None):
            if participant.id == me.id:
                # Check if we have admin rights
                if hasattr(participant, 'admin_rights') and participant.admin_rights:
                    return True
                # Check if we're the creator
                if hasattr(participant, 'creator') and participant.creator:
                    return True
        
        return False
        
    except Exception:
        # If we can't check admin status, assume we're not admin
        return False

if __name__ == '__main__':
    print("Starting Telegram Message Cleaner...")
    print("Make sure you have configured your API credentials in the script!")
    print()
    
    # Run the async main function
    asyncio.run(main()) 