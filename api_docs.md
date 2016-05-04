## URL Structure

`https://{Host}:7443/api/2.0/{Path}`
* Host is the host running the NVR
* Path is the path for the specific API method you’re calling.

## Authentication

API authentication happens either with cookies (for the web UI) or with a bearer token available from the web UI.  This token is sent as a query parameter with key `apiKey`.

For example, an api key of `abcDEF1234` could be used to fetch bootstrap information as follows:

`https://localhost:7443/api/2.0/bootstrap?apiKey=abcDEF1234`




