<template>
    <el-sub-menu v-if="item.children" :index="item.index">
      <template #title>
        <el-icon :class="item.icon" />
        <span>{{ item.title }}</span>
      </template>
      <el-menu-item
        v-for="child in item.children"
        :key="child.index"
        :index="child.index"
        @click="$emit('item-clicked', child.index)"
      >
        <el-icon :class="child.icon" />
        {{ child.label }}
      </el-menu-item>
    </el-sub-menu>
  </template>
  
  <script lang="ts" setup>
  import { defineProps, toRefs } from 'vue';
  
  const props = defineProps({
    item: Object,
    activeIndex: String,
  });
  
  const { item } = toRefs(props);
  </script>