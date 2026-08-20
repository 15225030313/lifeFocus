<template>
  <div class="empty-state">
    <svg class="art" viewBox="0 0 200 140" fill="none">
      <ellipse cx="100" cy="118" rx="72" ry="10" fill="#eceae3" />
      <rect x="55" y="38" width="90" height="66" rx="8" fill="#fff" stroke="#ddd8cc" stroke-width="2" />
      <rect x="67" y="52" width="44" height="6" rx="3" fill="#ddd8cc" />
      <rect x="67" y="66" width="66" height="5" rx="2.5" fill="#e8e4db" />
      <rect x="67" y="78" width="56" height="5" rx="2.5" fill="#e8e4db" />
      <circle cx="148" cy="34" r="14" fill="var(--primary-soft)" />
      <path d="M143 34l4 4 7-8" stroke="var(--primary)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
    <p class="text">{{ text }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{ text?: string }>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 72px 0;
}
.art {
  width: 180px;
  margin-bottom: 18px;
}
.text {
  color: var(--ink-3);
  font-size: 14.5px;
  letter-spacing: 0.5px;
  margin: 0 0 16px;
}
</style>
