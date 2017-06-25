from pymitter import EventEmitter

EVENT_RFID_TAG_DETECTED = "rfid_detected"
EVENT_RFID_TAG_REMOVED = "rfid_tag_removed"

EVENT_UPDATE_AVAILABLE = "update_available"
EVENT_UPDATE_EXECUTE = "update_execute"
EVENT_UPDATE_STATUS = "update_status"

ee = EventEmitter()
