<template>
    <div class="modal fade" :id="'showEditModal' + show.show_id" tabindex="-1"
        :aria-labelledby="'showEditModalLabel' + show.show_id" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" :id="'showEditModalLabel' + show.show_id">Edit Show {{ show.name }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="editShow">
                        <div class="row mb-3">
                            <label for="editShowNameInput" class="col-sm-2 col-form-label">Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="editShowNameInput" v-model="editedShow.name">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowRatingInput" class="col-sm-2 col-form-label">Rating</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="editShowRatingInput"
                                    v-model="editedShow.rating">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowTagsInput" class="col-sm-2 col-form-label">Tags</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="editShowTagsInput" v-model="editedShow.tags">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowLanguageInput" class="col-sm-2 col-form-label">Language</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="editShowLanguageInput" v-model="editedShow.language">
                                    <option value="English">English</option>
                                    <option value="Hindi">Hindi</option>
                                    <option value="Tamil">Tamil</option>
                                    <option value="Malayalam">Malayalam</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowImageInput" class="col-sm-2 col-form-label">Image</label>
                            <div class="col-sm-10">
                                <input type="file" class="form-control" id="editShowImageInput" @change="handleImageChange">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowTimingsInput" class="col-sm-2 col-form-label">Timings</label>
                            <div class="col-sm-10">
                                <select class="form-select" id="editShowTimingsInput" v-model="editedShow.timings">
                                    <option value="10:00AM-12:00PM">10:00AM-12:00PM</option>
                                    <option value="05:00PM-07:00PM">05:00PM-07:00PM</option>
                                    <option value="10:00PM-12:00AM">10:00PM-12:00AM</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowTicketPriceInput" class="col-sm-2 col-form-label">Ticket Price</label>
                            <div class="col-sm-10">
                                <input type="number" class="form-control" id="editShowTicketPriceInput"
                                    v-model="editedShow.ticket_price">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label for="editShowSeatsInput" class="col-sm-2 col-form-label">Seats</label>
                            <div class="col-sm-10">
                                <input type="number" class="form-control" id="editShowSeatsInput"
                                    v-model="editedShow.seats">
                            </div>
                        </div>
                        <button @click="deleteShow(show.show_id)" class="btn btn-danger">Delete Show</button>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import Server from "@/Server";

export default {
    name: "ShowEditModal",
    props: {
        show: Object,
    },
    data() {
        return {
            editedShow: {
                show_id: this.show.show_id,
                venue_id: this.show.venue_id,
                name: this.show.name,
                rating: this.show.rating,
                tags: this.show.tags,
                language: this.show.language,
                image_src: this.show.imagePath,
                timings: this.show.timings,
                ticket_price: this.show.price,
                seats: this.show.seats,

            },
        };
    },
    methods: {
        editShow() {
            Server().post(`/show/update`, this.editedShow)
                .then(response => {
                    console.log(response);
                    alert(response.data.msg);
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in editing show");
                });
        },
        handleImageChange(event) {
            const file = event.target.files[0];

            if (file) {
                this.editedShow.image_src = file.name;
            }
        },
        deleteShow(showID) {
            Server().post(`/show/delete`, { show_id: showID })
                .then(response => {
                    console.log(response);
                    window.location.reload();
                })
                .catch(error => {
                    console.log(error);
                    alert("Error in deleting show");
                });
        },
        closeModal() {
            window.location.reload();
        },
    },
}
</script>
  