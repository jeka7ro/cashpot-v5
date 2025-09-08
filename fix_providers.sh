#!/bin/bash

echo "🔍 Fixing provider mapping based on Google Sheet..."

# Login to Railway
echo "🔐 Logging in to Railway..."
LOGIN_RESPONSE=$(curl -s -X POST "https://cashpot-v5-production.up.railway.app/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Railway login failed"
  exit 1
fi

echo "✅ Logged in to Railway"

# Get providers
echo "📋 Getting providers..."
PROVIDERS_RESPONSE=$(curl -s -X GET "https://cashpot-v5-production.up.railway.app/api/providers" \
  -H "Authorization: Bearer $TOKEN")

# Extract provider IDs
EGT_ID=$(echo $PROVIDERS_RESPONSE | grep -o '"id":"[^"]*","name":"EGT"' | cut -d'"' -f4)
ALFASTREET_ID=$(echo $PROVIDERS_RESPONSE | grep -o '"id":"[^"]*","name":"Alfastreet"' | cut -d'"' -f4)

echo "📊 EGT ID: $EGT_ID"
echo "📊 Alfastreet ID: $ALFASTREET_ID"

# Get slot machines
echo "🎰 Getting slot machines..."
SLOTS_RESPONSE=$(curl -s -X GET "https://cashpot-v5-production.up.railway.app/api/slot-machines" \
  -H "Authorization: Bearer $TOKEN")

# Update specific slot machines based on Google Sheet mapping
echo "🔄 Updating slot machines..."

# EGT slots (from Google Sheet)
EGT_SERIALS=("134862" "135226" "149582" "149583" "149621" "149612" "149628" "149614" "142270" "150246" "150247" "155706" "142848" "142851" "150243" "142855" "150242")

for serial in "${EGT_SERIALS[@]}"; do
  echo "  🔄 Updating serial $serial to EGT..."
  
  # Find slot ID by serial number
  SLOT_ID=$(echo $SLOTS_RESPONSE | grep -o '"id":"[^"]*","serial_number":"'$serial'"' | cut -d'"' -f4)
  
  if [ ! -z "$SLOT_ID" ]; then
    # Update provider
    UPDATE_RESPONSE=$(curl -s -X PUT "https://cashpot-v5-production.up.railway.app/api/slot-machines/$SLOT_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"provider_id\": \"$EGT_ID\"}")
    
    if [[ $UPDATE_RESPONSE == *"success"* ]] || [[ $UPDATE_RESPONSE == *"updated"* ]]; then
      echo "    ✅ Updated $serial to EGT"
    else
      echo "    ❌ Failed to update $serial: $UPDATE_RESPONSE"
    fi
  else
    echo "    ⚠️  Slot with serial $serial not found"
  fi
done

# Alfastreet slots (from Google Sheet)
ALFASTREET_SERIALS=("2522046669" "2522046670")

for serial in "${ALFASTREET_SERIALS[@]}"; do
  echo "  🔄 Updating serial $serial to Alfastreet..."
  
  # Find slot ID by serial number
  SLOT_ID=$(echo $SLOTS_RESPONSE | grep -o '"id":"[^"]*","serial_number":"'$serial'"' | cut -d'"' -f4)
  
  if [ ! -z "$SLOT_ID" ]; then
    # Update provider
    UPDATE_RESPONSE=$(curl -s -X PUT "https://cashpot-v5-production.up.railway.app/api/slot-machines/$SLOT_ID" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"provider_id\": \"$ALFASTREET_ID\"}")
    
    if [[ $UPDATE_RESPONSE == *"success"* ]] || [[ $UPDATE_RESPONSE == *"updated"* ]]; then
      echo "    ✅ Updated $serial to Alfastreet"
    else
      echo "    ❌ Failed to update $serial: $UPDATE_RESPONSE"
    fi
  else
    echo "    ⚠️  Slot with serial $serial not found"
  fi
done

echo "🎉 Provider mapping fix completed!"