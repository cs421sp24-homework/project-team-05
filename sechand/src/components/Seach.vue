<template>
  <form class="d-flex" role="search">
    <input
      class="form-control me-2"
      type="search"
      placeholder="Search for anything"
      aria-label="Search"
      v-model="searchinput"
    />
    <select class="form-select" id="Category" v-model="category">
      <option value="" disabled selected hidden>Category</option>
      <option
        v-for="(value, index) in this.categories"
        :key="index"
        :value="value"
      >
        {{ value }}
      </option>
    </select>
    <button class="btn btn-outline-success" type="submit" @click="search">
      Search
    </button>
  </form>
</template>
<script>
export default {
  name: "Seach",
  props: {
    categories: Array,
  },
  data() {
    return {
      category: "",
      searchinput: "",
    };
  },
  methods: {
    search() {
      // use api to get location based cards, rerender
      // const HTTP_PREFIX = import.meta.env.VITE_HOST;
      // try {
      //   const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/all");
      //   this.cardsData = response.data;
      // } catch (error) {
      //   console.error(error);
      // }
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