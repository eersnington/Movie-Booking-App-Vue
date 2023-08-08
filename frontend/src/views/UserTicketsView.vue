<template>
    <div class="bookings">
        <div class="container">
            <div v-if="bookings.length === 0">
                <p>No bookings available.</p>
                <router-link to="/shows" class="btn btn-success">Book Now!</router-link>
            </div>
            <div v-else>
                <div v-for="(booking, key) in bookings" :key="key" class="card" style="max-width: 18rem;">
                    <img :src="require('@/assets/' + booking.image_src)" class="card-img-top" height="225">
                    <div class="card-body">
                        <h5 class="card-title">{{ booking.name }}</h5>
                        <p class="card-text">Seats:
                            <strong> {{ booking.seats }},</strong>
                        </p>
                        <p class="card-text">Venue: <strong>{{ booking.venue_name }}</strong></p>
                        <p class="card-text">Location: <strong>{{ booking.venue_location }}</strong></p>
                        <p class="card-text">Timings: <strong>{{ booking.timings }}</strong></p>
                    </div>
                </div>
                <br>
            </div>
        </div>
    </div>
</template>

<script>
import Server from '@/Server';

export default {
    data() {
        return {
            bookings: []
        };
    },
    mounted() {
        Server().get('/booking/get')
            .then(response => {
                this.bookings = response.data.bookings;
            })
            .catch(error => {
                console.log(error);
                alert("Error in fetching bookings");
            });
    }
};
</script>

<style scoped>
.container {
    padding: 10px;
    margin: 10px;
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    align-items: center;
}

.card {
    margin-bottom: 20px;
}
</style>
