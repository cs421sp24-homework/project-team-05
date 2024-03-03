<template>
    <div>
        <UserNavbar />
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <h1>Edit Item</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <form @submit.prevent="submitForm">
                        <!-- Item Name -->
                        <div class="mb-3">
                            <label for="itemName" class="form-label">Item Name</label>
                            <input type="text" class="form-control" id="itemName" v-model="item.name" required />
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
                            <textarea class="form-control" id="description" v-model="item.description" rows="3"
                                required></textarea>
                        </div>

                        <!-- Price -->
                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <input type="number" step="0.01" class="form-control" id="price" v-model="item.price"
                                required />
                        </div>

                        <!-- Address -->
                        <div class="mb-3">
                            <label for="address" class="form-label">Address</label>
                            <input type="text" class="form-control" id="address" :value="this.currentUser.address.name"
                                readonly />
                        </div>

                        <!-- Buttons -->
                        <div class="d-flex justify-content-end">
                            <button type="button" class="btn btn-secondary me-2" @click="cancel">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">Update</button>
                            <button type="submit" class="btn btn-danger me-2" @click="deleteItem">
                                Delete
                            </button>
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
    </div>
</template>
    
<script>
import UserNavbar from "@/components/UserNavbar.vue";
import axios from "axios";
import HTTP_PREFIX from "../router/apiEntry.js";
export default {
    name: "EditItem",
    components: {
        UserNavbar,
    },
    data() {
        return {
            item: {},
            currentUser: JSON.parse(localStorage.getItem('user'))
        };
    },
    async created() {
        // Check if the current user is the seller of the item
        this.id = this.$route.params.id;

        try {
            const response = await axios.get(HTTP_PREFIX + `api/v1/post/Item/${this.id}`);
            console.log(response.data);
            this.item = response.data;
        } catch (error) {
            console.error(error);
        }
    },
    methods: {
        handleFileUpload(event) {
            this.picture = event.target.files[0];
        },
        cancel() {
            this.$router.go(-1);
            console.log("Cancelled");
        },
        deleteItem() {
            try {
                const response = axios.delete(HTTP_PREFIX + `api/v1/post/Item/${this.id}`, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    data: {
                        id: this.currentUser.id
                    }

                });
                console.log("Form submitted successfully:", response.data);
                this.$router.push("/me");

            } catch (error) {
                console.error("Error submitting form:", error);
            }
        },
        async submitForm() {
            console.log("summitted");
            try {
                const formData = new FormData();
                formData.append('name', this.item.name);
                formData.append('description', this.item.description);
                formData.append('tag', ["ABC"]);
                formData.append('price', this.item.price);
                // formData.append('user_id', this.user.id);
                if (this.picture) {
                    formData.append('picture', this.picture);
                }
                console.log(formData);
                const response = await axios.patch(HTTP_PREFIX + `api/v1/post/Item/${this.id}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log("Form submitted successfully:", response.data);
                this.$router.go(-1);
                // Optionally, you can navigate to another page after successful form submission
                // this.$router.go(-1);
            } catch (error) {
                console.error("Error submitting form:", response.data);
                console.error("Error submitting form:", error);
            }
        },
    },
};
</script>
<style>
.btn {
    margin-left: 4px;
}

.btn:hover {
    opacity: 0.8;
    cursor: pointer;
}
</style>
    