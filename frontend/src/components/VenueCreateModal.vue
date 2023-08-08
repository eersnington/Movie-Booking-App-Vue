<template>
    <div class="modal fade" id="venueCreateModal" tabindex="-1" aria-labelledby="venueCreateModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="venueCreateModalLabel">Create Venue</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createVenue">
                        <div class="row mb-3">
                            <label for="venueNameInput" class="col-sm-2 col-form-label">Venue Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="venueNameInput" v-model="newVenue.name">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="venueLocationInput" class="col-sm-2 col-form-label">Venue Location</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="venueLocationInput" v-model="newVenue.location">
                                    <option value="Chennai">Chennai</option>
                                    <option value="Bangalore">Bangalore</option>
                                    <option value="Kochi">Kochi</option>
                                </select>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary" name="submit">Create Venue</button>
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
    name: "VenueCreateModal",
    data() {
        return {
            newVenue: {
                name: '',
                location: ''
            }
        };
    },
    methods: {
        createVenue() {
            Server().post('/venue/create', this.newVenue)
                .then(response => {
                    console.log(response);
                    alert(response.data.msg);
                    this.newVenue.name = '';
                    this.newVenue.location = '';
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in creating venue");
                });
        },
        closeModal() {
            window.location.reload();
        },
    }
};
</script>

<style lang="scss" scoped></style>