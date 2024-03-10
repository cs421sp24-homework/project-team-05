<!-- ImageUploader.vue -->
<template>
    <div class="image-uploader" :style="'width: '+size+'vh; height: '+size+'vh;'">
      <label class="upload-label">
        <input type="file" @change="handleImageUpload" class="file-input" :disabled="!edittable">
        <div class="upload-placeholder" v-if="!imageUrl && !default_src" :style="'font-size: '+size/2+'vh;'"></div>
        <img :src="default_src? default_src : imageUrl" v-else 
             :style="{ borderRadius: circular ? '50%' : '0%', 
                       border: edittable ? '5px dashed #00cc66' : '5px dashed #A0A0A0'}" 
                       class="uploaded-image">
      </label>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      circular: {
        type: Boolean,
        default: true
      },
      size: {
        type: Int32Array,
        default: 20
      },
      default_src: {
        type: String,
        default: ''
      },
      edittable: {
        type: Boolean,
        default: true
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
        // console.log("file", file);
        this.imageUrl = URL.createObjectURL(file);
        console.log(this.imageUrl);
        // console.log("image url", this.imageUrl);
        this.$emit("upload", file);
      }
    }
  };
  </script>
  
  <style scoped>
  .image-uploader {
    position: relative;
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
    color: #666;
  }
  
  .uploaded-image {
    width: 100%;
    height: 100%;
    border-radius: 10px;
    object-fit: cover;
    /* border: 2px dashed #007bff; */
  }
  </style>
  