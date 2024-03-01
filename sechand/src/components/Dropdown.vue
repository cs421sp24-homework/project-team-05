<template>
  <div class="dropdown">
    <button
      class="btn btn-secondary dropdown-toggle"
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
      @click="onClick()"
    >
      {{ text }}
    </button>
    <ul class="dropdown-menu dropdown-menu-dark">
      <li v-for="item in dropdownData" :key="item.id">
        <a
          class="dropdown-item"
          :href="item.link"
          @click="handleItemClick(item)"
          >{{ item.label }}</a
        >
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  name: "Dropdown",
  props: {
    text: {
      type: String,
      required: true,
    },
    emitMethod: {
      type: String,
      required: true,
    },
    dropdownData: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    handleItemClick(item) {
      this.$emit(this.emitMethod, item);
    },
    onClick() {
      this.$emit("dropdown-click");
    },
  },
};
</script>