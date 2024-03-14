<template>
  <div class="dropdown">
    <button
      class="btn btn-secondary dropdown-toggle"
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      {{ text }}
    </button>
    <ul class="dropdown-menu dropdown-menu-dark">
      <li v-for="(value, index) in dropdownData" :key="index">
        <a class="dropdown-item">
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              value=""
              :id="'checkbox' + index"
              @change="toggleSelection(value)"
            />
            <label class="form-check-label" :for="'checkbox' + index">
              {{ value }}
            </label>
          </div>
        </a>
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
    dropdownData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      selected: [],
    };
  },
  methods: {
    toggleSelection(value) {
      if (this.selected.includes(value)) {
        this.selected = this.selected.filter((item) => item !== value);
      } else {
        this.selected.push(value);
      }
      this.$emit("update:selected", this.selected);
    },
  },
};
</script>