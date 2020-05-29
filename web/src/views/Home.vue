<template>
    <div class="home">
        <main role="main" class="container">
            <div class="starter-template">
                <h1>{{getLang.semiAutomaticColorization}}</h1>
                <p class="lead">{{getLang.diplomaTopic}} <br>{{getLang.topic}}</p>
                <br>
                <h3>{{getLang.workAllows}}:</h3>
                <p>1. {{getLang.firstAllow}}<br>
                    2. {{getLang.secondAllow}}<br>
                    3. {{getLang.thirdAllow}}<br>
                    4. {{getLang.fourthAllow}}<br>
                    5. {{getLang.fifthAllow}}
                </p>
            </div>

        </main>
    </div>
</template>

<script>
    import {localization} from "../localization/localization";

    export default {
        name: 'Home',
        computed: {
            getLang() {
                if (this.$store.getters.getLocalization) {
                    return localization.en;
                }
                return localization.ua;
            },
        },
    }
</script>
