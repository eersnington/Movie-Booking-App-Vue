<template @search-applied="fetchFilteredShows">
    <div>
        <h2>Airing Now
            <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#filterOffcanvas"
                aria-controls="filterOffcanvas">
                Filter
            </button>
        </h2>

        <FilterComponent @filter-applied="updateFilteredShows" />
        <div class="container">
            <div v-if="shows.length === 0" class="col">
                <br><br>
                <h3>No shows found...</h3>
            </div>
            <div class="row" v-else>
                <div v-for="show in shows" :key="show.show_id" class="col">
                    <div class="card" style="width: 18rem;">
                        <img class="card-img-top" :src="require('@/assets/' + show.imagePath)" alt="Card image cap"
                            height="450">
                        <div class="card-body">
                            <h5 class="card-title">{{ show.name }}</h5>
                            <p class="card-text">{{ show.tags }}</p>
                            <p class="card-text">{{ show.rating }}/10</p>
                            <p class="card-text">{{ show.language }}</p>
                            <button class="btn btn-primary" @click="bookShow(show.show_id)">Book Now</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import Server from '@/Server';
import FilterComponent from '@/components/FilterComponent.vue';

export default {
    name: 'ShowsView',
    data() {
        return {
            shows: [],
            searchTerm: '',
        };
    },
    methods: {
        fetchShows() {
            Server().get('/show/get')
                .then(response => {
                    this.shows = response.data.shows;
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in fetching shows");
                });
        },
        updateFilteredShows(filteredShows) {
            this.shows = filteredShows;
        },
        async fetchFilteredShows() {
            try {
                const response = await Server().get('/show/get');
                const allShows = response.data.shows;
                this.shows = allShows.filter(show =>
                    show.name.toLowerCase().includes(this.searchTerm.toLowerCase())
                );
            } catch (error) {
                console.log(error);
                alert("Error in fetching shows");
            }
        }
    },
    mounted() {
        this.fetchShows();
        this.$parent.$on('search-applied', searchTerm => {
            this.searchTerm = searchTerm;
            this.fetchFilteredShows();
        });
    },
    components: {
        FilterComponent
    }
};
</script>
  
<style scoped></style>
  