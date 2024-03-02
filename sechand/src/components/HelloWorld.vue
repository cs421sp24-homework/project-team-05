<template>
  <div>{{ this.hello }}</div>
</template>

<script>
import axios from "axios";
import HTTP_PREFIX from "../router/apiEntry.js";
export default {
  methods: {
    fetchHello() {
      axios
        .get(HTTP_PREFIX + "hello_world/")
        .then((response) => {
          console.log(response.data);
          this.hello = response.data.msg;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
  },
  data() {
    return {
      hello: "initial",
    };
  },
  mounted() {
    this.fetchHello();
  },
};
</script>