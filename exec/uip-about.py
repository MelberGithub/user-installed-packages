#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The purpose of this program is to display the about-box for MX-Fluxbox.
Copyright (C) 2023 MX Authors

Authors: fehlix
         MX DevTeam <http://mxlinux.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import subprocess
from subprocess import run, DEVNULL, Popen
import gettext
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton
import shutil

# system
package_name    = 'user-installed-packages'
executable      = sys.executable
real_path       = os.path.realpath(__file__)
exec_path       = real_path
link_path       = f"{os.path.dirname(real_path)}/{package_name}"

if os.path.islink(link_path) and os.path.realpath(link_path) == real_path:
    exec_path = link_path

# files
license_file   = f"/usr/share/{package_name}/license.html"
# changelog
changelog_origin  = "MX repository"
changelog_uri     = "https://mxrepo.com/mx/repo/pool/@CHANGEPATH@.changelog"

# window icons and class
class_name   = package_name
icon_name    = package_name
aboutBoxIcon = f"/usr/share/pixmaps/{icon_name}.svg"
windowIcon   = icon_name
if os.path.exists(windowIcon):
    windowIcon   = f"/usr/share/pixmaps/{icon_name}.svg"

# translations
gettext.bindtextdomain(package_name, '/usr/share/locale')
gettext.textdomain(package_name)
gettext.install(package_name)
_ = gettext.gettext

about               = _('MX User Installed Packages')
aboutTitle          = _('About MX User Installed Packages')
aboutText           = _('An app to list and re-install user installed packages.')
changelogButtonText = _('Changelog')
changelogTitle      = _('MX User Installed Packages Changelog')
closeButtonText     = _('Close')
licenseButtonText   = _('License')
licenseViewerTitle  = _('MX User Installed Packages License')

# argv
key_opts = ['-c', '--changelog', '-l', '--license' ]
arg_opts = [x.lstrip('-') for x in sys.argv if x in key_opts]
key_default = 'close'

if len(arg_opts) > 0:
    if arg_opts[0] == 'changelog' or arg_opts[0] == 'c':
        key_default = 'changelog'
    elif arg_opts[0] == 'license' or arg_opts[0] == 'l':
        key_default = 'license'

def About(aboutBox):
    # get package version
    cmd = f"dpkg-query -f ${{Version}} -W {package_name}"
    version = run(cmd.split(),capture_output=True, text=True).stdout
    if not version:
        version = 'n/a'

    boxText = f'''
    <p align=center><b><h2>{about}</h2></b></p>
    <p align=center>Version: {version}</p>
    <p align=center><h3>{aboutText}</h3></p>
    <p align=center><a href=https://mxlinux.org>https://mxlinux.org</a>
    <br></p><p align=center>Copyright (c) MX Linux<br /><br/></p>
    '''

    iconPixmap = QtGui.QPixmap(aboutBoxIcon)
    aboutBox.setIconPixmap(iconPixmap)
    aboutBox.setWindowTitle(aboutTitle)
#   aboutBox.setWindowIcon(QtGui.QIcon(windowIcon))
    aboutBox.setWindowIcon(QtGui.QIcon.fromTheme(icon_name))
    aboutBox.setText(boxText)

    changelogButton = aboutBox.addButton((changelogButtonText), QMessageBox.ActionRole)
    licenseButton   = aboutBox.addButton((licenseButtonText)  , QMessageBox.ActionRole)
    closeButton     = aboutBox.addButton((closeButtonText)    , QMessageBox.RejectRole)

    changelogButton.setIcon(QtGui.QIcon.fromTheme("view-history"))
    licenseButton.setIcon(QtGui.QIcon.fromTheme("license"))
    closeButton.setIcon(QtGui.QIcon.fromTheme("window-close"))

    aboutBox.setEscapeButton(closeButton)
    if key_default == 'changelog':
        aboutBox.setDefaultButton(changelogButton)
    elif key_default == 'license':
        aboutBox.setDefaultButton(licenseButton)
    else:
        aboutBox.setDefaultButton(closeButton)

    aboutBox.exec_()

    if aboutBox.clickedButton() == changelogButton:
        showChangelog()
    if aboutBox.clickedButton() == licenseButton:
        showLicence()
    if aboutBox.clickedButton() == closeButton:
        sys.exit(0)

def showLicence():
    licenseViewer = license_viewer()
    if not licenseViewer:
        return
    if licenseViewer in ['/usr/bin/python3']:
        cmd = [licenseViewer, '-m', 'webbrowser', '-n',  license_file]
    elif licenseViewer in ['mx-viewer', 'antix-viewer']:
        cmd = [licenseViewer, license_file, licenseViewerTitle]
    elif licenseViewer in ['exo-open']:
        cmd = ['exo-open', '--launch', 'WebBrowser', license_file]
    else:
        cmd = [licenseViewer, license_file]

    run(cmd)

    cmd = [executable, exec_path,  '--license']
    Popen(cmd)
    sys.exit(0)

def showChangelog():
    from subprocess import Popen, check_call, run
    from subprocess import DEVNULL, PIPE, CalledProcessError

    changelog_aptpref = "Acquire::Changelogs::URI::Origin"
    changelog_option  = f"{changelog_aptpref}::{changelog_origin}={changelog_uri}"

    # display geometry
    cmd = ['xdotool', 'getdisplaygeometry']
    res = run(cmd, capture_output=True, text=True).stdout
    W, H = res.strip().split()
    height = int(H)*2/3
    width  = int(W)*3/5

    closeButton = f"{closeButtonText}!window-close"

    yad_filler = {
        'changelog_window_icon' : windowIcon,
        'changelog_title'       : changelogTitle,
        'class_name'            : class_name,
        'close'                 : closeButton,
        'height'                : int(height),
        'width'                 : int(width),
        }


    yad = """
          /usr/bin/yad
          --title={changelog_title}
          --window-icon={changelog_window_icon}
          --class={class_name}
          --width={width}
          --height={height}
          --center
          --button={close}
          --fontname=mono
          --margins=7
          --borders=5
          --text-info
        """
    # substitute placeholder with yad_filler
    y = [ x.strip() for x in yad.strip().split('\n') ]
    yad = [ x.format(**yad_filler) for x in y ]

    pipe1 = Popen(['apt-get', '-qq', '-o', changelog_option, 'changelog', package_name],
                  env={'PAGER':'cat'}, stdout=PIPE, stderr=subprocess.STDOUT,text=True)
    pipe2 = Popen(yad, stdin=pipe1.stdout, stdout=PIPE, stderr=PIPE, text=True)
    # if pipe2 exits before pipe1, send SIGPIPE to pipe1 to close
    pipe1.stdout.close()
    pipe2.communicate()[0]

    cmd = [executable, exec_path, '--changelog']
    Popen(cmd)
    sys.exit(0)

def license_viewer():
    # list of viewers to check
    viewer_list  = []
    viewer_list += ['mx-viewer', 'antix-viewer']
    viewer_list += ['/usr/bin/python3']
    # xfce-handling
    if os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
        viewer_list += ['exo-open']

    # set xdg-open last to avoid html opens with tools like html-editor
    viewer_list += ['sensible-browser']
    viewer_list += ['x-www-browser', ]
    viewer_list += ['gnome-www-browser']
    viewer_list += [ 'xdg-open']

    from shutil import which
    # take first viewer found
    # viewer = list(filter( lambda x: which(x), viewer_list))[0]
    # using lambda-filter over viewer_list to stop searching when found:
    v = ['']
    f = v.__setitem__
    vl = viewer_list
    viewer = list(filter(lambda x: not v[0] and (f(0, which(x)), v[0])[1], vl))[0]
    return viewer

def displayAbout():
    app = QApplication(sys.argv)
    aboutBox = QMessageBox()
    About(aboutBox)
    aboutBox.show()
    sys.exit(app.exec_())

def main():
    displayAbout()

if __name__ == '__main__':
    main()
