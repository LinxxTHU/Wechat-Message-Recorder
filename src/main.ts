import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router'
import { Md5 } from "ts-md5"
import { PASSWORD_UPPER_MD5 } from './constants/strings'

router.beforeEach(async (to, from) => {
    const token = window.localStorage.getItem("access_token");
    if (from.name === to.name)
        return false;
    if (to.name !== 'Login' && (token===null || Md5.hashStr(token).toUpperCase() !== PASSWORD_UPPER_MD5)) {
        return { name: 'Login' };
    }
})

createApp(App).use(router).mount('#app')
