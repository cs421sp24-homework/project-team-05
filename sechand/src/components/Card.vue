<template>
  <div class="card" @click="onClick()">
    <img :src="card.imageUrl" class="card-img-top" :alt="card.title" />
    <div class="card-body">
      <h5 class="card-title">{{ card.title }}</h5>
      <p class="card-text">{{ card.text }}</p>
    </div>
    <div class="card-seller">{{ card.seller }}</div>
  </div>
</template>
<script>
export default {
  name: "Card",
  props: {
    card: Object,
  },
  methods: {
    onClick() {
      this.$emit("card-detail");
    },
  },
};
</script>
<style scoped>
.card {
  margin: 10px;
  width: 18rem;
  cursor: pointer;
}
.card-seller {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.5);
  color: rgb(0, 0, 0);
  padding: 5px;
}
</style>