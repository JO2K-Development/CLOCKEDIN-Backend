# CLOCKEDIN - API

## How to start
https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile

### Environment Variables
Create a `.env` file in the app root directory with the following content:
```plaintext
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client
```



# API Server - OAuth2 Login with Google

## Process Diagram

```plaintext
Frontend (Click "Login with Google")
      ⬇️
Google (User authorization, consent)
      ⬇️
Backend (Exchange code for token)
      ⬇️
Google (Return access token)
      ⬇️
Backend (Create user and token)
      ⬇️
Frontend (User logged in)
```

## API Endpoints

### Login with Google

**POST** `/login/google/`

**Headers:**

`Content-Type`: application/json

**Body:**
```json
{
    "code": "<google-oauth-code>"
}
```

Response:
```json
{
    "token": "<session-token>"
}
```

---
**GET** `/test/unsecured/`

**Headers:**

`Content-Type`: application/json

**Response:**
```json
{
    "message": "This is an unsecured get endpoint!"
}
```

---
**GET** `/test/secured/`

**Headers:**

`Content-Type`: application/json

`Authorization`: Token <session-token>

**Response:**
```json
{
    "message": "This is a secured get endpoint!"
}
```
