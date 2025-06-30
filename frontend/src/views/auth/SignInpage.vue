<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '../../stores/auth';
    import hidebleInput from '../../components/microComponents/hidebleInput.vue';

    const auth = useAuthStore()

    const email = ref('')
    const password = ref('')

</script>

<template>
    <form class="container" @submit.prevent="auth.signUp(email, password)">
        <hideble-input 
            class="mt-3"
            :type="'text'"
            :allow-hiding="false"
            :place-holder="'Email'"
            :label-text="'Email'"
            v-model="email"
        />

        <hideble-input 
            class="mt-3"
            :type="'password'"
            :allow-hiding="true"
            :place-holder="'Password'"
            :label-text="'Password'"
            v-model="password"
        />

        <button type="submit" class="btn btn-primary mt-3">Registrati</button>
    </form>
</template>