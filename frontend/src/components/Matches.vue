<template>
  <div id="app">
    <h1> {{ message }} </h1>
    <button class="btn btn-success btn-lg" @click="buyTicket" :disabled="money_available < price_match"> Buy ticket </button>
    <button class="btn btn-danger btn-lg" @click="returnTicket" :disabled="tickets_bought === 0"> Return ticket </button>
    <h4> Total tickets bought: {{ tickets_bought }} </h4>
    <h4> Remaining tickets: {{ remaining_tickets }} </h4>
    <h4> Match price: {{ price_match }} </h4>
    <h4> Money available: {{ money_available }} </h4>
  </div>
</template>
<script>

export default {
  data () {
    return {
      message: 'My first component',
      tickets_bought: 0,
      remaining_tickets: 15,
      money_available: 100,
      price_match: 10
    }
  },
  methods: {
    buyTicket () {
      if (this.remaining_tickets > 0 && this.money_available >= this.price_match) {
        this.tickets_bought += 1
        this.remaining_tickets -= 1
        this.money_available -= this.price_match
      }
    },
    returnTicket () {
      if (this.tickets_bought > 0) {
        this.tickets_bought -= 1
        this.remaining_tickets += 1
        this.money_available += this.price_match
      }
    }
  }
}

</script>
