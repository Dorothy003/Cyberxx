# 🔐 Secure File System API (FastAPI)

A backend system built with **FastAPI** that allows users to:
- Generate RSA key pairs (public/private)
- Store and manage user keys
- Upload files (encrypted with AES)
- Download/decrypt files
- Track activity logs

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/secure-filesystem.git
cd secure-filesystem
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
User & Key Management

POST /users/create → Create a new user with RSA key pair

GET /users/{user_id}/keys → Get a user’s public key

GET /users → List all users

📂 File Management

POST /files/upload

Params: user_id, file (multipart)

Encrypts with AES and stores securely

GET /files/{file_id}/download

Decrypts and returns the file

GET /files

List all uploaded files

📜 Activity Log

GET /api/activity

Returns recent activity (file uploads/downloads, user creation, etc.)
###

Individual JSON bodies you can paste (quick copy)
A) /keys/generate

Method: POST

URL: http://127.0.0.1:8000/keys/generate

Body: none

Example response (what you’ll get back):

{
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"
}

B) /keys/upload (minimal)

Method: POST

URL: http://127.0.0.1:8000/keys/upload

Headers: Content-Type: application/json

Body (raw JSON):

{
  "username": "lash",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\nPASTE_PUBLIC_KEY_LINES_HERE\n-----END PUBLIC KEY-----\n"
}

C) /keys/upload (with encrypted private key pieces)

Only if you’re also storing the encrypted private key server-side.

{
  "username": "lash",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\nPASTE_PUBLIC_KEY\n-----END PUBLIC KEY-----\n",
  "priv_salt_b64": "BASE64_SALT",
  "priv_nonce_b64": "BASE64_NONCE",
  "priv_cipher_b64": "BASE64_ENCRYPTED_PRIVATE_KEY"
}

D) /files/upload (multipart form-data, not JSON)

In Postman, set Body → form-data and add:

owner (text) → your username (e.g., lash)

recipients (text) → add one field per recipient (e.g., lash, rahul)

f (file) → choose a file

Tip: to add multiple recipients, duplicate the recipients row in Postman.
