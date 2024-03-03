<template>
  <div>{{ this.hello }}</div>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    fetchHello() {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
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