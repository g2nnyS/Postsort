<template>
  <div class="post-list">
    <div class="tag-header">
      <a-tag
        v-for="tag in Object.keys(tagColors)"
        :key="tag"
        :color="selectedTags.includes(tag) ? tagColors[tag] : 'default'"
        class="filter-tag"
        @click="toggleTag(tag)"
      >
        {{ tag }}
      </a-tag>
    </div>

    <div class="scrollable-content">
      <div v-if="loading" class="empty-state">
        <a-spin size="large" />
      </div>
      <template v-else>
        <div v-if="filteredPosts.length === 0" class="empty-state">
          <a-empty
            description="暂无数据"
            :image="Empty.PRESENTED_IMAGE_SIMPLE"
          />
        </div>
        <a-card 
          v-else
          v-for="post in filteredPosts" 
          :key="post.link"
          class="post-card"
          :bordered="false"
        >
          <div class="post-content">
            <div class="post-tag-column">
              <a-tag :color="tagColors[post.tag]" class="post-side-tag">{{ post.tag }}</a-tag>
            </div>
            <div class="post-main-content">
              <h3 class="post-title">
                <a :href="post.link" target="_blank">{{ post.title }}</a>
              </h3>
              <p class="post-description">{{ post.description }}</p>
              <div class="post-footer">
                <span class="post-time">{{ new Date(post.published).toLocaleString() }}</span>
                <a :href="post.link" target="_blank" class="post-link">{{ post.link }}</a>
              </div>
            </div>
          </div>
        </a-card>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { Empty } from 'ant-design-vue';
import axios from "axios";

interface Post {
  id: number;  // 添加 id 字段
  title: string;
  description: string;
  published: string;
  link: string;
  tag: string;
}

export default defineComponent({
  name: "PostList",
  setup() {
    const posts = ref<Post[]>([]);
    const loading = ref(true);
    
    const tagColors: Record<string, string> = {
      悬赏: "gold",
      出售: "blue",
      收购: "green",
      情报: "purple",
      曝光: "red",
      求助: "orange",
    };

    // 默认选中所有标签
    const selectedTags = ref<string[]>(Object.keys(tagColors));

    const toggleTag = (tag: string) => {
      const index = selectedTags.value.indexOf(tag);
      if (index === -1) {
        selectedTags.value.push(tag);
      } else {
        selectedTags.value.splice(index, 1);
      }
    };

    // 修改过滤逻辑
    const filteredPosts = computed(() => {
      const validPosts = posts.value
        .filter(post => Object.keys(tagColors).includes(post.tag))
        .sort((a, b) => b.id - a.id);  // 按 id 降序排序
      
      return selectedTags.value.length === 0
        ? validPosts
        : validPosts.filter((post) => selectedTags.value.includes(post.tag));
    });

    const fetchPosts = async () => {
      loading.value = true;
      try {
        const response = await axios.get<Post[]>("http://localhost:8000/posts");
        posts.value = response.data;
      } catch (error) {
        console.error("无法加载帖子数据:", error);
      } finally {
        loading.value = false;
      }
    };

    fetchPosts();

    return {
      posts,
      tagColors,
      filteredPosts,
      loading,
      Empty,
      selectedTags, // 添加到返回值中
      toggleTag,    // 添加到返回值中
    };
  },
});
</script>

<style scoped>
.post-list {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止整体滚动 */
}

.tag-header {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  padding: 16px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 16px 16px 0 0;
  display: flex;
  justify-content: center; /* 居中显示标签 */
  gap: 16px;
  z-index: 10;
  width: 100%; /* 确保标签栏占满宽度 */
  box-sizing: border-box; /* 防止padding导致宽度溢出 */
  flex-wrap: wrap; /* 允许标签换行 */
  overflow: visible; /* 移除滚动 */
}

/* 删除滚动条相关样式 */
/* 删除 .tag-header::-webkit-scrollbar 相关代码 */

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 24px; /* 增加内边距 */
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 60%; /* 将宽度从 70% 减小到 60% */
  margin: 0 auto; /* 居中显示 */
  min-height: 100%; /* 确保容器占满高度 */
  align-self: center; /* 确保内容区域居中 */
}

.filter-tag {
  cursor: pointer; /* 恢复指针样式 */
  user-select: none;
  padding: 0 16px;
  height: 32px;
  line-height: 32px;
  transition: all 0.3s; /* 添加过渡效果 */
}

.filter-tag:hover {
  opacity: 0.8;
}

.post-card {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  margin-bottom: 4px;
  padding: 24px; /* 增加内边距 */
  width: 100%;
}

.post-content {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.post-tag-column {
  flex-shrink: 0;
  width: 60px;
  display: flex;
  justify-content: center;
  padding-top: 4px;
}

.post-side-tag {
  width: 100%;
  text-align: center;
  padding: 4px 8px;
}

.post-main-content {
  flex: 1;
  min-width: 0;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.post-tag {
  flex-shrink: 0;
  font-size: 14px;
  padding: 0 8px;
}

.post-title {
  margin: 0;
  font-size: 18px;
  line-height: 1.5;
  flex: 1;
  min-width: 0;
}

.post-description {
  margin: 0;
  color: #666;
  font-size: 15px;
  line-height: 1.6;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}

.post-time {
  color: #999;
  white-space: nowrap; /* 保持时间在一行 */
}

.post-link {
  color: #1890ff;
  text-decoration: none;
  transition: opacity 0.2s;
  word-break: break-all; /* 允许链接在任意字符处换行 */
  font-family: monospace; /* 使用等宽字体 */
}

.post-link:hover {
  opacity: 0.8;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  width: 100%;
  flex: 1; /* 占满剩余空间 */
}

/* 为空状态下的内容添加样式 */
.empty-state :deep(.ant-empty) {
  margin: auto; /* 使用 margin:auto 确保在flex容器中完全居中 */
}

.footer-disclaimer {
  text-align: center;
  padding: 20px 0;
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
}

.footer-disclaimer p {
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .post-list {
    border-radius: 0;
    height: 100vh;
  }
  
  .tag-header {
    border-radius: 0;
  }

  .scrollable-content {
    width: 100%; /* 小屏幕时占满宽度 */
    padding: 16px;
  }
}

@media (orientation: portrait) {
  /* 竖屏样式 */
  .post-list {
    border-radius: 0;
  }
  
  .tag-header {
    border-radius: 0;
  }

  .scrollable-content {
    width: 85%; /* 竖屏时稍微调整宽度 */
  }
}

@media (orientation: landscape) and (max-height: 768px) {
  /* 横屏但高度较小时的样式 */
  .tag-header {
    padding: 12px;
  }
  
  .scrollable-content {
    padding: 16px;
  }
  
  .post-title {
    font-size: 16px;
  }
}

@media (orientation: landscape) {
  .tag-header {
    padding: 20px 40px;
    gap: 20px; /* 增加标签间距 */
    width: 100%; /* 确保横屏时也是全宽 */
  }
  
  .scrollable-content {
    width: 60%; /* 横屏模式下也保持 60% 宽度 */
    padding: 32px 0; /* 修改内边距，保持两侧留白 */
  }
  
  .post-card {
    padding: 24px; /* 减小卡片内边距 */
  }
  
  .post-content {
    gap: 24px; /* 减小内容间距 */
  }
  
  .post-tag-column {
    width: 70px; /* 横屏时适当增加宽度 */
  }
  
  .post-side-tag {
    font-size: 15px;
    padding: 6px 10px;
  }
  
  .post-tag {
    font-size: 15px;
    padding: 0 12px;
  }
  
  .post-title {
    font-size: 20px; /* 墽大标题字号 */
    margin-bottom: 16px;
  }
  
  .post-description {
    font-size: 16px; /* 墽大描述文字字号 */
    line-height: 1.8;
    margin-bottom: 20px;
  }
  
  .post-footer {
    font-size: 14px;
  }

  .filter-tag {
    padding: 0 20px; /* 横屏时增加标签内部空间 */
    height: 36px; /* 横屏时增加标签高度 */
    line-height: 36px;
    font-size: 16px; /* 墽大标签字号 */
  }

  .post-main-content {
    max-width: 100%;
  }

  .footer-disclaimer {
    padding: 24px 0;
    font-size: 15px;
  }
}

/* 针对超宽屏幕的优化 */
@media (min-width: 1920px) {
  .post-title {
    font-size: 22px;
  }
  
  .post-description {
    font-size: 17px;
  }
  
  .scrollable-content {
    padding: 40px;
  }
}
</style>
