<template>
  <div>
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import Server from "@/Server";
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "API Not Working",
    };
  },
  methods: {
    getResponse() {
      Server().get("")
      .then((res)=>{
          this.msg = res.data;
      })
      .catch((err)=>{
          console.log(err);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>

<style lang="scss" scoped></style>
