@ECHO OFF
REM Please execute pyrcc5_set_path.bat file stored in the same directory

REM Set the default plugin folder
SET PLUGIN_NAME=oam_qgis3_express
SET OAM_PLUGIN_DIR=%HOMEPATH%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\%PLUGIN_NAME%

SET FOLDERS=ext_libs gui icon module temp i18n
SET TARGET_FILES=__init__.py metadata.txt oam_qgis3.py^
                resources.qrc^
                resources.py^
                oam_qgis3_dialog.py oam_qgis3_dialog_base.ui

REM Set the build folder for help files
SET HELP=help\build\html

REM set the resource folder for translation
REM SET LOCALS=, LRELEASE=, etc.

if "%1" == "deploy" (
  ECHO Create resources.py
  pyrcc5 -o ..\resources.py ..\resources.qrc

  ECHO Create OAM Plugin Directory %OAM_PLUGIN_DIR%
  mkdir %OAM_PLUGIN_DIR%

  FOR %%f IN (%FOLDERS%) DO (
    xcopy ..\%%f %OAM_PLUGIN_DIR%\%%f\ /E /Y
  )

  REM xcopy ..\%HELP% %OAM_PLUGIN_DIR%\help\ /E /Y

  FOR %%f IN (%TARGET_FILES%) DO (
    copy ..\%%f %OAM_PLUGIN_DIR%\%%f
  )

  ECHO Delete resources.py file
  del ..\resources.py
)
if "%1" == "derase" (
	ECHO under construction - derase
)
if "%1" == "doc" (
	ECHO Building help file in html format...
  REM CALL ..\help\make.bat html
)
if "%1" == "docclean" (
	ECHO Deleting help file...
  REM del ..\help\build /S /F /Q
)
