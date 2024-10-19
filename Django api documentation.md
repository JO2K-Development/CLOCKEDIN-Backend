# DJANGO API DOCUMENTATION

This API must have a middleware that checks the token and other necessary parameters.

## Endpoints

### POST /api/login/google
1. KTOS KTO UMIE OAUTH2

### POST /worker/switch-work-status
**About:**  
**Params:** None  
**Body:** `QR string`

**Function Description:**
- Check middleware
- Check if client is a worker in the database
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

### GET /worker/work-cycles-by-period
**About:**  
**Params:** `period_start`, `period_beginning`  
**Body:** `worker_id`  

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

### GET /worker/work-cycles-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}  
**Body:** `worker_id`  

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

### GET /worker/statistics/summed-up-hours-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}, `is_confirmed_in_office` = {active, inactive} (filter flag, if inactive or not given)  
**Body:** `worker_id`  

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

### GET /worker/statistics/work-cycles-by-period
**About:**  
**Params:** `period_start`, `period_beginning`, `is_confirmed_in_office` = {active, inactive} (filter flag, if inactive or not given)  
**Body:** `worker_id`  

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

### GET /worker/statistics/salary-and-ifnotwage-by-type-and-offset
**About:** Finds the periods for you (easier for frontend developers).  
**Params:** `neg_offset`, `time_span_type` = {D, M, Y}  
**Body:** `worker_id`  

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
Salary within the period and, if the first day in the period didn't have a wage, the date of first wage, or an error.

### GET /worker/statistics/salary-and-ifnotwage-by-period
**About:**  
**Params:** `period_start`, `period_beginning`  
**Body:** `worker_id`  

**Function Description:**
- Check middleware
- Validate period and date

**If period and date are valid:**
- Retrieve all work cycles by the period from the database
- Find the first workday with specified wage in the wage logs, save that date.
- Go through all the work cycles checking wage for every day, multiply day's work by current day's salary for each day in the period.
- Respond with salary within the period and, if the first day in the period didn't have a wage, the date of first wage.

**Else:**
- Respond with an error.

**Response:**  
Salary within the period and, if the first day in the period didn't have a wage, the date of first wage, or an error.




POST(/worker/new-wage)
No.
about: Will add a wage into wage logs, if there is a wage
for that time
it will not change it and respond with appropriate report 
params: None
body: worker_id, new_wage, date_for_set

function desctription: 
-check middleware
-validate body
IF there is a wage in workers wages with the same date
as date_for_set:
-return error
ELSE:
-add new wage log

response: message


PUT(/worker/new-wage)
No.
about: Will add wage for the specified time even if there was 
a wage before
params: 
body: user_id, new_wage, date_for_set

function desctription:
-check middleware
-validate body
-add new wage log

response: message

DELETE(/worker/new-wage)
No.
about: removes all the wages for all the dates if they are there
params: 
body: user_id, to_be_removed_dates (might be a single el list)

function desctription:
-removes all the wages for all the dates if they are there

response:

(/admin)

POST(/admin/send-invite)
about: this allows user of this email to join ornganization
params: None
body: invited_email, organization_Id

function desctription:
this will send an email to a specific user informing him,
that he has been added to the organization and if this 
email is not yet registered in the organization the email 
content will encourage him to create an account. When he loggs
in he can choose what ivite to accept or create an organization.
Thats why the user will be added as invited in the organizations
users and will have a placeholder row in users table even if his
account is not yet created

-checks if user of invited_email is already in some organization if so 
responds with a message 'user is already in organization'
-checks if user of invited_email is in users table, if not, 
creates a placeholder account
-sends email to invited_email with information
-responds with a message 'user invited to organization'

response: message={'user is already in organization', 'user invited to organization'}




