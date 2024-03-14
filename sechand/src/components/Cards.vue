<template>
  <div class="cards-container">
    <div :key="card.id" v-for="(card, index) in cards" class="card-wrapper">
      <Card :card="card" :idx="index" />
    </div>
  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  name: "Cards",
  props: {
    cards: Array,
  },
  components: {
    Card,
  },
};
</script>

<style scoped>
.cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.card-wrapper {
  margin: 10px;
}
</style>