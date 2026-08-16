<template>
  <div class="empty">
    <el-icon class="icon"><DocumentDelete /></el-icon>
    <p>{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ text?: string }>()
</script>

<style scoped>
.empty {
  text-align: center;
  padding: 60px 0;
  color: var(--text-3);
}
.icon {
  font-size: 48px;
  margin-bottom: 12px;
}
.empty p {
  font-size: 14px;
}
</style>
