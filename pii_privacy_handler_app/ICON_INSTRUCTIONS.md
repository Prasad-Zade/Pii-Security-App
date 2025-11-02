# App Icon Setup Instructions

## Quick Setup (Recommended)

1. **Get a PII Privacy Icon:**
   - Go to https://www.flaticon.com or https://icons8.com
   - Search for "shield lock" or "data privacy" or "security shield"
   - Download a 512x512 PNG icon (green shield with lock is ideal)

2. **Save the icon:**
   - Save it as `icon.png` in the `assets/` folder
   - Copy the same file as `icon_foreground.png`

3. **Generate launcher icons:**
   ```bash
   flutter pub get
   flutter pub run flutter_launcher_icons
   ```

## Alternative: Use Material Icon

If you want to use the built-in security icon:

1. Run this command:
   ```bash
   flutter pub get
   flutter pub run flutter_launcher_icons
   ```

The app will use a shield/security icon with a dark background (#2F2F2F).

## Icon Theme
- Background: Dark gray (#2F2F2F)
- Icon: Green shield with lock (represents PII protection)
- Style: Modern, minimal, professional
