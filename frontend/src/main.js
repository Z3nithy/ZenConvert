import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import './assets/styles/main.css'
import { initializeTheme } from './composables/useTheme'

const app = createApp(App)

initializeTheme()
app.use(router)

app.mount('#app')
