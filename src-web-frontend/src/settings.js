// Replaced by WebPack
const IS_DEV = process.env.NODE_ENV === 'development'
const IS_PRODUCTION = process.env.NODE_ENV === 'production'

let settings = {
  API_BASE_URL: null,
  WEBSOCKET_URL: null
}

if (IS_DEV) {
  settings.API_BASE_URL = 'http://0.0.0.0:5000'
  settings.WEBSOCKET_URL = `ws://0.0.0.0:5000/ws`
} else if (IS_PRODUCTION) {
  throw new Error('Not yet implemented')
  // settings.API_BASE_URL = 'https://www.python-boilerplate.com'
}

// console.log(settings)

export const API_BASE_URL = settings.API_BASE_URL
export const WEBSOCKET_URL = settings.WEBSOCKET_URL
