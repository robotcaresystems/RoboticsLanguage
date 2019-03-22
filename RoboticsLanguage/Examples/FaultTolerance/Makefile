
all:
	rol messages.rol
	rol fault_detection_topics.fdt
	rol fault_detection_heartbeat.fdh
	rol fault_handler.rol
	rol failure_handler.rol
	rol fault_tolerance_system.fts

gui:
	rol messages.rol -o HTMLGUI RosCpp
	rol fault_detection_topics.fdt -o HTMLGUI RosCpp
	rol fault_detection_heartbeat.fdh -o HTMLGUI RosCpp
	rol fault_handler.rol -o HTMLGUI RosCpp
	rol failure_handler.rol -o HTMLGUI RosCpp
	rol fault_tolerance_system.fts -o HTMLGUI RosCpp


launchgui:
	rol messages.rol -lo HTMLGUI RosCpp
	rol fault_detection_topics.fdt -lo HTMLGUI RosCpp
	rol fault_detection_heartbeat.fdh -lo HTMLGUI RosCpp
	rol fault_handler.rol -lo HTMLGUI RosCpp
	rol failure_handler.rol -lo HTMLGUI RosCpp
	rol fault_tolerance_system.fts -lo HTMLGUI RosCpp

compilegui:
	rol messages.rol -co HTMLGUI RosCpp
	rol fault_detection_topics.fdt -co HTMLGUI RosCpp
	rol fault_detection_heartbeat.fdh -co HTMLGUI RosCpp
	rol fault_handler.rol -co HTMLGUI RosCpp
	rol failure_handler.rol -co HTMLGUI RosCpp
	rol fault_tolerance_system.fts -co HTMLGUI RosCpp

compile:
	rol messages.rol -c
	rol fault_detection_topics.fdt -c
	rol fault_detection_heartbeat.fdh -c
	rol fault_handler.rol -c
	rol failure_handler.rol -c
	rol fault_tolerance_system.fts -c
