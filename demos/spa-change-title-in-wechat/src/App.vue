<template>
    <div id="app">
        <ol style="text-align: left;">
            <li>请在微信端运行此程序</li>
            <li>点击下方的导航菜单改变当前展现的页面</li>
            <li>观察微信导航栏当前页面的标题</li>
            <li>兼容 iOS 端微信的 UIWebView 和 WKWebView</li>
        </ol>
        <div style="margin-top: 60px;">
            <router-link to="/">Home</router-link>
            <router-link to="/articles">Articles</router-link>
            <div class="router-view">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
<script>
  export default {
    name: 'App'
  }
</script>
<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }

    .router-view {
        margin-top: 30px;
    }
</style>
