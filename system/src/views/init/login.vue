<template>
    <div class="login-container">
        <div class="background" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
        <el-card class="login-card" shadow="hover" style="background-color: #ffffff; border-radius: 15px; border: 1px solid #ccc; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); width: 500px; padding: 30px;">
            <h2 class="login-title" style="color: #2c3e50;">登录</h2>
            <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="auto" >
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="loginForm.username" placeholder="请输入用户名" clearable></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="loginForm.password" placeholder="请输入密码" show-password></el-input>
                </el-form-item>
                <el-form-item v-if="showCaptcha" label="验证码" prop="captcha">
                    <div style="display: flex; align-items: center;">
                        <el-input v-model="loginForm.captcha" placeholder="请输入验证码" clearable style="flex: 1; margin-right: 10px;" @focus="focusCaptcha"></el-input>
                        <canvas ref="captchaCanvas" class="captcha-img" @click="refreshCaptcha" style="flex: none;"></canvas>
                    </div>
                    <el-button link @click="refreshCaptcha" style="margin-top: 10px;">看不清，换一张</el-button>
                    <div v-if="captchaError" style="color: red; margin-top: 5px;">验证码错误，请重新输入</div>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleLogin" block>登录</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button link @click="goToRegister" block>没有账号？去注册</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="js">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const loginForm = ref({
    username: '',
    password: '',
    captcha: ''
});
const showCaptcha = ref(false);
const captchaSrc = ref('');
const captchaError = ref(false);
const loginAttempts = ref(0);
const loginFormRef = ref(null);
const captchaCanvas = ref(null);

const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '用户名长度不能小于3个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
    ],
    captcha: [
        { required: true, message: '请输入验证码', trigger: 'blur' }
    ]
};

const refreshCaptcha = () => {
    captchaSrc.value = generateCaptcha();
    drawCaptcha(captchaSrc.value);
};

const focusCaptcha = () => {
    captchaError.value = false;
}

const generateCaptcha = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let captcha = '';
    for (let i = 0; i < 6; i++) {
        captcha += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return captcha;
};

const drawCaptcha = (captcha) => {
    const canvas = captchaCanvas.value;
    const ctx = canvas.getContext('2d');
    canvas.width = 150;
    canvas.height = 50;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw background lines
    for (let i = 0; i < 15; i++) { // 增加干扰线数量
        ctx.beginPath();
        ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
        ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
        ctx.strokeStyle = `rgba(0, 0, 0, ${Math.random()})`; // 增加干扰线的透明度
        ctx.lineWidth = 1 + Math.random(); // 增加干扰线的宽度
        ctx.stroke();
    }

    // Draw captcha text
    ctx.font = '24px Arial';
    ctx.fillStyle = '#000';
    for (let i = 0; i < captcha.length; i++) {
        const char = captcha.charAt(i);
        ctx.save();
        ctx.translate(20 + i * 20, 30);
        ctx.rotate(Math.random() * 0.5 - 0.25); // 随机旋转字符
        ctx.fillText(char, 0, 0);
        ctx.restore();
    }

    // Draw noise dots
    for (let i = 0; i < 50; i++) {
        ctx.beginPath();
        ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, 1, 0, 2 * Math.PI);
        ctx.fillStyle = `rgba(0, 0, 0, ${Math.random()})`;
        ctx.fill();
    }
};

const handleLogin = () => {
    loginFormRef.value.validate((valid) => {
        if (valid) {
            if (showCaptcha.value && loginForm.value.captcha.toLowerCase() != captchaSrc.value.toLowerCase()) {
                captchaError.value = true;
                refreshCaptcha();
                return;
            }
            axios.post('/api/login', loginForm.value)
                .then(response => {
                    // handle successful login
                })
                .catch(error => {
                    loginAttempts.value++;
                    if (loginAttempts.value >= 2) {
                        showCaptcha.value = true;
                        refreshCaptcha();
                    }
                });
        }
    });
};

const goToRegister = () => {
    router.push({name:"registerpage"});
};

onMounted(() => {
    if (showCaptcha.value) {
        refreshCaptcha();
    }
});
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('@/assets/img/渐变背景.671bea90.jpg');
    background-size: cover;
    background-position: center;
    margin: 0; /* Ensure no margin around the container */
    overflow: hidden; /* Prevent scrollbar */
}

.login-card {
    width: 400px;
    padding: 20px;
    box-shadow: none; /* Remove any box shadow */
}

.login-title {
    text-align: center;
    margin-bottom: 20px;
}

.captcha-img {
    cursor: pointer;
    margin-top: 10px;
    border: 1px solid #ccc;
    display: block;
}
</style>
