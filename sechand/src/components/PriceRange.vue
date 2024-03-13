<template>
  <div class="price-range-container">
    <div class="input-with-dollar">
      <span>$</span>
      <input type="number" id="min" placeholder="MIN" />
    </div>
    <span class="dash">-</span>
    <div class="input-with-dollar">
      <span>$</span>
      <input type="number" id="max" placeholder="MAX" />
    </div>
  </div>
</template>
<script>
export default {
  name: "PriceRange",
};
</script>
<style>
.price-range-container {
  display: flex;
  align-items: center;
  background: #343a40;
  padding: 10px;
  border-radius: 8px;
}
.input-with-dollar {
  position: relative;
  margin-right: 10px;
}

.input-with-dollar span {
  position: absolute;
  left: 8px;
  top: 45%;
  transform: translateY(-50%);
  color: #333435;
}

.input-with-dollar input {
  width: 100px;
  padding-left: 20px; /* Adjust as needed */
  border-radius: 4px;
}
.dash {
  color: rgb(247, 247, 247); /* Change the color of the dash */
  margin-right: 5px; /* Add some margin for spacing */
}
</style>