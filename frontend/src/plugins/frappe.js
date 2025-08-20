import { FrappeApp } from 'frappe-js-sdk'

// If you proxy / are on same origin, this can be your site origin.
// Otherwise put the full URL to your Frappe site:
export const frappe = new FrappeApp(import.meta.env.VITE_FRAPPE_URL)
