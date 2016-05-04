## URL Structure

`https://{Host}:7443/api/2.0/{Path}`
* Host is the host running the NVR
* Path is the path for the specific API method you’re calling.

## Authentication

API authentication happens either with cookies (for the web UI) or with a bearer token available from the web UI.  This token is sent as a query parameter with key `apiKey`.

For example, an api key of `abcDEF1234` could be used to fetch bootstrap information as follows:

`https://localhost:7443/api/2.0/bootstrap?apiKey=abcDEF1234`


## API Methods

* `bootstrap` 
	* This fetches a bunch of data about the system
	* Structure is as follows:
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
			* `cameras` - List of cameras, each a Dict with the following keys:
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