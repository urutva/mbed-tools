APP_DMG_NAME=Mbed_tools.dmg
DIST_DIR=dist

all:	${APP_DMG_NAME}

clean:
	rm -rf ${DIST_DIR}

mbed-tools.spec:
	pyinstaller --distpath ${DIST_DIR} --hidden-import='pkg_resources.py2_warn' ../mbed_tools/cli.py --name mbed-tools

${DIST_DIR}:
	pyinstaller --distpath ${DIST_DIR} mbed_tools.spec

${APP_DMG_NAME}:	${DIST_DIR} dmg_settings.py
	dmgbuild -s dmg_settings.py "Mbed Tools Installer" ${APP_DMG_NAME}
	echo "Created ${APP_DMG_NAME}"
