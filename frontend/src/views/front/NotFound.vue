<template>
  <div class="not-found">
    <div class="code">404</div>
    <p>哎呀，页面走丢了～</p>
    <router-link to="/"><el-button type="primary">返回首页</el-button></router-link>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: 80px 0;
}
.code {
  font-size: 72px;
  font-weight: 800;
  color: var(--primary);
}
.not-found p {
  color: var(--text-3);
  margin: 12px 0 24px;
}
</style>
