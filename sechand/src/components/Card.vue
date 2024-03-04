<template>
  <div class="card" @click="cardDetail(card)">
    <img :src="card.imageUrl" class="card-img-top" :alt="card.name" />
    <div class="card-body">
      <h5 class="card-name">{{ card.name }}</h5>
      <p class="card-description">{{ card.description }}</p>
      <p class="card-price">Price: ${{ card.price }}</p>
    </div>
    <div class="card-seller">{{ card.displayname }}</div>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    card: Object,
  },
  methods: {
    cardDetail(card) {
      this.$router.push({ name: 'ShowItem', params: { id: card.id } });

      console.log("Detail");
    },
  },
};
</script>

<style scoped>
.card {
  margin: 10px;
  width: 250px;
  /* Adjust the width as needed */
  height: 350px;
  /* Adjust the height as needed */
  cursor: pointer;
  position: relative;
  /* Add relative positioning to the card */
}

.card-img-top {
  width: 100%;
  height: 200px;
  /* Adjust the image height as needed */
  object-fit: cover;
  /* Ensure the image covers the entire space */
}

.card-body {
  padding: 1rem;
}

.card-name {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-description {
  margin-bottom: 0.5rem;
}

.card-price {
  margin-bottom: 0.5rem;
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
