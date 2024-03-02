<template>
  <button @click="onClick()" :style="{ background: color }" class="btn">
    {{ text }}
  </button>
</template>
  
<script>
export default {
  name: "Button",
  props: {
    text: String,
    color: String,
  },
  methods: {
    onClick() {
      this.$emit("btn-click");
    },
  },
};
</script>
<style scoped>
.btn:hover {
  opacity: 0.5;
  cursor: pointer;
}

.btn {
  margin: 4px 2px;
}
</style>