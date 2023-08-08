<template>
    <div class="modal fade" :id="'venueEditModal' + venue.venue_id" tabindex="-1"
        :aria-labelledby="'venueEditModalLabel' + venue.venue_id" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" :id="'venueEditModalLabel' + venue.venue_id">Edit Venue</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="editVenue" id="venueEditForm">
                        <div class="row mb-3">
                            <label for="venueNameEditInput" class="col-sm-2 col-form-label">Venue Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="venueNameEditInput" v-model="editedVenue.name">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="venueLocationEditInput" class="col-sm-2 col-form-label">Venue Location</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="venueLocationEditInput" v-model="editedVenue.location">
                                    <option value="Chennai">Chennai</option>
                                    <option value="Bangalore">Bangalore</option>
                                    <option value="Kochi">Kochi</option>
                                </select>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary" name="submit">Edit Venue</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button @click="closeModal" type="button" class="btn btn-secondary"
                        data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import Server from '@/Server';

export default {
    name: 'VenueEditModal',
    props: {
        venue: Object,
    },
    data() {
        return {
            editedVenue: {
                id: this.venue.venue_id,
                name: this.venue.name,
                location: this.venue.location,
            },
        };
    },
    methods: {
        editVenue() {
            Server().post(`/venue/update`, this.editedVenue)
                .then(response => {
                    console.log(response);
                    alert(response.data.msg);
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in editing venue");
                });
        },
        closeModal() {
            window.location.reload();
        },
    }
};
</script>
  