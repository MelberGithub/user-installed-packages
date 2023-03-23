# user-installed-packages

This app is designed to make it easy to reinstall packages that the user has added to the default installation and retained.
It combines two steps:
1) quickly and easily create a list of those packages
2) use that list in another location to review and reinstall those packages, if still available

![user-installed-packages](/pix/uip-main.png)


Build package with "debuild -uc -us"

Build and sign package with "debuild -si"

Clean build  "debuild -- clean"

Build prerequisit : meson version >= 1.0.0
