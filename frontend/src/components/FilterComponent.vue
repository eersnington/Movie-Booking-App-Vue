<template>
    <div class="offcanvas offcanvas-start" id="filterOffcanvas">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="filterOffcanvasLabel">Filter Search</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <form @submit.prevent="submitFilter" id="filterSearchForm">
                <div class="row mb-3">
                    <p style="font-weight: bold;">Movie Ratings:</p>
                    <div class="col-sm-10">
                        <label for="minRating" class="col-sm-4 col-form-label">Min</label>
                        <input type="number" class="form-control" id="minRating" v-model="filter.minRating" max="10"
                            min="0">
                    </div>
                </div>
                <div class="row mb-3">
                    <p style="font-weight: bold;">Movie Language:</p>
                    <div class="col-sm-10">
                        <select class="form-select" id="languageInput" v-model="filter.language">
                            <option selected value="Any">Any</option>
                            <option value="English">English</option>
                            <option value="Hindi">Hindi</option>
                            <option value="Tamil">Tamil</option>
                            <option value="Malayalam">Malayalam</option>
                        </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <p style="font-weight: bold;">Venue Location:</p>
                    <div class="col-sm-10">
                        <select class="form-select" id="locationInput" v-model="filter.location">
                            <option selected value="Any">Any</option>
                            <option value="Chennai">Chennai</option>
                            <option value="Bangalore">Bangalore</option>
                            <option value="Kochi">Kochi</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary" name="submit" value="Filter">Edit Search</button>
            </form>
        </div>
    </div>
</template>
  
<script>
import Server from '@/Server';

export default {
    name: 'FilterComponent',
    data() {
        return {
            filter: {
                minRating: '0',
                language: 'Any',
                location: 'Any',
            },
        };
    },
    methods: {
        submitFilter() {
            Server().post('/filter', this.filter)
                .then((response) => {
                    this.$emit('filter-applied', response.data.shows);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>
  