<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <img src="./assets/logo.png" width="50" height="50">
        <a class="navbar-brand" href="">&nbsp;MovieCops</a>
        <div class="collapse navbar-collapse" id="navbarElements">
          <ul class="navbar-nav me-auto">
            <li class="nav-item active">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">Shows</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="profileDropdown" role="button" data-bs-toggle="dropdown"
              aria-expanded="false">
                User
              </a>
              <ul class="dropdown-menu" aria-labelledby="profileDropdown">
                <li><a class="dropdown-item" href="">Bookings</a></li>
                <router-link to="/login" class="dropdown-item" v-if="!token">Login</router-link>
                <button @click="logout" class="dropdown-item"  v-else>Logout</button>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="locationDropdown" role="button" data-bs-toggle="dropdown">
              Location
              </a>
              <ul class="dropdown-menu" aria-labelledby="locationDropdown">
              <li><a class="dropdown-item" href="">Chennai</a></li>
              <li><a class="dropdown-item" href="">Kochi</a></li>
              <li><a class="dropdown-item" href="">Bangalore</a></li>
              </ul>
            </li>
          </ul>
          <br>
          <form class="d-flex" action="" method="POST">
            <input class="form-control mr-sm-2" type="search" placeholder="Search Shows" name="search">
            <button class="btn btn-outline-success" type="submit" name="submit" value="search">Search</button>
          </form>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
</style>

<script>
import Server from '@/Server';
export default {
  computed: {
    token() {
      return localStorage.getItem('token') !== null;
    },
  },
  methods: {
    logout() {
      Server().get('/logout')
      .then(res => {
        console.log(res);
        localStorage.removeItem('token');
        this.$router.push('/').catch(()=>{});
        window.location.reload();
          
      })
      .catch(error => {
          console.error('Logout failed:', error.response.data.error);          
      });
    },
  },
};
</script>
