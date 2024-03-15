<template>
  <form class="d-flex" role="search" @submit.prevent="handleSubmit">
    <input class="form-control me-2" type="search" placeholder="Search for anything" aria-label="Search"
      v-model="searchinput" id="searchid" />
    <select class="form-select" id="Category" v-model="category">
      <option value="all" selected>All Category</option>
      <!-- <option value="all">All Category</option> -->
      <option v-for="(value, index) in this.categories" :key="index" :value="value">
        {{ value }}
      </option>
    </select>
    <Button @btn-click="onClick()" text="Search" id="searchbtn"></Button>
  </form>
</template>
<script>
import Button from "@/components/Button.vue";
export default {
  name: "Seach",
  props: {
    categories: Array,
  },
  components: {
    Button,
  },
  data() {
    return {
      category: "all",
      searchinput: "",
    };
  },
  methods: {
    onClick() {
      this.$emit("onClick", { input: this.searchinput, cate: this.category });
    },
  },
};
</script>
<style scoped>
#Category {
  width: 30%;
  margin-left: 0px;
}

#searchbtn {
  border: 1px solid #00cc66;
  margin-left: 10px;
  height: 5vh;
}

#searchbtn:hover {
  background-color: #01361b;
  color: white;
  opacity: 1;
}
</style>