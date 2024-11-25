# Employee Work Time Monitoring System [CLOCKEDIN]

## 📢 **About the Project**

This system is a comprehensive solution for monitoring employee work time, designed for small and medium-sized businesses seeking affordable tools for managing employee hours. The main goals of the project include:

- **Real-time work time monitoring** for employees.
- **Streamlining employee data management** through the admin panel.
- **Support for supervisors and employees** with accessible statistics, data filtering, and editable work hours.

The project is currently under development, with the first version scheduled for completion by February 28, 2025.

---

## 🎯 **Project Goals**

### Final Goal:
- Delivering a fully functional system with three main modules:
  - **Admin Panel**: manage employees and generate reports.
  - **User Panel**: view work hours and statistics.
  - **Reader Mode**: log employee entry and exit using QR codes.

### Detailed Requirements:
- **User Panel**:
  - Display historical data on work hours and overtime.
  - Filter data by date, week, or month.
  - Calculate salaries based on hours worked.
- **Admin Panel**:
  - Add, edit, and delete employees.
  - Generate work time reports.
  - Manage hourly rates and oversee access areas.
- **Reader Mode**:
  - Log entry and exit using cameras and QR codes.
  - Achieve a 95% success rate in employee logins within the first month of operation.

---

## 💡 **Development Plan**

### Phase I: Core Functionality (by February 2025)
1. **Web Application**:
   - OAuth2 login.
   - Record work start and end times.
   - View work statistics and filter historical data.
2. **Backend (API)**:
   - Store historical data and support filtering.
   - OAuth2 authentication and login.
   - Mechanism for tracking currently active employees.
3. **Mobile Application**:
   - OAuth2 login support.
   - QR code verification feature.
4. **Reader Mode**:
   - Implement devices for logging entry and exit times.

### Phase II: Advanced Modules (after 2025)
- **Leave and Absence Management**: submit leave requests, sick leave, and other absences.
- **Contract Authentication**: digitally sign legal documents.
- **Automated Payroll**: generate salary transfers.
- **Google Calendar Integration**: synchronize events and schedules.

---

## 🛠 **Technologies and Architecture**

### Technologies:
- **Backend**: Django & Python.
- **Frontend**: React & TypeScript.
- **Mobile Application**: Flutter.
- **Database**: MySQL.
- **Authentication**: OAuth2.

### API Features:
- Secure storage of historical data.
- Data filtering for reports and statistics.
- Real-time work session logging.

---

# CLOCKEDIN - API

## How to start

### Environment Variables
Create a `.env` file in the app root directory with the following content:
```plaintext
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client>
EMAIL_HOST_PASSWORD=<email-host-password>
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```


### Install Dependencies
```bash
pip install -r requirements.txt
```

### Migrate the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser
```bash
python manage.py createsuperuser
```

### Run the Server
```bash
python manage.py runserver
```

### Optional: Docker
```bash
docker-compose up --build
```

---
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

### Register User

***POST*** `/auth/register/`

**Headers:**

`Content-Type`: application/json

**Body:**
```json
{
    "email": "<email>",
    "password1": "<password>",
    "password2": "<password>"
}
```



### Login with Google

**POST** `auth/google/`

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
