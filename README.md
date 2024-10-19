# CLOCKEDIN - API

## How to start

### Google OAuth2 Integration for Development

This guide provides steps to integrate **Google OAuth2** using **Google Developers Playground** for development purposes.

### Steps:

1. **Navigate to Google Developers Playground:**
   - Visit the [Google Developers Playground](https://developers.google.com/oauthplayground/).

2. **Add OAuth Scopes and Authorize APIs:**
   - In the first step, add the following OAuth scopes (all in one line) and click "Authorize APIs":
     ```
     https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile
     ```

3. **Exchange Authorization Code for Tokens:**
   - In the second step, click "Exchange authorization code for tokens."
   - Copy the `id_token` from the response.

4. **Send `id_token` to Your API Endpoint:**
   - Send a `POST` request to your API endpoint (`api/login/google/`) with the `id_token` in the request body as JSON.
     ```json
     {
       "token": "<your_id_token_here>"
     }
     ```

5. **Receive and Use JWT Token:**
   - You will receive a JWT token in the response.
   - Use this JWT token for authenticated requests by adding it to the `Authorization` header as a Bearer token:
     ```
     Authorization: Bearer <your_jwt_token>
     ```

---

### Environment Variables
Create a `.env` file in the app root directory with the following content:
```plaintext
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client>
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
