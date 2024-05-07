<template>
  <div v-if="this.currentUser">
    <UserNavbar :currentUser="currentUser" @userLogout="userStateChange" />
    <div class="contain">
      <div class="left">
        <div class="row">
          <Button v-if="unreviewedItems != 0" :text="'You have ' + unreviewedItems.length + ' item waiting for review'"
            color="lightyellow" @click="reviewItem">
          </Button>
          <div class="row">
            <div class="col-6">
              <h2>My Items</h2>
            </div>
            <div class="col-6 text-end">
              <Button class="new-post-btn" text="New Post" color="green" @click="newPost" id="toPost"></Button>
              <Button class="showall" text="All Posts" color="transparent" @click="myitems"></Button>
            </div>
          </div>

          <div class="card-container">
            <Cards :cards="postCardsData" :number="3" />
          </div>
        </div>

        <!-- Segment -->
        <div class="row">
          <div class="col-12">
            <hr class="segment" />
          </div>
        </div>
        <div class="row">
          <div class="row">
            <div class="col-6">
              <h2>Order History</h2>
            </div>
            <div class="col-6 text-end">
              <Button class="showall" text="All Order" color="transparent" @click="historys"></Button>
            </div>
          </div>

          <div class="card-container">
            <Cards :cards="historyCardsData" :number="3" />
          </div>
        </div>
        <!-- Segment -->
        <div class="row">
          <div class="col-12">
            <hr class="segment" />
          </div>
        </div>
        <div class="row">
          <div class="row">
            <div class="col-6">
              <h2>Wishlist</h2>
            </div>
            <div class="col-6 text-end">
              <Button class="showall" text="All Wishlist" color="transparent" @click="wishlist"></Button>
            </div>
          </div>

          <div class="card-container">
            <Cards :cards="collectionCardsData" :number="3" />
          </div>
        </div>
      </div>
      <div class="line"></div>
      <div class="right">
        <div class="rightupper">
          <!-- User profile information -->
          <img :src="this.currentUser.image" alt="User Icon" class="me-3 profile-image"
            style="width: 150px; height: 150px; border-radius: 50%" />
          <p class="mb-1 font-large-vh font-large-vw profile-name">
            {{ this.currentUser.displayname }}
          </p>
          <!-- Increase font size -->
          <p class="mb-0 font-large-vh font-large-vw profile-address">
            {{ this.currentUser.address.name }}
          </p>
          <!-- Increase font size -->
          <Button class="edit-profile-btn" text="My Profile" color="transparent" @click="editProfile" id="profile">
          </Button>
          <Star :value="reviews.overall_rating" :selectable="false" />
          <p style="font-size: 20px; padding: 10px"> Reviews </p>
        </div>
        <div v-for="review in reviews.reviews" :key="review.id" class="review-container">
          <div class="avatar-info">
            <img :src="review.buyer_avatar" class="review-image" />
            <p class="buyer-name">{{ review.buyer_displayname }}</p>
            <i>{{ review.item_name }}</i>
          </div>
          <div>
            <Star :value="review.rating" :selectable="false" />
          </div>
          <div>
            <p class="review-text">{{ review.review }}</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Cards from "@/components/Cards.vue";
import Button from "@/components/Button.vue";
import axios from "axios";
import Star from "@/components/Star.vue";
export default {
  name: "Me",
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
      unreviewedItems: {},
      reviews: {},
      postCardsData: [],
      historyCardsData: [],
      collectionCardsData: [],
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
      console.log("unreviewedItems", response.data);
    } catch (error) {
      console.error(error);
    }
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(
        HTTP_PREFIX + `api/v1/post/Order/Transaction/Review/${this.currentUser.id}`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      this.reviews = response.data;
      console.log("reviews", this.reviews.overall_rating);
    } catch (error) {
      console.error(error);
    }
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(
        HTTP_PREFIX + "api/v1/post/UserItems/all",
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      console.log("postCardsData", response.data);
      this.postCardsData = response.data;
    } catch (error) {
      console.error(error);
    }
    // history card data
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(
        HTTP_PREFIX + "api/v1/post/Order/Transactions/all",
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      console.log("historyCardsData", response.data);
      this.historyCardsData = response.data;
      console.log("historyCardsData", response.data);
    } catch (error) {
      console.error(error);
    }
    try {
      const accessToken = localStorage.getItem("access_token");
      const response = await axios.get(HTTP_PREFIX + "api/v1/post/Items/Collection", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      this.collectionCardsData = response.data;
      console.log("collectionCardsData", response.data);
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    reviewItem() {
      this.$router.push({ name: "Review" });
    },
    myitems() {
      this.$router.push({ name: 'ShowAll', params: { data: "myItems" } });
    },
    historys() {
      this.$router.push({ name: 'ShowAll', params: { data: "history" } });
    },
    wishlist() {
      this.$router.push({ name: 'ShowAll', params: { data: "Wishlist" } });
    },
    userStateChange() {
      this.$emit("userStateChange", {});
    },
    editProfile() {
      this.$router.push("/profile");
      console.log("Edit profile");
    },
    newPost() {
      this.$router.push("/postitem");
    },
  },
};
</script>

<style scoped>
.contain {
  margin-top: 12vh;
  margin-left: 5vw;
}

.left {
  width: 74vw;
  height: 100vh;
  float: left;
}

.right {
  width: 19vw;
  height: 100vh;
  float: right;
  /* justify-content: center; */

}

.rightupper {
  flex-direction: column;
  display: flex;
  align-items: center;
}

.profile-image {

  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 2vh;
}

.profile-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.profile-address {
  font-size: 16px;
  color: #666;
}

.edit-profile-btn {
  background: none;
  border: none;
  color: #007bff;
  font-size: 16px;
  cursor: pointer;
  text-decoration: underline;
  outline: none;
}

.edit-profile-btn:hover {
  color: #0056b3;
}

.new-post-btn {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.new-post-btn:hover {
  background-color: #218838;
  cursor: pointer;
}

.segment {
  border-top: 1px solid #ddd;
}

.card-container {
  overflow-x: auto;
  white-space: wrap;
  height: 50vh;
}

.card {
  display: inline-block;
  margin-right: 10px;
}

.line {
  width: 1px;
  height: 100%;
  background-color: #bdbdbd;
  position: fixed;
  top: 0;
  bottom: 0;
  margin-left: 75vw;
}

.showall {
  text-decoration: underline grey;
}

.review-container {
  /* margin-left: 1vw; */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
}

.review-image {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}


.buyer-name {
  font-weight: bold;
  margin-bottom: 5px;
  margin-right: 5px;
}

.avatar-info {
  display: flex;
  align-items: center;

}

.review-text {
  margin-top: 5px;
}
</style>
