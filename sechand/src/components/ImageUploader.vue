<!-- ImageUploader.vue -->
<template>
    <div class="image-uploader">
      <label class="upload-label">
        <input type="file" @change="handleImageUpload" class="file-input">
        <div class="upload-placeholder" v-if="!imageUrl"></div>
        <img :src="imageUrl" v-else :style="{ borderRadius: circular ? '50%' : '0%' }" class="uploaded-image">
      </label>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      circular: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        imageUrl: ''
      };
    },
    methods: {
      handleImageUpload(event) {
        const file = event.target.files[0];
        this.imageUrl = URL.createObjectURL(file);
        this.$emit("upload", file);
      }
    }
  };
  </script>
  
  <style scoped>
  .image-uploader {
    position: relative;
    width: 20vh;
    height: 20vh;
  }
  
  .file-input {
    display: none;
  }
  
  .upload-label {
    height: 100%;
    display: block;
    position: relative;
    cursor: pointer;
  }
  
  .upload-placeholder {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px dashed #ccc;
    transition: border-color 0.3s ease;

  }
  
  .upload-placeholder:before {
    content: "+";
    font-size: 6vh;
    color: #666;
  }
  
  .uploaded-image {
    width: 100%;
    height: 100%;
    max-height: 20vh;
    border-radius: 10px;
    object-fit: cover;
    border: 2px dashed #007bff;
  }
  </style>
  