## Open Aerial Map (OAM) Plugin for QGIS 3, Express Edition

With this plugin, we can search and download images and metadata via OAM catalog. For the details of Open Aerial Map Project, please visit the following site:
https://docs.openaerialmap.org/

## Build from source code
(As of April 2021, this plugin is developed with QGIS 3.18 on Linux Mint 20, 64bit)

1. Install pyrcc5:
You need to install pyrcc5 if you don't have it installed on your system.
Probably, the easiest way to install pyrcc5 is to use package manager.
If using ubuntu or its compatible distribution, following command should work:
&nbsp;&nbsp;&nbsp;&nbsp;apt-get install pyqt5-dev-tools
For the other distributions, please use the online resource to get the information.

2. Download the repository and deploy the code to the plugin directory:
$ git clone https://github.com/yojiyojiyoji/oam_qgis3_express.git
$ cd oam_qgis3_express
$ make deploy

## Installation from package file
If you already have a packaged file (.zip format), you can simply install it from QGIS Plugin Manager.

1. Click "Plugin" in Menu Bar -> "Manage and Install Plugins", and plugin Window will open.
2. Select "Install from ZIP" on the left side of the window.
3. Select the package (.zip) file of the plugin.
4. Click "Install Plugin".

Please refer to the online resources of QGIS for the details of the plugin installation process.