<template>
  <div>
    <h1>Dashboard</h1>
    <template>
      <router-link :to="{ name: 'form-create' }">Create form</router-link>
      <FormCard v-for="form in forms" :key="form.id" :form="form" />
    </template>
  </div>
</template>

<script>
import FormCard from '@/components/FormCard.vue'
import axios from 'axios'

export default {
  data() {
    return {
      forms: []
    }
  },
  components: {
    FormCard
  },
  created() {
    return axios.get('//localhost:8000/forms/').then(response => {
      this.forms = response.data
    })
  }
}
</script>

<style scoped></style>
