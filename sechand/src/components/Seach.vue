<template>
  <form class="d-flex" role="search" @submit.prevent="handleSubmit">
    <input class="form-control me-2" type="search" placeholder="Search for anything" aria-label="Search"
      v-model="searchinput" />
    <select class="form-select" id="Category" v-model="category">
      <option value="" disabled selected hidden>Category</option>
      <option value="">All Category</option>
      <option v-for="(value, index) in this.categories" :key="index" :value="value">
        {{ value }}
      </option>
    </select>
    <Button @btn-click="onClick()" text="Search"></Button>
  </form>
</template>
<script>
import axios from "axios";
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
      category: "",
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
<style>
#Category {
  width: 30%;
  margin-left: 0px;
}
</style>