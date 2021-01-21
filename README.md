###  Available endpoints

#### Generates a JWT token
http://127.0.0.1:8000/api/v1/token/ 

#### To refresh a JWT access token using a refresh token
http://127.0.0.1:8000/api/v1/refresh/ 

#### User enrollment for an Actio session. Creates a session identifier which is a UUID.
http://127.0.0.1:8000/admin/backend/actiosession/

#### Coach starts the session and when coach pushes "Start session", this end point is reached.
http://127.0.0.1:8000/api/v1/twilio/room/create/930a903c-aae1-4eda-9a8b-46c7fbc8be34/ 
  - Creates a Twilio Room
  - Sends back room display name, room unique name, and a Twilio auth token.

#### Start a video call(Done by a coach)
http://127.0.0.1:8000/api/v1/twilio/calls/video/930a903c-aae1-4eda-9a8b-46c7fbc8be34/		
   - From coache's phone, a request is sent to this endpoint, and it starts the session.
   - Collects the users enrolled for a session.
   - Sends a ANS Push notification to each device by reading each users's ARN from database. This is done serially at the moment.

#### Retrieve sessions
http://127.0.0.1:8000/api/v1/sessions/status/[Scheduled|Completed]/			
  - To retrieve scheduled/completed sessions
