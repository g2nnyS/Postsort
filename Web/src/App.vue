<template>
  <div id="app" :style="backgroundStyle">
    <div class="content-container">
      <div class="post-list-wrapper">
        <PostList />
      </div>
    </div>
    <div class="footer-disclaimer">
      <p>2024 王小美 Ganyu · 页面内容来自其它论坛，作者不对其内容负责。分类标签仅供参考</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import PostList from "./PostList.vue";

export default defineComponent({
  name: "App",
  components: {
    PostList,
  },
  setup() {
    // 这里可以从本地存储或配置中读取背景图片URL
    const backgroundImage = ref("/bg.webp"); // 替换为默认背景图URL

    const backgroundStyle = computed(() => ({
      backgroundImage: `url(${backgroundImage.value})`,
    }));

    return {
      backgroundStyle,
    };
  },
});
</script>

<style>
#app {
  min-height: 100vh;
  width: 100vw;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 防止出现滚动条 */
  margin: 0;
  padding: 0;
}

.content-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0; /* 移除内边距 */
}

.post-list-wrapper {
  width: 95%;
  height: 95vh;
}

.footer-disclaimer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
  padding: 16px 0;
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
}

.footer-disclaimer p {
  margin: 0;
  line-height: 1.5;
}

@media (orientation: portrait) {
  /* 竖屏样式 */
  .post-list-wrapper {
    width: 100%;
    height: 100vh;
    max-height: 100vh;
  }
  
  #app {
    padding: 0;
  }
}

@media (orientation: landscape) {
  /* 横屏样式 */
  .post-list-wrapper {
    width: calc(95vh * 16 / 9); /* 根据16:9比例计算宽度 */
    max-width: 95%; /* 防止在超宽屏幕上过宽 */
    height: 95vh;
  }

  @media (min-aspect-ratio: 16/9) {
    /* 当屏幕比例超过16:9时 */
    .post-list-wrapper {
      width: calc(95vh * 16 / 9);
      height: 95vh;
    }
  }

  @media (max-aspect-ratio: 16/9) {
    /* 当屏幕比例小于16:9时 */
    .post-list-wrapper {
      width: 95vw;
      height: calc(95vw * 9 / 16);
    }
  }
}

/* 超宽屏幕优化 */
@media (min-width: 2560px) {
  .post-list-wrapper {
    max-width: 2000px; /* 限制最大宽度 */
  }
}
</style>