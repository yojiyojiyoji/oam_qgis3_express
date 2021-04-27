## Open Aerial Map (OAM) Plugin for QGIS 3, Express Edition

With this plugin, we can search and download images and metadata via OAM catalog. For the details of Open Aerial Map Project, please visit the following site:
https://docs.openaerialmap.org/

## Build from source code
(As of April 2021, this plugin is developed with QGIS 3.18 on Linux Mint 20, 64bit)

###### Linux
1. Install pyrcc5:<br />
You need to install pyrcc5 if you don't have it installed on your system. Probably, the easiest way to install pyrcc5 is to use package manager. If using ubuntu or its compatible distribution, following command should work:<br /><br />
$ apt-get install pyqt5-dev-tools<br /><br />
For the other distributions, please use the online resource to get the information.

2. Download the repository and deploy the code to the plugin directory:<br />
$ git clone https://github.com/yojiyojiyoji/oam_qgis3_express.git<br />
$ cd oam_qgis3_express<br />
$ make deploy

###### Windows
1. Download the repository and deploy the code to the plugin directory:<br />
git clone https://github.com/yojiyojiyoji/oam_qgis3_express.git<br />
cd oam_qgis3_express\windows\

2. Execute pyrcc5_set_path.bat file with QGIS version<br />
Ex. (if you are using QGIS 3.16)<br />
pyrcc5_set_path.bat 3.16

2. Execute the batch file for installation<br />
Ex.<br />
make.bat deploy


## Installation from package file
If you already have a packaged file (.zip format), you can install it from QGIS Plugin Manager.

1. Click "Plugin" in Menu Bar -> "Manage and Install Plugins", and plugin Window will open. <br />
2. Select "Install from ZIP" on the left side of the window.
3. Select the package (.zip) file of the plugin.
4. Click "Install Plugin".

Please refer to the online resources of QGIS for the details of the plugin installation process.
