<template>
    <div class="star-rating" v-if="selectable">
        <span v-for="starIndex in 5" :key="starIndex" @click="setRating(starIndex)"
            :class="{ 'filled': starIndex <= displayRating }">&#9733;</span>
    </div>
    <div class="star-rating" v-else>
        <span v-for="starIndex in 5" :key="starIndex" :class="{ 'filled': starIndex <= rating }">&#9733;</span>
    </div>
</template>

<script>
export default {
    name: 'Star',
    props: {
        rating: {
            type: Number,
            required: true
        },
        selectable: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            displayRating: this.rating
        };
    },
    methods: {
        setRating(rating) {
            this.displayRating = rating;
            this.$emit('update:rating', rating);
        }
    }
}
</script>

<style>
.star-rating {
    font-size: 24px;
}

.star-rating span {
    color: rgb(149, 148, 146);
    cursor: pointer;
}

.star-rating .filled {
    color: orange;
}
</style>