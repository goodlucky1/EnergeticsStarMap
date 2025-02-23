import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: "home",
      path: "/",
      redirect: "/login"
    },
    {
      name: "loginpage",
      path: "/login",
      component: () => import('@/views/init/Login.vue')
    },
    {
      name: "registerpage",
      path: "/register",
      component: () => import('@/views/init/Registry.vue')
    },
    {
      name: "homepage",
      path: "/home",
      component: () => import('@/views/home/HOME.vue'),
      meta: {
        rolelevel: 1,
        metaname: "首页",
        isitem:true
      },
      children: [
        //角色管理的路由
        {
          name: "userpage",
          path: "user",
          meta: {
            rolelevel: 10,
            metaname: "角色管理",
            isitem:true
          },
          children: [
            {
              name: "usercontrolpage",
              path: "usercontrol",
              component: () => import('@/views/user/UserControl.vue'),
              meta: {
                rolelevel: 100,
                rolename: "管理员",
                metaname: "用户管理",
                isitem:false
              }
            },
            {
              name: "studentcontrolpage",
              path: "studentcontrol",
              component: () => import('@/views/user/StudentControl.vue'),
              meta: {
                rolelevel: 10,
                rolename: "教师",
                metaname: "学生管理",
                isitem:false
              }
            },
            {
              name: "hometest1",
              path: "hometest1",
              component: () => import('@/views/init/Login.vue'),
              meta: {
                rolelevel: 10,
                rolename: "教师",
                metaname: "学生管理1",
                isitem:false
              }
            },
            {
              name: "hometest2",
              path: "hometest2",
              component: () => import('@/views/init/Registry.vue'),
              meta: {
                rolelevel: 10,
                rolename: "教师",
                metaname: "学生管理223132",
                isitem:false
              }
            }
          ]
        },
        {
          name: "datashowpage",
          path: "datashow",
          meta: {
            rolelevel: 1,
            metaname: "数据显示",
            isitem:true
          },
          children: [
            {
              name: "studentdatashowpage",
              path: "studentdatashow",
              meta: {
                rolelevel: 100,
                metaname: "学生数据",
                isitem:false
              },
              component: () => import('@/views/datashow/StudentDataShow.vue')
            },
            {
              name: "teacherstudentdatashowpage",
              path: "teacherstudentdatashow",
              meta: {
                rolelevel: 10,
                metaname: "你的学生数据",
                isitem:false
              },
              component: () =>
                import('@/views/datashow/TeacherStudentDataShow.vue')
            },
            {
              name: "stueddatashowpage",
              path: "stueddatashow",
              meta: {
                rolelevel: 1,
                metaname: "你的数据",
                isitem:false
              },
              component: () => import('@/views/datashow/stueddatashow.vue')
            }
          ]
        },
        {
          name: "datacontrolpage",
          path: "datacontrol",
          meta: {
            rolelevel: 10,
            metaname: "数据管理",
            isitem:true
          },
          children: [
            {
              name: "studentdatacontrolpage",
              path: "studentdatacontrol",
              meta: {
                rolelevel: 100,
                metaname: "学生数据",
                isitem:false
              },
              component: () =>
                import('@/views/datacontrol/StudentDataControl.vue')
            },
            {
              name: "teacherstudentdatacontrolpage",
              path: "teacherstudentdatacontrol",
              meta: {
                rolelevel: 10,
                metaname: "你的学生数据",
                isitem:false
              },
              component: () =>
                import('@/views/datacontrol/TeacherStudentDataControl.vue')
            }
          ]
        },
        {
          name: "appraisecontrolpage",
          path: "appraisecontrol",
          meta: {
            rolelevel: 1,
            metaname: "评价系统",
            isitem:true
          },
          children: [
            {
              name: "studentappraisepage",
              path: "studentappraise",
              meta: {
                rolelevel: 100,
                metaname: "学生评价",
                isitem:false
              },
              component: () => import('@/views/appraise/StudentAppraise.vue')
            },
            {
              name: "teacherstudentappraisepage",
              path: "teacherstudentappraise",
              meta: {
                rolelevel: 10,
                metaname: "你的学生评价",
                isitem:false
              },
              component: () =>
                import('@/views/appraise/TeacherStudentAppraise.vue')
            },
            {
              name: "stuselfappraisepage",
              path: "stuselfappraise",
              meta: {
                rolelevel: 1,
                metaname: "你的评价",
                isitem:false
              },
              component: () => import('@/views/appraise/StudentSelfAppraise.vue')
            }
          ]
        }
      ]
    }
  ]
});

export default router;