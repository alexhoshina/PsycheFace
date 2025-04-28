// plugins/gsap.js
import { defineNuxtPlugin } from '#app'
import { gsap } from 'gsap'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.provide('gsap', gsap)
  nuxtApp.provide('gsap', gsap)
})