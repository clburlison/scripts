Get the current console users desktop picture path or print a message if using the default picture from Apple.

This is actually slower than using `osascript` (example below) however it gives you access to the data differently. Being easier to utilize the data might make it worth the performance loss.

```bash
osascript -e 'tell application "Finder" to get POSIX path of (get desktop picture as alias)'
```