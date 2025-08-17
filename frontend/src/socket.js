import { io } from "socket.io-client"
import { socketio_port } from "../../../../sites/common_site_config.json"

let socket = null

export function initSocket() {
    const host = window.location.hostname
    const siteName = window.site_name
    const protocol = window.location.protocol === "https:" ? "https" : "http"
    const port = socketio_port ? `:${socketio_port}` : ""
    
    // إذا السيرفر ما يحتاج مسار مخصص، لا تضيف /siteName
    const url = `${protocol}://${host}${port}`

    socket = io(url, {
        path: `/${siteName}`, // إذا فعلاً السيرفر يستخدم namespace بهذا الاسم
        withCredentials: true,
        reconnectionAttempts: 5,
        transports: ["websocket"], // يقلل مشاكل الـ polling
    })

    return socket
}

export function useSocket() {
    return socket
}
