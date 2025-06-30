import { createApp } from 'vue'
import { createPinia } from 'pinia'
// Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser, faLock, faEnvelope, faEyeSlash, faEye } from '@fortawesome/free-solid-svg-icons'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Aggiungile alla libreria
library.add(faUser, faLock, faEnvelope, faEyeSlash, faEye)

const app = createApp(App)

// Registra il componente globalmente
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(createPinia())
app.use(router)

app.mount('#app')
