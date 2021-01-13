
http://127.0.0.1:8000/api/v1/token/						- Generates a JWT token.

http://127.0.0.1:8000/api/v1/refresh/						- To refresh a JWT access token using a refresh token.

http://127.0.0.1:8000/admin/backend/actiosession/ 				- User enrolls for an Actio session.

http://127.0.0.1:8000/api/v1/twilio/room/?action=create&actio_session=5  	- Coach starts the session and when coach pushes "Start session", this end point is reached. 
										  - It creates a Twilio Room
										  - Sends back room display name, room unique name, and a Twilio auth token.

http://127.0.0.1:8000/api/v1/twilio/calls/video/?actio_session=4		- From coache's phone, a request is sent to this endpoint, and it starts the session.
										  - Collects the users enrolled for a session.
										  - Sends a ANS Push notification to each device by reading each users's ARN from database. This is done serially at the moment.


http://127.0.0.1:8000/api/v1/session/retrieve/?status=completed			- To retrieve scheduled/completed sessions
