# MongoDB Atlas Setup for Render

## 1. Create MongoDB Atlas Account
1. Go to https://cloud.mongodb.com
2. Create a free account
3. Create a new cluster (free tier)

## 2. Configure Database Access
1. Go to "Database Access" in the left menu
2. Add a new database user
3. Create a username and password
4. Set privileges to "Read and write to any database"

## 3. Configure Network Access
1. Go to "Network Access" in the left menu
2. Add IP Address: 0.0.0.0/0 (allow all IPs)
3. Or add Render's IP ranges

## 4. Get Connection String
1. Go to "Clusters" in the left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace <password> with your database user password
6. Replace <dbname> with "cashpot_v5"

## 5. Add to Render Environment Variables
1. Go to your Render service dashboard
2. Go to "Environment" tab
3. Add MONGO_URL with your connection string
4. Add JWT_SECRET_KEY with a secure random string
5. Add DB_NAME=cashpot_v5

## Example MONGO_URL:
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/cashpot_v5?retryWrites=true&w=majority
