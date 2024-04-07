<template>
  <div class="cards-container">
    <div :key="card.id" v-for="(card, index) in getCards(number)" class="card-wrapper">
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
    number: Number,
  },
  components: {
    Card,
  },
  methods: {
    getCards(number) {
      if (number === undefined)
        return this.cards;
      if (number <= this.cards.length)
        return this.cards.slice(0, number);
      else
        return this.cards;
    },
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