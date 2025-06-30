// stores/auth.js
import { defineStore } from 'pinia'
import { supabase } from '../services/supabase'// Assicurati di esportare un client Supabase

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: true,
    loading: false,
    error: null
  }),

  actions: {
    async init() {
      this.loading = true
      try {
        const { data, error } = await supabase.auth.getSession()
        if (error) throw error

        this.user = data.session?.user || null
      } catch (err) {
        this.error = err.message
        this.user = null
      } finally {
        this.loading = false
      }
    },

    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password
        })
        if (error) throw error

        this.user = data.user
        this.isAuthenticated = true
        return true

      } catch (err) {
        this.error = err.message
        return false

      } finally {
        this.loading = false
      }
    },

    async signUp(email, password) {
      this.loading = true
      this.error = null
      try {
        const { data, error } = await supabase.auth.signUp({
          email,
          password
        })
        if (error) throw error

        this.user = data.user
        this.isAuthenticated = true
        return true

      } catch (err) {
        this.error = err.message
        return false

      } finally {
        this.loading = false
      }
    },

    async logout() {
      await supabase.auth.signOut()
      this.isAuthenticated = false
      this.user = null
    }
  }
})
