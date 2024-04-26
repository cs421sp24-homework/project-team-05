<template>
  <div>
    <UserNavbar :currentUser="currentUser" @userLogout="userStateChange" />
    <div class="contain">
      <div v-for="item in unreviewedItems" :key="item.id" class="item-container">
        <div class="item-info">
          <h4>{{ item.itemdetail.name }}</h4>
          <img :src="item.itemdetail.image" class="item-image">
        </div>
        <div class="item-review">
          <Star :rating.sync="item.rating" :selectable="isSelectable" />
          <form @submit.prevent="submitReview(item)" class="review-form">
            <textarea v-model="item.review" placeholder="Write your review"></textarea>
            <Button type="submit" text="Submit Review" color="lightBlue"></Button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import Button from "@/components/Button.vue";
import Star from "@/components/Star.vue";
import axios from "axios";
export default {
  name: "Review",
  props: {
    currentUser: Object,
  },
  components: {
    UserNavbar,
    Cards,
    Button,
    Star
  },
  data() {
    return {
      rating: 5,
      isSelectable: true,
      unreviewedItems: {},
    };
  },
  async created() {
    const HTTP_PREFIX = import.meta.env.VITE_HOST;
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(
        HTTP_PREFIX + "api/v1/post/Order/Transaction/Review/UnReviewedOrder",
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      this.unreviewedItems = response.data;
      if (this.unreviewedItems.length === 0) {
        this.$router.push("/me");
      }
      console.log("unreviewedItems", response.data);
    } catch (error) {
      console.error(error);
    }
    for (let item of this.unreviewedItems) {
      try {
        const response = await axios.get(HTTP_PREFIX + `api/v1/post/Item/${item.item_id}`);
        item.itemdetail = response.data;
      } catch (error) {
        console.error(error);
      }
    }
  },
  methods: {
    userStateChange() {
      this.$emit("userStateChange", {});
    },
    async submitReview(item) {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      const accessToken = localStorage.getItem("access_token");
      try {
        const formData = new FormData();
        formData.append("rating", item.rating);
        formData.append("review", item.review);
        const response = await axios.patch(
          HTTP_PREFIX + `api/v1/post/Order/Transaction/Review/add/${item.id}`, formData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.$router.push({ name: "Me" });
      } catch (error) {
        console.error(error);
      }

    },
  }

}

</script>
<style scoped>
.contain {
  margin-top: 12vh;
  margin-left: 5vw;
}

.item-container {
  display: flex;
  margin-bottom: 20px;
}

.item-info {
  flex: 0 0 200px;
}

.item-review {
  margin-left: 20px;
  flex: 1;
}

.item-image {
  width: 100%;
  height: auto;
}

.review-form {
  width: 100%;
}

.review-text {
  margin-top: 10px;
}

textarea {
  width: 80%;
  height: 200px;
}
</style>