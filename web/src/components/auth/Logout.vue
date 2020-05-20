<template>
</template>

<script>
    import accessToken from '../../helpers/access-token';
    export default {
        created() {
            accessToken.removeToken();
            this.$router.push({ name: 'home' });
        }
    }
</script>
