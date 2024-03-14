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
    <Button @btn-click="onClick()" text="Search" id="search"></Button>
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

#search {
  border: 1px solid #00cc66;
  margin-left: 10px;
  height: 5vh;
}

#search:hover {
  background-color: #09562f;
  color: white;
}
</style>