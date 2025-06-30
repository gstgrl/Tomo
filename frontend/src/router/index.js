import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../services/supabase'
import { useAuthStore } from '../stores/auth'
import HomePage from '../views/home/HomePage.vue'
import LoginPage from '../views/auth/LoginPage.vue'
import SignInpage from '../views/auth/SignInpage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage, meta: { requiresAuth: false }},
  { path: '/login', name: 'Login', component: LoginPage, meta: { requiresAuth: false }},
  { path: '/registration', name: 'Sign-in', component: SignInpage, meta: { requiresAuth: false }},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // Assicura che lo store abbia l'informazione dell'utente da Supabase
  if (auth.user === null) {
    await auth.init()
  }

  const session = supabase.auth.getSession ? (await supabase.auth.getSession()).data.session : null

  // Verifica se la rotta richiede login
  if (to.meta.requiresAuth && !session?.user) {
    return { name: 'Login' }
  }

  // Evita accesso a login se sei già loggato
  if (to.name === 'Login' && session?.user) {
    return { name: 'Home' }
  }
})

export default router
