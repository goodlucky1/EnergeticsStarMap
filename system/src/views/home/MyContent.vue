<template>
  <div>
    <div class="header">
      <div class="breadcrumb">
      <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item v-for="item in $route.matched" :key="item.path" :to="item.path">{{ item.meta.metaname }}</el-breadcrumb-item>
      </el-breadcrumb>
      </div>

      <div class="icon" @click="toggleMenu">
        <el-icon v-if="isMenuOpen">
          <Fold />
        </el-icon>
        <el-icon v-else>
          <Expand />
        </el-icon>
      </div>

      <div class="tabs">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick" @tab-remove="removeTab">
          <el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name"
            :closable="true"></el-tab-pane>
        </el-tabs>
      </div>
      <div class="right">
        <div class="time">
          {{ time }}
        </div>
        <div class="line">|</div>
        <div class="loginout" @click="out">
          <el-icon>
            <SwitchButton />
          </el-icon>
        </div>
      </div>
    </div>

    <div class="wrapper">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import dayjs from 'dayjs';
import { useRouter, useRoute } from 'vue-router';
import { Expand, Fold, SwitchButton ,ArrowRight } from '@element-plus/icons-vue';

const props = defineProps(["isClose"]);
const emit = defineEmits(["change"]);

let time = ref(null);
const router = useRouter();
const route = useRoute();
const tabs = ref([]);
const activeTab = ref(route.name);
const isMenuOpen = ref(true);

const change = () => {
  emit("change");
};

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
  change();
};

onMounted(() => {
  time.value = dayjs(new Date()).format('YYYY-MM-DD HH:mm:ss');
  setInterval(() => {
    time.value = dayjs(new Date()).format('YYYY-MM-DD HH:mm:ss');
  }, 1000);

  if(localStorage.getItem('isbeforeunload')){
    localStorage.removeItem('isbeforeunload');
    tabdata(route);
  }
});

watch(route, (newRoute,old) => {
      console.log(route, newRoute,old);
      tabdata(newRoute);
});

const tabdata= (newRoute)=>{
  if (newRoute.meta.metaname&&!newRoute.meta.isitem) {
    if (!tabs.value.find(tab => tab.name === newRoute.name)) {
      tabs.value.push({
        name: newRoute.name,
        label: newRoute.meta.metaname
      });
    }
    activeTab.value = newRoute.name;
  }
}

//刷新操作
window.addEventListener('beforeunload', function(event) {
  localStorage.setItem('isbeforeunload', true);
  alert('刷新');
});

const handleTabClick = (tab) => {
  router.push({ name: tab.props.name });
};

const removeTab = (tabName) => {
  const index = tabs.value.findIndex(tab => tab.name === tabName);
  if (index !== -1) {
    tabs.value.splice(index, 1);
    if (activeTab.value === tabName) {
      activeTab.value = tabs.value.length ? tabs.value[0].name : null;
      if (activeTab.value) {
        router.push({ name: activeTab.value });
      }
    }
  }
};

const out = () => {
  router.push("/login");
};
</script>

<style lang="less" scoped>

:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner, .el-breadcrumb__item:last-child .el-breadcrumb__inner a, .el-breadcrumb__item:last-child .el-breadcrumb__inner a:hover, .el-breadcrumb__item:last-child .el-breadcrumb__inner:hover ){
  color: rgb(143, 7, 7);
  font-size: 18px;
  line-height: 9px;
}
:deep(.el-breadcrumb__inner.is-link){
  font-style: oblique;
  
}
:deep(.el-tabs__item){
  font-weight: bold;
}

.header {
  height: 80px;
  line-height: 80px;
  background-color: #1e78bf;
  color: #fff;
  display: flex;
  position: relative;

  .icon {
    font-size: 24px;
    flex: 1;
    width: 20px;
    height: 20px;

    i {
      cursor: pointer;
    }
  }

  .breadcrumb {
    flex: 8;
    height: 20px;
    display: flex;
    padding-left: 0px;
    position: absolute;
    left: 50px;
    top: 10px;

  }

  .tabs {
    margin-top: 25px;
    flex: 8;

    .el-tabs__nav {
      justify-content: flex-start;
    }
  }

  .right {
    padding-right: 20px;
    display: flex;

    .time {
      font-size: 12px;
    }

    .line {
      padding-left: 10px;
      padding-right: 10px;
    }

    .loginout {
      margin-top: 2px;
    }
  }
}

.wrapper {
  margin: 10px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>