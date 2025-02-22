<template>
  <el-row class="tac">
    <el-col :span="12">
      <el-menu :collapse="isCollapsed" :collapse-transition="true" class="el-menu-vertical-demo el_menu"
        active-text-color="#ffd04b" unique-opened background-color="#112f50" text-color="#fff" @open="handleOpen" @close="handleClose"
        @select="handleSelect">

        <el-menu-item class="top">
          <template #title>
            <span class="title-text">学生管理系统</span>
          </template>
        </el-menu-item>

        <el-sub-menu index="1">
          <template #title>
            <el-icon>
              <User />
            </el-icon>
            <span>角色管理</span>
          </template>
          <el-menu-item-group title="管理员">
            <el-menu-item index="usercontrolpage">&nbsp;&nbsp;用户管理</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="教师">
            <el-menu-item index="studentcontrolpage">&nbsp;&nbsp;学生管理</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon>
              <Histogram />
            </el-icon>
            <span>数据显示</span>
          </template>
          <el-menu-item-group title="管理员">
            <el-menu-item index="studentdatashowpage">&nbsp;&nbsp;学生数据</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="教师">
            <el-menu-item index="teacherstudentdatashowpage">&nbsp;&nbsp;您的学生数据</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="学生">
            <el-menu-item index="stueddatashowpage">&nbsp;&nbsp;您的数据</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <el-icon>
              <Tools />
            </el-icon>
            <span>数据管理</span>
          </template>
          <el-menu-item-group title="管理员">
            <el-menu-item index="studentdatacontrolpage">&nbsp;&nbsp;学生数据</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="教师">
            <el-menu-item index="teacherstudentdatacontrolpage">&nbsp;&nbsp;您的学生数据</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon>
              <EditPen />
            </el-icon>
            <span>评价管理</span>
          </template>
          <el-menu-item-group title="管理员">
            <el-menu-item index="studentappraisepage">&nbsp;&nbsp;学生评价数据</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="教师">
            <el-menu-item index="teacherstudentappraisepage">&nbsp;&nbsp;教师评价</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="学生">
            <el-menu-item index="stuselfappraisepage">&nbsp;&nbsp;学生自评</el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>








        <!-- 添加测试菜单项 -->
        <el-menu-item index="hometest1">Home Test 1</el-menu-item>
        <el-menu-item index="hometest2">Home Test 2</el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import {
  Location,
  User,
  Histogram,
  Tools,
  EditPen
} from '@element-plus/icons-vue';
const props = defineProps(["isCollapsed"]);
const router = useRouter();

const isCollapsed = ref(false);

watch(() => props.isCollapsed, (val) => {
  isCollapsed.value = val;
});

const isshow = ref({

})

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};

const handleSelect = (key, keyPath) => {
  router.push({ name: key });
};


</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.el_menu {
  border-right: none;
}

.top {
  background-color: #000;
  font-size: 20px;
  text-align: center;
  padding: 16px 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.top:hover {
  background-color: #1a3d59;
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.title-text {
  color: #ffd04b;
  font-weight: bold;
  transition: color 0.3s ease;
}

.top:hover .title-text {
  color: #fff;
}
</style>
