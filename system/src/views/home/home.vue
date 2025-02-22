<template>
  <div>
    <div id="mymenudiv" class="menu" :class="{menu1:isMenuCollapsed}">
      <MyMenu :is-collapsed="isMenuCollapsed"></MyMenu>
    </div>
    <div class="content" :class="{ expanded: isMenuCollapsed }">
      <MyContent @change="toggleMenu"></MyContent>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import MyMenu from './MyMenu.vue';
import MyContent from './MyContent.vue';

const isMenuCollapsed = ref(false);
const toggleMenu = () => {
  isMenuCollapsed.value = !isMenuCollapsed.value;
  const div = document.getElementById('mymenudiv');
  div.classList.toggle('menu2');
  div.classList.toggle('menu1');
  
};
</script>

<style lang="less" scoped>
@import "../../assets/css/base.css";
.menu {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  background-color: #112f50;
  transition: width 0.5s;
  width: 200px;
  &.menu1 {
    width: 64px;
  }
}

.content {
  padding-left: 200px;
  transition: padding-left 0.45s;
  &.expanded {
    padding-left: 64px; /* 调整为简化显示时的宽度 */
  }
}
</style>