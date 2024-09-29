import pyscreenshot as ImageGrab

# Capture the entire screen
im = ImageGrab.grab()

# Save the screenshot to a file
im.save("screenshot.png")

# Display the screenshot
im.show()
