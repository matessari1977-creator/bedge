[app]

# (str) Title of your application
title = Bedge

# (str) Package name
package.name = bedge

# (str) Package domain (needed for android packaging)
package.domain = org.matteo

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# CAUTION: non bloccare le versioni di python o hostpython, ci pensa GitHub online!
requirements = python3,kivy,pg8000

# (str) Supported orientations (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (int) Android API to use (33 o 34 sono gli standard stabili attuali)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android architectural target (arm64-v8a e armeabi-v7a coprono tutti i telefoni)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

android.permissions = INTERNET
