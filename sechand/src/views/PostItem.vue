<template>
  <div>
    <UserNavbar />
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1>New Post</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <form class="postForm" @submit.prevent="submitForm">
            <!-- Item Name -->
            <div class="mb-3">
              <label for="itemName" class="form-label">Item Name</label>
              <input type="text" class="form-control" id="itemName" v-model="itemName" required />
            </div>

            <!-- Upload Picture -->
            <div class="mb-3 d-flex align-items-center">
              <label for="uploadPicture" class="form-label me-2">Upload Picture</label>
              <input type="file" id="uploadPicture" accept="image/*" style="display: none" ref="fileInput"
                @change="handleFileUpload" />
              <button type="button" class="btn btn-primary" @click="$refs.fileInput.click()">
                Choose File
              </button>
            </div>
            <!-- Choose Category -->
            <div class="mb-3">
              <label for="Category" class="form-label">Category</label>
              <select class="form-select" id="Category" v-model="category" required>
                <option v-for="(value, index) in this.categories" :key="index" :value="value">
                  {{ value }}
                </option>
              </select>
            </div>
            <!-- Description -->
            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea class="form-control" id="description" v-model="description" rows="3" required></textarea>
            </div>

            <!-- Price -->
            <div class="mb-3">
              <label for="price" class="form-label">Price</label>
              <input type="number" step="0.01" class="form-control" id="price" v-model="price" required />
            </div>

            <!-- Address -->
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <input type="text" class="form-control" id="address" :value="this.currentUser.address.name" readonly />
            </div>

            <!-- Buttons -->
            <div class="d-flex justify-content-end">
              <button type="button" class="btn btn-secondary me-2" @click="cancel">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">Post</button>
            </div>
          </form>
        </div>
        <div class="col-md-6">
          <!-- Image Preview -->
          <div class="mb-3">
            <label class="form-label">Card Preview</label><br />
            <Card :card="{
            name: this.itemName,
            description: this.description,
            price: this.price,
            image: this.imageUrl,
            displayname: this.currentUser.displayname,
          }"></Card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "@/components/UserNavbar.vue";
import Card from "@/components/Card.vue";
import axios from "axios";
export default {
  name: "NewPost",
  props: {
    categories: Array,
  },
  components: {
    UserNavbar,
    Card,
  },
  data() {
    return {
      itemName: "",
      category: "",
      description: "",
      price: "",
      picture: null,
      imageUrl: "",
      currentUser: JSON.parse(localStorage.getItem("user")),
      card: {
        name: this.itemName,
        description: this.description,
        price: this.price,
        image: this.imageUrl,
        // displayname: this.currentUser.displayname,
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      this.picture = event.target.files[0];
      this.imageUrl = URL.createObjectURL(this.picture);
      console.log("image uploaded:", this.imageUrl);
    },
    cancel() {
      this.$router.go(-1);
      console.log("Cancelled");
    },
    async submitForm() {
      const HTTP_PREFIX = import.meta.env.VITE_HOST;
      console.log("submmitted");
      try {
        const formData = new FormData();
        formData.append("name", this.itemName);
        formData.append("description", this.description);
        formData.append("category", this.category);
        formData.append("price", this.price);
        formData.append("seller", this.currentUser.id);
        formData.append("image", this.picture);
        console.log(formData);
        const response = await axios.post(
          HTTP_PREFIX + "api/v1/post/Item/new",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("Form submitted successfully:", response.data);
        this.$router.push("/me");
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },
  },
};
</script>
<style>
.postForm {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.postForm label {
  font-weight: bold;
}

.postForm input[type="text"],
.postForm input[type="number"],
.postForm textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.postForm input[type="file"] {
  display: none;
}

.postForm .btn-file {
  cursor: pointer;
}

.postForm .btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: #fff;
}

.postForm .btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
  color: #fff;
}

.postForm .btn {
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.postForm .btn:not(:last-child) {
  margin-right: 10px;
}

.postForm .img-fluid {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin-top: 10px;
}

.postForm .text-muted {
  color: #6c757d;
}
</style>