# Ubiquiti NVR API (unofficial)

I wanted to try writing some code to interface with the Ubiquiti NVR video and couldn't find any documentation on their API.  This is my attempt at starting that, both for my own personal use and to help others.  This mostly comes from playing around in the UI and looking at what requests it makes with the Network tab in the developer tools.

## URL Structure

`https://{Host}:7443/api/2.0/{Method}`

* Host is the host running the NVR
* Method is the specific API method you’re calling (see below for enumeration)

## Authentication

API authentication happens either with the cookie `JSESSIONID_AV` (for the web UI) or with a bearer token available from the web UI.  This token is sent as a query parameter with key `apiKey`.

For example, an api key of `abcDEF1234` could be used to fetch bootstrap information as follows:

`https://localhost:7443/api/2.0/bootstrap?apiKey=abcDEF1234`


## API Methods

These are all the API methods I've seen so far.  I try to cover any parameters first, and then the return structure, which is generally JSON.

* `bootstrap`
	* This fetches a bunch of data about the system
	* Return value structure is a dictionary as follows:
		* `meta`
		* `data` - a list of length 1, containing a dict
			* `cloudHost`
			* `cameraSchedules`
			* `userGroups`
			* `settings` - Dict.  Settings for the system as a whole - nothing per-camera.
				* `systemSettings` - Dict.  A handful of system-side settings, like whether it should discover new cameras or report stats.
				* `_id` - String.  A unique identifier for the system (?)
				* `alertSettings` - Dict.  Global settings about how to do alerts	and emails
				* `emailSettings` - Dict.  SMTP information for the mechanics of sending emails
			* `systemInfo` - Dict.  Info about the NVR software (build numbers, ports, etc).
			* `maps` - Dict.  Info for showing cameras on a map (?)
			* `cameras` - List of cameras, each a Dict with keys documented in the `camera` API method
			* `adminUserGroupId`
			* `servers` - List of NVRs (?) with similar data to `systemInfo`
			* `serviceState` - A string, e.g. `READY`
			* `liveViews` - Empty list?
			* `firmwares` - List of available firmware upgrades
			* `nvrName` - String.  The name of this NVR.
			* `user` - Dict.  Metadata about the current logged in user (including the api key).
			* `alertSchedules`
			* `isFactoryDefault`
			* `isLoggedIn`
			* `isHardwareNvr`

* `camera`
	* `GET` gets camera info
	* `PUT` sets camera info (do you need to submit all of it, or can you just send one updated value?)
	* Info:
		* `enableSpeaker`
		* `managed`
		* `speakerVolume`
		* `zones`
		* `lastSeen`
		* `analyticsSettings`
		* `protocolVersion`
		* `mapSettings`
		* `ispSettings`
		* `firmwareVersion`
		* `uptime`
		* `recordingSettings`
		* `uuid`
		* `firmwareBuild`
		* `platform`
		* `state`
		* `deviceSettings`
		* `username`
		* `scheduleId`
		* `internalHost`
		* `provisioned`
		* `deleted`
		* `lastRecordingId`
		* `micVolume`
		* `host`
		* `hasDefaultCredentials`
		* `name`
		* `channels`
		* `networkStatus`
		* `lastRecordingStartTime`
		* `systemInfo`
		* `mac`
		* `status`
		* `enableSuggestedVideoSettings`
		* `model`
		* `_id`
		* `osdSettings`
		* `enableStatusLed`
* `recording` - Fetches information about recordings
	* GET params, e.g. `cause%5B%5D=fullTimeRecording&cause%5B%5D=motionRecording&startTime=1462258800000&endTime=1462345200000&idsOnly=true&sortBy=startTime&sort=desc`
		* `cause[]` - list (one key per entry) with possible values:
			*  `fullTimeRecording`
			*  `motionRecording`
		*  `startTime` - ms since epoch. Show recordings after this time
		*  `endTime` - ms since epoch.  Show recordings before this time.
		*  `idsOnly` - boolean.  If true, just return a list of video uuids.  If false, also include metadata about each recording as well.
		*  `sortBy` - Takes at least one value, `startTime`
		*  `sort` - Takes `desc` or (presumably) `asc`.
	*  Response: See `recording/{RecordingID}` for response data.
*  `recording/{RecordingID}[,{RecordingID}...]` - Takes a comma-separated list of recording IDs and returns metadata about each
* `snapshot/recording/{CameraID}/{YYYY}/{MM}/{DD}/{RecordingID}` - Fetches a JPG thumbnail for the given recording from the given camera
	* Optionally takes `width` parameter, with pixel width of thumbnail
* `recording/{RecordingID}/motion` - Fetches a PNG showing where motion was detected on the given recording
	* Optionally takes `alpha` parameter.  If true, returns PNG with alpha channel and red marking areas of motion.  If false, returns PNG with black showing no motion and white showing motion.
	* Response:
		* `inProgress`: boolean. 
		* `locked`: boolean
		* `endTime`: int.  ms since epoch.
		* `cameras`: A list (why?) of cameras IDs involved.
		* `eventType`: e.g. motionRecording, 
		* `_id`: The recording ID.
		* `meta`: dict with keys as follows:
			* `key`: string.
			* `cameraName`: string.  Human name for the camera (may be non-unique)
			* `recordingPathId`: string.
		* `startTime`: int.  ms since epoch.
		* `markedForDeletion`: boolean.
* `recording/{RecordingID}/download`: a video file representing the recording.