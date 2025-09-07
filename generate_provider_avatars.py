#!/usr/bin/env python3
"""
Script to generate custom avatars for providers on Railway
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

def generate_avatar_image(name, size=200):
    """Generate avatar image with initials"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Generate initials
    words = name.strip().split()
    if len(words) >= 2:
        initials = (words[0][0] + words[1][0]).upper()
    else:
        initials = name[:2].upper()
    
    # Try to use a system font, fallback to default
    try:
        font_size = int(size * 0.4)
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Get text size for centering
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Draw background circle
    margin = 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(59, 130, 246, 255), outline=(37, 99, 235, 255), width=2)
    
    # Draw text
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    draw.text((text_x, text_y), initials, fill=(255, 255, 255, 255), font=font)
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    return base64.b64encode(img_data).decode()

def login_railway():
    """Login to Railway and get token"""
    login_data = {'username': 'eugeniu2', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def upload_avatar(token, provider_id, provider_name):
    """Upload avatar for a provider"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Generate avatar
    avatar_data = generate_avatar_image(provider_name)
    
    # Create attachment data
    attachment_data = {
        'filename': f'custom_avatar_providers_{provider_id}_{provider_name.replace(" ", "_")}.png',
        'original_filename': f'avatar_{provider_name.replace(" ", "_")}.png',
        'file_size': len(base64.b64decode(avatar_data)),
        'mime_type': 'image/png',
        'file_data': avatar_data
    }
    
    # Upload attachment
    response = requests.post(
        f'https://cashpot-v5-production.up.railway.app/api/attachments/providers/{provider_id}',
        json=attachment_data,
        headers=headers
    )
    
    return response.status_code == 200

def main():
    print("🎨 Generating avatars for providers...")
    
    # Login
    token = login_railway()
    if not token:
        print("❌ Login failed")
        return
    
    print("✅ Logged in successfully")
    
    # Get providers
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://cashpot-v5-production.up.railway.app/api/providers', headers=headers)
    
    if response.status_code != 200:
        print("❌ Failed to fetch providers")
        return
    
    providers = response.json()
    print(f"📋 Found {len(providers)} providers")
    
    # Generate avatars for each provider
    success_count = 0
    for provider in providers:
        provider_id = provider['id']
        provider_name = provider['name']
        
        print(f"🎨 Generating avatar for {provider_name}...")
        
        if upload_avatar(token, provider_id, provider_name):
            print(f"✅ Avatar generated for {provider_name}")
            success_count += 1
        else:
            print(f"❌ Failed to generate avatar for {provider_name}")
    
    print(f"\n🎉 Generated avatars for {success_count}/{len(providers)} providers!")

if __name__ == "__main__":
    main()

