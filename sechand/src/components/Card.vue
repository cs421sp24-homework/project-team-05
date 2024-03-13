<template>
  <div class="card" @click="cardDetail(card)">
    <img :src="card.image" class="card-img-top" :alt="card.name" />
    <div class="card-body">
      <h5 class="card-name ellipsis">{{ card.name }}</h5>
      <p class="card-description ellipsis">{{ card.description }}</p>
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
      this.$router.push({ name: "ShowItem", params: { id: card.id } });
      console.log("Detail");
    },
  },
};
</script>

<style scoped>
.card {
  background: rgb(146, 146, 157);
  border: 3px solid #33332b35;
  margin: 10px;
  width: 250px;
  /* Adjust the width as needed */
  height: 350px;
  /* Adjust the height as needed */
  cursor: pointer;
  position: relative;
  /* Add relative positioning to the card */
  border-radius: 30px;
}

.card-img-top {
  padding: 1rem;
  width: 100%;
  height: 200px;
  /* Adjust the image height as needed */
  object-fit: cover;
  border-radius: 30px;
  /* Ensure the image covers the entire space */
}

.card-body {
  background: grey;
  padding: 1rem;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
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
  border-radius: 10px;
}
.ellipsis {
  display: block;
  /* max-height: 10em; Adjust to the desired number of lines */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 200px; /* Define a width to trigger text overflow */
}
</style>
