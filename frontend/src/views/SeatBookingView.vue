<template>
    <div class="form-seatBooking">
        <form @submit.prevent="confirmBooking">
            <div class="container">
                <h5>{{ showInfo.name }}</h5>
                <div class="movieScreen"></div>
                <p> Movie Screen </p>
                <div v-for="row in rows" :key="row" class="row text-success">
                    {{ row }}
                    <div v-for="seatNumber in seatNumbers" :key="seatNumber" class="col-sm">
                        <input class="form-check-input" type="checkbox" :value="row + seatNumber"
                            :id="'seat' + row + seatNumber" :name="'seat' + row + seatNumber" v-model="selectedSeats"
                            v-bind="{ checked: isSeatBooked(row + seatNumber), disabled: isSeatBooked(row + seatNumber) }" />
                        <label :for="'seat' + row + seatNumber" class="form-check-label">
                            {{ row + seatNumber }}
                        </label>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm">
                        <p>Venue: <strong>{{ showInfo.venue_name }}</strong></p>
                        <p>Location: <strong>{{ showInfo.venue_location }}</strong></p>
                        <p>Price Per Ticket: <strong>{{ showInfo.price }}</strong></p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm">
                        <button class="btn btn-lg btn-primary w-100" type="submit">Confirm Booking</button>
                    </div>
                </div>
                <br>
            </div>
            <br>
        </form>
    </div>
</template>
  
<script>
import Server from '@/Server';

export default {
    data() {
        return {
            showID: this.$route.params.showId,
            showInfo: {},
            bookedSeats: [],
            selectedSeats: []
        };
    },
    computed: {
        rows() {
            return ['A', 'B', 'C', 'D', 'E'];
        },
        seatNumbers() {
            return ['1', '2', '3', '4', '5'];
        }
    },
    methods: {
        isSeatBooked(seat) {
            return this.bookedSeats.includes(seat);
        },
        confirmBooking() {
            if (this.selectedSeats.length === 0) {
                alert('Please select at least one seat.');
                return;
            }

            if (localStorage.getItem('token') === null) {
                alert('Please login to book tickets.');
                return;
            }

            console.log('Selected Seats:', this.selectedSeats);
        }
    },
    mounted() {
        Server().get('/show/get/' + this.showID)
            .then(response => {
                this.showInfo = response.data.shows;

                console.log(this.showInfo)
            })
            .catch(error => {
                console.log(error);
                alert("Error in fetching the show info");
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

.movieScreen {
    border-top: 128px solid;
    border-left: 32px solid transparent;
    border-right: 32px solid transparent;
}
</style>
  