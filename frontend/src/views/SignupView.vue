<template>
    <form @submit.prevent="signup">
    <div class="container">
        <div class="row">
            <div class="col-sm">
                <h1 class="h3">Sign up to MovieCops <img src="@/assets/logo.png" width="50"
                    height="50" alt=""> </h1>
            </div>
        </div>
        <div class="row ">
            <div class="col-sm">
                <div class="form-floating">
                <input type="email" v-model="email" class="form-control" id="email" required>
                <label for="email">Email address</label>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm">
                <div class="form-floating">
                    <input type="text" v-model="name" class="form-control" id="name" required>
                    <label for="name">Name</label>
                </div>
            </div>
            <div class="col-sm">
                <div class="form-floating">
                <select class="form-select" v-model="language">
                    <option disabled selected style="color:green;">Select your preferred language</option>
                    <option value="English">English</option>
                    <option value="Hindi">Hindi</option>
                    <option value="Tamil">Tamil</option>
                    <option value="Malayalam">Malayalam</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm">
                <div class="form-floating">
                <input type="password" v-model="password" class="form-control" id="password" required>
                <label for="password">Password</label>
                </div>
            </div>
        </div>
        <div class="col w-100 h-auto">
            <div class="alert alert-warning alert-dismissible fade show" role="alert">
                <ul class="list">
                <li class="requirements lang">
                    Your password must have at least 8 chars.
                </li>
                <li class="requirements capital-and-small">
                    Your password must have at least 1 capital and small letter.
                </li>
                <li class="requirements num">
                    Your password must have at least 1 number.
                </li>
                <li class="requirements special-char">
                    Your password must have at least 1 special char (!, @, #, $, %).
                </li>
                </ul>
            </div>
        </div>
        <div class="row">
            <div class="col-sm">
                <button class="w-100 btn btn-lg btn-primary" type="submit">Sign Up</button>
        </div>
        </div>
        <div class="row">
            <div class="error">
                <p v-if="status === 'failed'" class="error-message">{{ fail_message }}</p>
                <p v-if="status === 'success'" class="success-message">{{ success_message }}</p>
            </div>
        </div>
        <div class="row">
            <div v-if="status === 'success'" class="col-sm">
                <router-link to="/login" class="w-100 btn btn-lg btn-outline-primary" role="button">Sign In</router-link>
            </div>
        </div>
    </div> 
  </form>
</template>

<script>
import Server from '@/Server';

export default {
    name: "SignupView",
    data() {
        return {
            email: '',
            password: '',
            name: '',
            language: '',
            status: null,
            fail_message: null,
            success_message: null
        };
    },
    methods: {
        signup() {
            const data = { email: this.email, password: this.password, name: this.name, language: this.language };
            Server().post('/signup', data)
                .then(() => {
                this.status = "success";
                this.success_message = "Sign up successful. Please Sign in to Continue.";
            })
                .catch(error => {
                this.status = "failed";
                console.error('Signup failed:', error.response.data.error);
                this.fail_message = error.response.data.error;
            });
        }
    }
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

.success-message {
    color: green;
}
</style>