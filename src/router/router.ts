import { createRouter, createWebHashHistory } from "vue-router";
import Msgtable from '../components/msgtable.vue'
import Login from '../components/login.vue'

const routes = [
    { path: '/', name: "App", component: Msgtable },
    { path: '/Login', name: "Login", component: Login },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})


export default router