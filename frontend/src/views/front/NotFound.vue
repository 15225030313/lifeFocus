<template>
  <div class="not-found rise-in">
    <div class="code">404</div>
    <h2>这一页似乎不存在</h2>
    <p>链接可能已失效，或者内容被搬去了别处。</p>
    <router-link to="/">
      <el-button type="primary" round size="large">回到首页</el-button>
    </router-link>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: 110px 24px 90px;
}
.code {
  font-family: Georgia, serif;
  font-style: italic;
  font-size: 110px;
  font-weight: 800;
  line-height: 1;
  background: linear-gradient(135deg, var(--primary) 0%, #6ec9bf 60%, var(--gold) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 20px;
}
h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 10px;
}
p {
  color: var(--ink-3);
  margin: 0 0 30px;
  font-size: 14.5px;
}
</style>
