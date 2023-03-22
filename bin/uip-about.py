#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
The purpose of this program is to display the about-box for MX-Fluxbox.
Copyright (C) 2020 MX Authors

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

gettext.bindtextdomain('user-installed-packages', '/usr/share/locale')
gettext.textdomain('user-installed-packages')
gettext.install('user-installed-packages')
_ = gettext.gettext

# system
executable = sys.executable
abspath_file = os.path.abspath(__file__)

# files
changelog_file = "/usr/share/doc/user-installed-packages/changelog.gz"
changelog_url  = "http://mxrepo.com/mx/repo/pool/main/m/user-installed-packages/current.{debian_codename}"
license_file   = "/usr/share/doc/user-installed-packages/user-installed-packages.html"
version_file   = "/etc/mxfb_version"

# icons
aboutBoxIcon = '/usr/share/pixmaps/user-installed-packages.png'
windowIcon   = '/usr/share/pixmaps/user-installed-packages.png'

# translations
about               = _('MX User Installed Packages')
aboutTitle          = _('About MX User Installed Packages')
aboutText           = _('An app to list and re-install user installed packages.')
changelogButtonText = _('Changelog')
changelogTitle      = _('MX User Installed Packages Changelog')
closeButtonText     = _('Close')
licenseButtonText   = _('License')
licenseViewerTitle  = _('MX User Installed Packages license')

# argv
key_opts = ['-c', '--changelog', '-l', '--license' ]
arg_opts = [x.lstrip('-') for x in sys.argv if x in key_opts ]
key_default = 'close'

if len(arg_opts) > 0:
    if arg_opts[0] == 'changelog' or arg_opts[0] == 'c':
        key_default = 'changelog'
    elif arg_opts[0] == 'license' or arg_opts[0] == 'l':
        key_default = 'license'

def About(aboutBox):
    # read fluxbox version from file
#    try:
#        with open(version_file,"r") as f:
#            version = f.read().strip()
#    except FileNotFoundError:
#        version = 'n/a'
    # get packge version as release number
    cmd = "dpkg-query -f ${Version} -W user-installed-packages"
    release = run(cmd.split(),capture_output=True, text=True).stdout
    if not release:
        release = 'n/a'
        
#    <p align=center>Version: {version}</p>

    boxText = f'''
    <p align=center><b><h2>{about}</h2></b></p>

    <p align=center>Release: {release}</p>
    <p align=center><h3>{aboutText}</h3></p>
    <p align=center><a href=https://mxlinux.org>https://mxlinux.org</a>
    <br></p><p align=center>Copyright (c) MX Linux<br /><br/></p>
    '''

    iconPixmap = QtGui.QPixmap(aboutBoxIcon)
    aboutBox.setIconPixmap(iconPixmap)
    aboutBox.setWindowTitle(aboutTitle)
    aboutBox.setWindowIcon(QtGui.QIcon(windowIcon))
    aboutBox.setText(boxText)

    changelogButton = aboutBox.addButton((changelogButtonText), QMessageBox.ActionRole)
    licenseButton   = aboutBox.addButton((licenseButtonText)  , QMessageBox.ActionRole)
    closeButton     = aboutBox.addButton((closeButtonText)    , QMessageBox.RejectRole)
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
    if licenseViewer in ['mx-viewer', 'antix-viewer']:
        cmd = [licenseViewer, license_file, licenseViewerTitle]
    elif licenseViewer in ['exo-open']:
        cmd = ['exo-open', '--launch', 'WebBrowser', license_file]
    else:
        cmd = [licenseViewer, license_file]

    run(cmd)
    cmd = [executable, abspath_file, '--license']
    Popen(cmd)
    sys.exit(0)

def showChangelog():
    from subprocess import Popen, check_call, run
    from subprocess import DEVNULL, PIPE, CalledProcessError
    global changelog_file
    global changelog_url

    # display geometry
    cmd = ['xdotool', 'getdisplaygeometry']
    res = run(cmd, capture_output=True, text=True).stdout
    W, H = res.strip().split()
    height = int(H)*2/3
    width  = int(W)*3/5

    yad_filler = {
        'changelog_window_icon' : windowIcon,
        'changelog_title'       : changelogTitle,
        'close'                 : closeButtonText,
        'height'                : int(height),
        'width'                 : int(width),
        }

    yad = """
          /usr/bin/yad
          --title={changelog_title}
          --window-icon={changelog_window_icon}
          --width={width}
          --height={height}
          --center
          --button={close}
          --fontname=mono
          --margins=7
          --borders=5
          --text-info
        """
    # subsitute placeholder with yad_filler
    y = [ x.strip() for x in yad.strip().split('\n') ]
    yad = [ x.format(**yad_filler) for x in y ]

    show = False
    if not show:
        # try local changelog file
        try:
            with open(changelog_file,"r"):
                show = True
        except FileNotFoundError as e:
            changelog_file = ''
        if show:
            pipe1 = Popen(['zcat', changelog_file], stdout=PIPE)
            pipe2 = Popen(yad, stdin=pipe1.stdout, stdout=PIPE, stderr=PIPE, text=True)
            pipe1.stdout.close()
            pipe2.communicate()[0]

    if not show:
        # try check with curl file exists on sever
        changelog_url = changelog_url.format(debian_codename=debian_codename())
        try:
            cmd = f"curl --output /dev/null --silent --fail -r 0-0 {changelog_url}"
            cmd = cmd.split()
            check_call(cmd)
            show = True
        except CalledProcessError as e:
            ret = e.returncode
        if show:
            cmd = ['curl', '--silent', changelog_url ]
            pipe1 = Popen(cmd, stdout=PIPE, text=True)
            pipe2 = Popen(yad, stdin=pipe1.stdout, stdout=PIPE, stderr=PIPE, text=True)
            pipe1.stdout.close()
            pipe2.communicate()[0]

    if show:
        cmd = [executable, abspath_file, '--changelog']
        Popen(cmd)
        sys.exit(0)

def license_viewer():
    # list of viewers to check
    viewer_list = ['mx-viewer', 'antix-viewer']

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

def debian_codename():
    cmd = "lsb_release -sc".split()
    codename = run(cmd, capture_output=True, text=True).stdout.strip()
    return codename

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
