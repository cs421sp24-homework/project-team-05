<template>
  <div>
    <UserNavbar :icon_src="icon_src" :Username="Username" />
    <div class="row">
      <div class="col-12">
        <h1>New Post</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <form @submit.prevent="submitForm">
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

          <!-- Description -->
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea class="form-control" id="description" v-model="description" rows="3" required></textarea>
          </div>

          <!-- Price -->
          <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input type="number" class="form-control" id="price" v-model="price" required />
          </div>

          <!-- Address -->
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <input type="text" class="form-control" id="address" :value="address" readonly />
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
          <label class="form-label">Image Preview</label>
          <img v-if="picture" :src="picturePreview" class="img-fluid" alt="Image Preview" />
          <div v-else class="text-muted">No image selected</div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
export default {
  name: "NewPost",
  components: {
    UserNavbar,
  },
  data() {
    return {
      icon_src: "/icon.jpg",
      Username: "User",
      itemName: "",
      description: "",
      price: "",
      address: "123 Main Street, City, Country", // Sample address
      picture: null,
    };
  },
  methods: {
    openUserProfile() {
      console.log("Open user profile");
    },
    handleFileUpload(event) {
      this.picture = event.target.files[0];
    },
    cancel() {
      console.log("Cancelled");
    },
    // submitForm() {
    //   console.log("Form submitted");
    // },
    async submitForm() {
      console.log("summitted");
      try {
        const formData = new FormData();
        formData.append('name', this.itemName);
        formData.append('description', this.description);
        formData.append('tag', ["ABC"]);
        formData.append('price', this.price);
        formData.append('user_id', 16);
        // formData.append('user_id', this.user.id);
        if (this.picture) {
          formData.append('picture', this.picture);
        }
        console.log(formData);
        const response = await axios.post('http://127.0.0.1:8000/api/v1/post/Item/new', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log("Form submitted successfully:", response.data);
        // Optionally, you can navigate to another page after successful form submission
        // this.$router.push('/success');
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },
  },
};
</script>
  