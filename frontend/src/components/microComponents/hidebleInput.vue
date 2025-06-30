<script setup>
    import { defineProps, defineEmits, ref } from "vue";

    const props = defineProps({  
        modelValue: {
          type: String,
          required: true,
        },
        type: {
            type: String,
            required: true,
        },
        allowHiding: {
            type: Boolean,
            required: true,
        },
        placeHolder: {
            type: String,
            default: '',
        },
        value: {
            type: String,
            required: true,
        },
        labelText: {
            type: String,
            required: true,
        },
    });
    const emit = defineEmits(['update:modelValue'])

    function onInput(event) {
      emit('update:modelValue', event.target.value)
    }

    const showValue = ref(false)
    const handleVisibilityVale = () => {
      showValue.value = !showValue.value
    }
</script>

<template>
  <div class="form-floating position-relative" v-if="allowHiding">
    <input
      @input="onInput"
      :type="showValue ? 'text' : type"
      class="form-control"
      :id="`floating${type}`"
      :placeholder="placeHolder"
    />
    <label :for="`floating${type}`">{{ labelText }}</label>
    <font-awesome-icon 
      class="position-absolute top-50 end-0 translate-middle-y me-3" 
      :icon="showValue ? ['fas', 'eye-slash'] : ['fas', 'eye']" 
      @click="handleVisibilityVale"
    />
  </div>

  <div class="form-floating" v-else>
    <input
      @input="onInput"
      :type="type"
      class="form-control"
      :id="`floating${type}`"
      :placeholder="placeHolder"
    />
    <label :for="`floating${type}`">{{ labelText }}</label>
  </div>
</template>
