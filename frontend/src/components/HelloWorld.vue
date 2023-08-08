<template>
  <div>
    <img alt="Vue logo" src="@/assets/logo.png" />
    <h1>{{ msg }}</h1>
    <p> {{ token }} </p>
  </div>
</template>

<script>
import Server from "@/Server";
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "API Not Working",
      token: localStorage.getItem('token'),
    };
  },
  methods: {
    getResponse() {
      Server().get("")
        .then((res) => {
          this.msg = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>