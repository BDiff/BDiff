<script setup lang="ts"></script>

<template>
  <router-view />

  <footer>
    <div class="mt-5 mb-3 d-flex gap-3 justify-content-center">
      <a href="https://beian.miit.gov.cn/" class="link-secondary">湘ICP备2024083800号</a>
      <router-link to="/security-policy" class="link-secondary">Security Policy</router-link>
    </div>
  </footer>
</template>
