<template>
    <form @submit.prevent="login">
        <div class="container">
            <h1 class="h3">Please sign in</h1>
            <div class="row">
                <div class="col-sm">
                    <div class="form-floating">
                        <input type="email" class="form-control" v-model="email" id="email" required>
                        <label for="email">Email address</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm">
                    <div class="form-floating">
                        <input type="password" class="form-control" v-model="password" id="password" required>
                        <label for="password">Password</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm">
                    <button class="w-100 btn btn-lg btn-primary" type="submit">Sign In</button>
                </div>
                <div class="col-sm">
                    <router-link to="/signup" class="w-100 btn btn-lg btn-outline-primary" role="button">Sign
                        Up</router-link>
                </div>
            </div>
        </div>

        <br>
        <div class="error">
            <p v-if="status === 'failed'" class="error-message">{{ fail_message }}</p>
        </div>
    </form>
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
                    this.$router.push('/').catch(() => { });
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
.container {
    max-width: 500px;
    padding: 15px;
    margin: 0 auto;
}

.row {
    padding: 15px;
}

.error-message {
    color: red;
}
</style>