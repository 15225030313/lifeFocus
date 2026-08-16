import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('lf_token') || '')
  const username = ref(localStorage.getItem('lf_user') || '')

  function set(t: string, u: string) {
    token.value = t
    username.value = u
    localStorage.setItem('lf_token', t)
    localStorage.setItem('lf_user', u)
  }
  function logout() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('lf_token')
    localStorage.removeItem('lf_user')
  }
  return { token, username, set, logout }
})
