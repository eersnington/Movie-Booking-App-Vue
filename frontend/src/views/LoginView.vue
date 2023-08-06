<template>
    <div class="d-flex justify-content-center align-items-center">
        <h2>Login</h2>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="email">Username</label>
                <input type="text" class="form-control" v-model="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" v-model="password" required>
            </div>
            <div class="error">
                <p v-if="status === 'failed'" class="error-message">{{ fail_message }}</p>
            </div>
        <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>

<script>
import Server from '@/Server';

export default {
    name: "LoginView",
    data() {
        return {
        email: '',
        password: '',
        status: null,
        fail_message: null,
        };
    },
    methods: {
        login() {
            const data = { email: this.email, password: this.password };
            Server().post('/login', data)
            .then(res => {
                localStorage.setItem('token', res.data.access_token);
                this.$router.push('/').catch(()=>{});
                window.location.reload();
            })
            .catch(error => {
                this.status = "failed";
                console.error('Login failed:', error.response.data.error);
                this.fail_message = error.response.data.error;
                
            });
        }
    },
};
</script>

<style scoped>
.error-message {
    color: red;
}
</style>