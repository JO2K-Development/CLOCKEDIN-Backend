# DJANGO API DOCUMENTATION

This API must have a middleware that checks the token and other necessary parameters.

## Endpoints

### POST /api/login/google
1. KTOS KTO UMIE OAUTH2

### POST /user/switch-work-status
**About:**  
**Params:** None  
**Body:** 

### POST /user/switch-work-status-qr
**About:**  
**Params:** None  
**Body:** `QR string`

**Function Description:**
- Check middleware
- Check if client is a user in the database
- Decipher QR string
- Compare `date(now)` - QR string's timestamp < 24h (expired QR)

**If comparison is correct:**
- Switch user's work status (the table with current opened work cycles dependent on its current status will have the current user's cycle terminated, with data propagation to the table with past cycles)
- Respond with a 'correct' flag and user details, including information on whether they arrived or left.

**Else If comparison is outdated:**
- Respond solely with an 'outdated' flag.

**Else:**
- Respond solely with an 'incorrect' flag.

**Response:**  
Flag and, if the QR code is correct, user details including information on whether they arrived or left.



### GET /user/work-cycles-by-period
**About:**  
**Params:** `period_start`, `period_beginning`  
**Body:** `user_id`  

**Function Description:**
- Check middleware
- Validate period and date

**If period and date are valid:**
- Retrieve all work cycles by the period from the database
- Respond with a list of work cycles in JSON format from the period.

**Else:**
- Respond with an error.

**Response:**  
List of work cycles in JSON format from the period or an error.

### GET /user/work-cycles-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}  
**Body:** `user_id`  

**Function Description:**
- Check middleware
- Validate params

**If params are valid:**
- Take the beginning of the current D/M/Y
- Offset it appropriately to a new position (by `-neg_offset` applied to days/months/years)
- Retrieve all work cycles from the period of new position -> new position + D/M/Y from the database
- Respond with a list of work cycles in JSON format from the period.

**Else:**
- Respond with an error.

**Response:**  
List of work cycles in JSON format from the period or an error.

## Statistics Endpoints

### GET /user/statistics/summed-up-hours-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}, `is_confirmed_in_office` = {active, inactive} (filter flag, if inactive or not given)  
**Body:** `user_id`  

**Function Description:**
- Check middleware
- Validate params

**If params are valid:**
- Take the beginning of the current D/M/Y
- Offset it appropriately to a new position (by `-neg_offset` applied to days/months/years)
- Retrieve all work cycles from the period of new position -> new position + D/M/Y from the database
- Apply filter if active
- Respond with summed hours of all the work cycles within the period.

**Else:**
- Respond with an error.

**Response:**  
Summed hours of all the work cycles within the period or an error.

### GET /user/statistics/work-cycles-by-period
**About:**  
**Params:** `period_start`, `period_beginning`, `is_confirmed_in_office` = {active, inactive} (filter flag, if inactive or not given)  
**Body:** `user_id`  

**Function Description:**
- Check middleware
- Validate period and date

**If period and date are valid:**
- Retrieve all work cycles by the period from the database
- Apply filter if active
- Respond with summed hours of all the work cycles within the period.

**Else:**
- Respond with an error.

**Response:**  
Summed hours of all the work cycles within the period or an error.

### GET /user/statistics/salary-and-ifnotwage-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}  
**Body:** `user_id`  

**Function Description:**
- Check middleware
- Validate params

**If params are valid:**
- Take the beginning of the current D/M/Y
- Offset it appropriately to a new position (by `-neg_offset` applied to days/months/years)
- Retrieve all work cycles from the period of new position -> new position + D/M/Y from the database
- Find the first workday with specified wage in the wage logs, save that date.
- Go through all the work cycles checking wage for every day, multiply day's work by current day's salary for each day in the period.
- Respond with salary within the period and, if the first day in the period didn't have a wage, the date of first wage.

**Else:**
- Respond with an error.

**Response:**  
Salary within the period and, if the first day in the period didn't have a wage, the date of
