import Vue from 'vue'

export const EVENT_RFID_DETECTED = 'rfid_detected'
export const EVENT_DOWNLOAD_PROGRESS = 'download_progress'
export const EVENT_DOWNLOAD_STATE = 'download_state'

const eventHub = new Vue()
export default eventHub
