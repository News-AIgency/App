<template>
    <div class="container">
        <div class="steps">
            <span class="circle" :class="{ active: isActive[0] }">1</span>
            <span class="circle" :class="{ active: isActive[1] }">2</span>
            <span class="circle" :class="{ active: isActive[2] }">3</span>
            <div id="progress-bar" class="progress-bar">
                <span class="indicator"></span>
            </div>
        </div>
        <div class="step-descriptions">
            <p>Article<br>URL</p>
            <p>Select<br>topic</p>
            <p>Save<br>results</p>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        activePage: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            isActive: [false, false, false],
        };
    },
    watch: {
        isActive: {
            handler: 'setStep',
            deep: true,
        },
        activePage: {
            immediate: true,
            handler(newPage) {
                this.updateActiveSteps(newPage);
            },
        },
    },
    methods: {
        updateActiveSteps(page: number) {
            this.isActive = [false, false, false];
            if (page >= 1 && page < this.isActive.length + 1) {
                this.isActive[page - 1] = true;
            }
            this.setStep();
        },
        setStep() {
            const progressBar = document.getElementById("progress-bar")
            if (progressBar) {
                if (this.isActive[0]) {
                    progressBar.style.background = `linear-gradient(
                        to right, 
                        #9f00ff 0%, 
                        #9f00ff 27%, 
                        #545454 27%, 
                        #545454 100%
                    )`;
                } else if (this.isActive[1]) {
                    progressBar.style.background = `linear-gradient(
                        to right, 
                        #545454 0%, 
                        #545454 25%, 
                        #9f00ff 25%, 
                        #9f00ff 75%, 
                        #545454 75%, 
                        #545454 100%
                    )`;
                } else if (this.isActive[2]) {
                    progressBar.style.background = `linear-gradient(
                        to right, 
                        #545454 0%, 
                        #545454 73%, 
                        #9f00ff 73%, 
                        #9f00ff 100%
                    )`;
                } else {
                    progressBar.style.background = `#545454`;
                }
            }
        }
    }
}
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    justify-self: center;
    max-width: 500px;
    width: 75vw;
}

.steps {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
    position: relative;
}

.step-descriptions {
    display: flex;
    flex-direction: row;
    justify-self: center;
    justify-content: space-between;
    text-align: center;
    width: 99%;
}

.circle {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 500;
    color: var(--color-text);
    height: 50px;
    width: 50px;
    border-radius: 50%;
    background-color: #545454;
    border: 4px solid #444343;
}

.active {
    background-color: var(--color-accent) !important;
    border: 4px solid #5a0092 !important;
}

.progress-bar {
    position: absolute;
    height: 4px;
    width: 100%;
    background-color: #545454;
    z-index: -1;
}
</style>