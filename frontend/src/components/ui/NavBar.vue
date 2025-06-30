<script setup>
    import { RouterLink } from 'vue-router';
    import { useAuthStore } from '../../stores/auth';
    import router from '../../router';

    const auth = useAuthStore()

    const redirectFunctions = (destination) => {
        router.push(`/${destination}`)
    }
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <RouterLink to="/">
                <img src="/public/logo.png" alt="Logo" width="100px">
            </RouterLink>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">

                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Dropdown
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>
                </ul>

                <div>
                    <div class="auth-buttons" v-if="!auth.isAuthenticated">
                        <button type="button" class="btn btn-outline-success me-2" @click="redirectFunctions('login')">Accedi</button>
                        <button type="button" class="btn btn-success" @click="redirectFunctions('registration')">Registrati</button>
                    </div>

                    <div class="user" v-else>
                        <button type="button" class="btn btn-outline-danger" @click="auth.logout">Esci</button>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>