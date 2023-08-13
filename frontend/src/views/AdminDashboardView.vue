<template>
    <div class="dashboard">
        <h1>Admin Dashboard</h1>
        <!-- Venue Create Form -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#venueCreateModal">
            + Add Venues
        </button>

        <!-- Venue Cards -->
        <div v-if="venues.length === 0">
            <p>No venues available!</p>
        </div>
        <div v-else>
            <div v-for="venue in venues" :key="venue.venue_id" class="card text-dark border-primary" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title text-primary"> {{ venue.name }} </h5>
                    <p class="card-text">Location: {{ venue.location }}</p>

                    <div v-for="show in shows.filter(s => s.venue_id == venue.venue_id)" :key="show.show_id">
                        <ShowEditModal :show="show" />

                        <button type="button" class="btn btn-secondary" data-bs-toggle="modal"
                            :data-bs-target="'#showEditModal' + show.show_id">
                            Show {{ show.show_id }}
                        </button>
                    </div>

                    <VenueEditModal :venue="venue" />
                    <ShowCreateModal :venue="venue" />

                    <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                        :data-bs-target="'#showsCreateModal' + venue.venue_id">
                        + Add Shows
                    </button>

                </div>
                <div class="card-footer">
                    <!-- Venue Edit and Delete Buttons -->
                    <button @click="exportCSV(venue.venue_id)" class="btn btn-success">Export CSV</button>
                    <button @click="deleteVenue(venue.venue_id)" class="btn btn-danger">Delete Venue</button>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                        :data-bs-target="'#venueEditModal' + venue.venue_id">
                        Edit
                    </button>
                </div>
            </div>
        </div>
        <VenueCreateModal />
    </div>
</template>
  
<script>
import ShowCreateModal from "@/components/ShowCreateModal.vue";
import VenueCreateModal from "@/components/VenueCreateModal.vue";
import VenueEditModal from "@/components/VenueEditModal.vue";
import ShowEditModal from "@/components/ShowEditModal.vue";

import Server from "@/Server";

export default {
    name: "AdminDashboardView",
    data() {
        return {
            venues: [],
            shows: [],
        };
    },
    methods: {
        fetchVenues() {
            Server().get('/venue/get')
                .then(response => {
                    this.venues = response.data.venues;
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in fetching venues");
                });
        },
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
        deleteVenue(venueID) {
            Server().post(`/venue/delete`, { venue_id: venueID })
                .then(response => {
                    console.log(response);
                    window.location.reload();
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in deleting venue");
                });
        },
        exportCSV(venueID) {
            Server().post(`/export`, { venue_id: venueID })
                .then(response => {

                    setTimeout(this.checkCSV(response.data.msg), 3000);
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in exporting csv");
                });
        },
        checkCSV(id) {
            Server().post(`/export/status`, { task_id: id })
                .then(response => {
                    alert(response.data.msg);
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in checking csv");
                });
        }
    },
    created() {
        this.fetchVenues();
        this.fetchShows();
    },
    components: { VenueCreateModal, ShowCreateModal, VenueEditModal, ShowEditModal }
};
</script>



<style scoped>
.btn {
    margin: 5px;
    padding: 10px;
}

.card {
    margin: 10px;
    padding: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.card-body {
    border-radius: 10px;
    margin: 10px;
    padding: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
</style>