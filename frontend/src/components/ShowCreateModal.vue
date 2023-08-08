
  
<template>
    <div class="modal fade" :id="'showsCreateModal' + venue.venue_id" tabindex="-1"
        :aria-labelledby="'showCreateModalLabel' + venue.venue_id" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" :id="'showCreateModalLabel' + venue.venue_id">Add Shows for {{ venue.name }}
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addShow" id="showForm">
                        <div class="row mb-3">
                            <label for="movieNameInput" class="col-sm-2 col-form-label">Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="movieNameInput" v-model="newShow.movieName">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="movieRatingInput" class="col-sm-2 col-form-label">Rating</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="movieRatingInput" v-model="newShow.movieRating">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="movieTagsInput" class="col-sm-2 col-form-label">Tags</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="movieTagsInput" v-model="newShow.movieTags">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="movieLanguageInput" class="col-sm-2 col-form-label">Language</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="movieLanguageInput" v-model="newShow.movieLanguage">
                                    <option value="English">English</option>
                                    <option value="Hindi">Hindi</option>
                                    <option value="Tamil">Tamil</option>
                                    <option value="Malayalam">Malayalam</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="showTimingsInput" class="col-sm-2 col-form-label">Timings</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="showTimingsInput" v-model="newShow.showTimings">
                                    <option value="10:00AM-12:00PM">10:00AM-12:00PM</option>
                                    <option value="05:00PM-07:00PM">05:00PM-07:00PM</option>
                                    <option value="10:00PM-12:00AM">10:00PM-12:00AM</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="showImageInput" class="col-sm-2 col-form-label">Image</label>
                            <div class="col-sm-10">
                                <input type="file" class="form-control" id="showImageInput" @change="handleImageUpload">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="seatsInput" class="col-sm-2 col-form-label">Seats</label>
                            <div class="col-sm-10">
                                <input type="number" class="form-control" id="seatsInput" v-model="newShow.seats">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="ticketPriceInput" class="col-sm-2 col-form-label">Price</label>
                            <div class="col-sm-10">
                                <input type="number" class="form-control" id="ticketPriceInput"
                                    v-model="newShow.ticketPrice">
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary" name="submit" value="Add Show">Add Show</button>
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
    name: "ShowCreateModal",
    props: {
        venue: Object,
    },
    data() {
        return {
            newShow: {
                venue_id: this.venue.venue_id,
                movieName: '',
                movieRating: '',
                movieTags: '',
                movieLanguage: 'English',
                imageFile: null,
                showTimings: '10:00AM-12:00PM',
                ticketPrice: '',
                seats: ''
            }
        };
    },
    methods: {
        addShow() {

            Server().post('/show/create', this.newShow)
                .then((response) => {
                    console.log(response);
                    alert(response.data.msg);
                    this.newShow.movieName = '';
                    this.newShow.movieRating = '';
                    this.newShow.movieTags = '';
                    this.newShow.movieLanguage = 'English';
                    this.newShow.imageFile = null;
                    this.newShow.showTimings = '10:00AM-12:00PM';
                    this.newShow.ticketPrice = '';
                    this.newShow.seats = '';
                })
                .catch((error) => {
                    console.log(error);
                    alert("Error in creating show");
                });
        },
        handleImageUpload(event) {
            const file = event.target.files[0];

            if (file) {
                this.newShow.imageFile = file.name;
            }
        },
        closeModal() {
            window.location.reload();
        },
    }
};
</script>