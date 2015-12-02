disable_camera_popup
===

Only tested on 10.9-10.11.

The following script will stop Photos.app, Image Capture.app, iPhoto, etc. from opening when plugging in a "camera" device. Apple stores per-device preferences inside of ``~/Library/Preferences/ByHost/com.apple.ImageCapture2.$UUID.plist`` however if the following two keys are set to null no apps are opened. Device UID preferences override these global settings.