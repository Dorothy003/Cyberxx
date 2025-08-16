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