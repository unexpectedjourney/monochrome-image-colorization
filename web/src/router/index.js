import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../components/auth/Login.vue'
import Registration from '../components/auth/Registration.vue'
import Logout from '../components/auth/Logout.vue'
import ImageEditor from '../components/ImageEditor.vue'
import Images from '../components/Images.vue'
import ImageComponent from "../components/ImageInfo";
import Versions from "../components/versioning/Versions";
import UserProfile from "../components/UserProfile";
import UserHistory from "../components/history/UserHistory";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
        meta: {
            requiresVisitor: true,
        }
    },
    {
        path: '/register',
        name: 'register',
        component: Registration,
        meta: {
            requiresVisitor: true,
        }
    },
    {
        path: '/logout',
        name: 'logout',
        component: Logout
    },
    {
        path: '/editor/:file_id?',
        name: 'image_editor',
        component: ImageEditor,
        props: true,
        meta: {
            requiresAuth: true,
        }
    },
    {
        path: '/images',
        name: 'images',
        component: Images,
        meta: {
            requiresAuth: true,
        }
    },
    {
        path: '/images/:id',
        name: 'image',
        component: ImageComponent,
        props: true,
        meta: {
            requiresAuth: true,
        }
    },
    {
        path: '/images/:id/versions',
        name: 'versions',
        component: Versions,
        props: true,
        meta: {
            requiresAuth: true,
        }
    },
    {
        path: '/user_profile',
        name: 'user_profile',
        component: UserProfile,
        meta: {
            requiresAuth: true,
        }
    },
    {
        path: '/user_history',
        name: 'user_history',
        component: UserHistory,
        meta: {
            requiresAuth: true,
        }
    },
]

const router = new VueRouter({
    mode: 'history',
    // base: process.env.BASE_URL,
    routes
})

export default router
