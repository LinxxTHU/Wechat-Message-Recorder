<template>
    <h1>Login</h1>
    <p><el-input v-model="pswd" style="width: 300px;" /></p>
    <p><el-button type="primary" @click="auth(pswd)">Submit</el-button></p>
</template>

<script setup lang="ts">
import { Ref, ref } from 'vue'
import router from '../router/router'
import { Md5 } from 'ts-md5'
import { PASSWORD_RAW_MD5 } from '../constants/strings'

const pswd: Ref<string> = ref('')
const pswd_md5: Ref<string> = ref('')

const auth = (pswd: string) => {
    pswd_md5.value = Md5.hashStr(pswd);
    if (pswd_md5.value.toUpperCase() === PASSWORD_RAW_MD5) {
        window.localStorage.setItem('access_token', pswd.toUpperCase());
        ElMessage.success('Welcome!');
        router.push('/');
    }
    else {
        ElMessage.error('Invalid Password!');
    }
}
</script>